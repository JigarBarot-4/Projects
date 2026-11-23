
import cv2
import numpy as np

from face_recognition import detector, recognizer
from attendance import mark_attendance


DATA_PATH = "registered_faces/face_data.npz"
THRESHOLD = 0.40


def load_registered_faces():
    with np.load(DATA_PATH, allow_pickle=True) as data:
        names = list(data["names"])
        embeddings = list(data["embeddings"])

    return names, embeddings


def recognize_one_face(frame, face, names, embeddings):

    aligned_face = recognizer.alignCrop(frame, face)

    embedding = recognizer.feature(aligned_face).flatten()
    embedding = embedding / np.linalg.norm(embedding)

    best_name = "Unknown"
    best_score = -1

    for name, saved_embedding in zip(names, embeddings):

        score = float(np.dot(embedding, saved_embedding))

        if score > best_score:
            best_score = score
            best_name = name

    if best_score >= THRESHOLD:
        return best_name

    return "Unknown"


def run_camera():

    names, embeddings = load_registered_faces()

    camera = cv2.VideoCapture(0)

    marked_names = set()

    while True:

        success, frame = camera.read()

        if not success:
            break

        height, width = frame.shape[:2]

        detector.setInputSize((width, height))

        _, faces = detector.detect(frame)

        if faces is not None:

            for face in faces:

                x, y, w, h = map(int, face[:4])

                name = recognize_one_face(
                    frame, face, names, embeddings
                )

                if name != "Unknown":

                    if name not in marked_names:
                        result = mark_attendance(name)
                        marked_names.add(name)
                        print(name, "-", result)

                    color = (0, 255, 0)
                    label = f"{name} - PRESENT"

                else:

                    color = (0, 0, 255)
                    label = "Unknown"

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    color,
                    2
                )

                cv2.putText(
                    frame,
                    label,
                    (x, max(y - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2
                )

        cv2.imshow("Automatic Face Attendance", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_camera()
