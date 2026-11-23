import cv2
import av
import threading
import streamlit as st
import numpy as np

from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from face_recognition import detector, recognizer
from attendance import mark_attendance
import pandas as pd
import sqlite3
from datetime import datetime
from registration import register_person


st.set_page_config(
    page_title="Face Attendance Dashboard",
    layout="wide"
)
class AttendanceProcessor(VideoProcessorBase):

    def __init__(self, names, embeddings):
        self.names = names
        self.embeddings = embeddings
        self.marked_names = set()
        self.lock = threading.Lock()

    def recv(self, frame):

        image = frame.to_ndarray(format="bgr24")

        height, width = image.shape[:2]
        detector.setInputSize((width, height))

        _, faces = detector.detect(image)

        if faces is not None:

            for face in faces:

                x, y, w, h = map(int, face[:4])

                aligned_face = recognizer.alignCrop(image, face)
                embedding = recognizer.feature(aligned_face).flatten()
                embedding = embedding / np.linalg.norm(embedding)

                best_name = "Unknown"
                best_score = -1

                for name, saved_embedding in zip(
                    self.names, self.embeddings
                ):
                    score = float(np.dot(embedding, saved_embedding))

                    if score > best_score:
                        best_score = score
                        best_name = name

                if best_score >= 0.40:

                    with self.lock:
                        if best_name not in self.marked_names:
                            mark_attendance(best_name)
                            self.marked_names.add(best_name)

                    color = (0, 255, 0)
                    label = f"{best_name} - PRESENT"

                else:
                    color = (0, 0, 255)
                    label = "Unknown"

                cv2.rectangle(
                    image,
                    (x, y),
                    (x + w, y + h),
                    color,
                    2
                )

                cv2.putText(
                    image,
                    label,
                    (x, max(y - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2
                )

        return av.VideoFrame.from_ndarray(
            image,
            format="bgr24"
        )
st.set_page_config(
    page_title="Face Attendance Dashboard",
    layout="wide"
)

st.title("Face Recognition Attendance System")
st.subheader("Register a Student")

with st.expander("Register New Student", expanded=True):

    student_name = st.text_input("Student Name")

    student_photo = st.file_uploader(
        "Upload one clear face photograph",
        type=["jpg", "jpeg", "png"]
    )

    if st.button("Register Student"):

        if not student_name.strip():
            st.error("Please enter student name.")

        elif student_photo is None:
            st.error("Please upload a photograph.")

        else:
            success, message = register_person(
                student_name,
                student_photo
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

# Load registered faces
try:
    with np.load(
        "registered_faces/face_data.npz",
        allow_pickle=True
    ) as data:
        registered_names = list(data["names"])
        registered_embeddings = list(data["embeddings"])

except FileNotFoundError:
    registered_names = []
    registered_embeddings = []

# Attendance scanning
st.subheader("Live Attendance Scanner")

if not registered_names:
    st.warning("Register students before scanning attendance.")

else:
    webrtc_streamer(
        key="attendance-scanner",
        video_processor_factory=lambda: AttendanceProcessor(
            registered_names,
            registered_embeddings
        ),
        media_stream_constraints={
            "video": True,
            "audio": False
        },
        async_processing=True
    )

if st.button("Refresh Attendance Dashboard"):
    st.rerun()

# Load today's attendance
conn = sqlite3.connect("attendance.db")

today = datetime.now().strftime("%Y-%m-%d")

attendance = pd.read_sql_query(
    "SELECT name, date, time FROM attendance WHERE date = ?",
    conn,
    params=(today,)
)

conn.close()

present_names = attendance["name"].tolist()

absent_names = [
    name for name in registered_names
    if name not in present_names
]

# Dashboard metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Registered", len(registered_names))
col2.metric("Present Today", len(present_names))
col3.metric("Absent Today", len(absent_names))

st.divider()

# Attendance table
st.subheader("Today's Attendance")

if not attendance.empty:
    st.dataframe(attendance, use_container_width=True)
else:
    st.info("No attendance recorded today.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Present")
    for name in present_names:
        st.write(name)

with col2:
    st.subheader("Absent")
    for name in absent_names:
        st.write(name)

# CSV download
if not attendance.empty:

    csv = attendance.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Attendance CSV",
        csv,
        file_name=f"attendance_{today}.csv",
        mime="text/csv"
    )

