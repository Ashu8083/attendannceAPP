from app.exceptions.custom_exception import FaceNotFound
from app.face_model.aligner import FaceAligner
from app.face_model.detector import FaceDetector
from app.face_model.mobilefacenet import MobileFaceNet
from app.face_model.verifier import FaceVerifier

import numpy as np


class FaceService:
    def __init__(
        self
    ):
        self.detector = FaceDetector()
        self.aligner = FaceAligner()
        self.mobile_face_net = MobileFaceNet()
        self.verifier = FaceVerifier()

    def extract_embedding(self, image: np.ndarray) -> np.ndarray:

        faces = self.detector.detect(image)

        if len(faces) != 1:
            raise FaceNotFound()

        face = self.aligner.align(image, faces[0])

        embedding = self.mobile_face_net.get_embedding(face)

        embedding /= np.linalg.norm(embedding)

        return embedding

    def verify(
        self,
        image: np.ndarray,
        stored_embedding: np.ndarray,
    ):

        live_embedding = self.extract_embedding(image)

        return self.verifier.verify(
            live_embedding,
            stored_embedding,
        )