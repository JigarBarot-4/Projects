
import cv2
import os

yunet_path = "models/face_detection_yunet_2026may.onnx"
sface_path = "models/face_recognition_sface_2021dec.onnx"

print("Testing YuNet...")

detector = cv2.FaceDetectorYN.create(
    yunet_path,
    "",
    (320, 320)
)

print("YuNet loaded successfully!")

print("\nTesting SFace...")

recognizer = cv2.FaceRecognizerSF.create(
    sface_path,
    ""
)

print("SFace loaded successfully!")

print("\nBoth models are ready!")
