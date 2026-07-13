# app/services/face_service.py

from abc import ABC, abstractmethod
import numpy as np


class BaseFaceService(ABC):

    @abstractmethod
    def generate_embedding(self, image_bytes: bytes) -> np.ndarray:
        pass

    @abstractmethod
    def verify_embedding(
        self,
        new_embedding: np.ndarray,
        stored_embedding: np.ndarray,
        threshold: float = 0.75,
    ) -> bool:
        pass