
import os
import cv2
import numpy as np
from face_recognition import extract_embedding

DATA_PATH = "registered_faces/face_data.npz"


def register_person(name, uploaded_image):

    name = name.strip()

    if not name:
        return False, "Please enter a name."

    if uploaded_image is None:
        return False, "Please upload one photograph."

    image_bytes = uploaded_image.getvalue()

    image = cv2.imdecode(
        np.frombuffer(image_bytes, np.uint8),
        cv2.IMREAD_COLOR
    )

    if image is None:
        return False, "Invalid image."

    embedding = extract_embedding(image)

    if embedding is None:
        return False, "No face detected in the photograph."

    os.makedirs("registered_faces", exist_ok=True)

    if os.path.exists(DATA_PATH):

        with np.load(DATA_PATH, allow_pickle=True) as data:
            names = list(data["names"])
            saved_embeddings = list(data["embeddings"])

        if name.lower() in [n.lower() for n in names]:
            return False, "This person is already registered."

    else:
        names = []
        saved_embeddings = []

    names.append(name)
    saved_embeddings.append(embedding)

    np.savez(
        DATA_PATH,
        names=np.array(names),
        embeddings=np.array(saved_embeddings)
    )

    return True, f"{name} registered successfully!"
