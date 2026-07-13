# app/services/insightface_service.py

import cv2
import numpy as np

from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity

from .BaseFaceService import BaseFaceService


class InsightFaceService(BaseFaceService):

    def __init__(self):

        self.app = FaceAnalysis()

        self.app.prepare(ctx_id=-1)

    def generate_embedding(
        self,
        image_bytes: bytes
    ) -> np.ndarray:

        image = cv2.imdecode(
            np.frombuffer(image_bytes, np.uint8),
            cv2.IMREAD_COLOR,
        )

        faces = self.app.get(image)

        if len(faces) == 0:
            raise Exception("No face detected")

        if len(faces) > 1:
            raise Exception("Multiple faces detected")

        return faces[0].embedding

    def verify_embedding(
        self,
        new_embedding,
        stored_embedding,
        threshold=0.85,
    ):

        score = cosine_similarity(
            [new_embedding],
            [stored_embedding],
        )[0][0]

        return score >= threshold