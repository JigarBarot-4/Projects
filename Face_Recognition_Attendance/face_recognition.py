
import cv2
import numpy as np

# Model paths
YUNET_PATH = "models/face_detection_yunet_2026may.onnx"
SFACE_PATH = "models/face_recognition_sface_2021dec.onnx"

# Load models
detector = cv2.FaceDetectorYN.create(
    YUNET_PATH,
    "",
    (320, 320),
    0.8,
    0.3,
    5000
)

recognizer = cv2.FaceRecognizerSF.create(
    SFACE_PATH,
    ""
)


def extract_embedding(image):

    height, width = image.shape[:2]

    detector.setInputSize((width, height))

    _, faces = detector.detect(image)

    if faces is None or len(faces) == 0:
        return None

    if len(faces) > 1:
        raise ValueError("Multiple faces detected. Upload one person's face at a time.")

    face = faces[0]

    # Align and crop face
    aligned_face = recognizer.alignCrop(image, face)

    # Generate facial embedding
    embedding = recognizer.feature(aligned_face)

    # Normalize embedding
    embedding = embedding.flatten()
    embedding = embedding / np.linalg.norm(embedding)

    return embedding


def recognize_face(image, registered_names, registered_embeddings):

    embedding = extract_embedding(image)

    if embedding is None:
        return "No face detected"

    best_match = None
    best_score = -1

    for name, saved_embedding in zip(
        registered_names, registered_embeddings
    ):

        score = float(
            np.dot(embedding, saved_embedding) /
            (np.linalg.norm(embedding) * np.linalg.norm(saved_embedding))
        )

        if score > best_score:
            best_score = score
            best_match = name

    if best_score >= 0.40:
        return best_match

    return "Unknown"

