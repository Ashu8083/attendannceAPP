# mobilefacenet.py

from pathlib import Path
import onnxruntime as ort
import numpy as np

class MobileFaceNet:
    def __init__(self):
        model_path = Path(__file__).parent / "model" / "mobilefacenet.onnx"

        self.session = ort.InferenceSession(
            str(model_path),
            providers=["CPUExecutionProvider"]
        )

    def get_embedding(
        self,
        face: np.ndarray
    ) -> np.ndarray:

        pass