# verifier.py
import numpy as np
class FaceVerifier:
    def verify(
        self,
        emb1: np.ndarray,
        emb2: np.ndarray,
        threshold: float = 0.65
    ):

        emb1 /= np.linalg.norm(emb1)
        emb2 /= np.linalg.norm(emb2)

        similarity = np.dot(emb1, emb2)

        return {
            "verified": similarity >= threshold,
            "similarity": float(similarity)
        }