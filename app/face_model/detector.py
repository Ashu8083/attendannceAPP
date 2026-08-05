# detector.py
import cv2
import numpy as np

class FaceDetector:
    def detect(self, image: np.ndarray):
        """
        Returns:
            [
                {
                    "bbox": [x1, y1, x2, y2],
                    "landmarks": ...
                }
            ]
        """
        pass