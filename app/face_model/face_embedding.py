# app/utils/face_embedding.py
import numpy as np
import cv2
import threading
import logging
from insightface.app import FaceAnalysis

from app.exceptions.custom_exception import FaceNotFound

logger = logging.getLogger(__name__)

# -------------------------------------------------------
# InsightFace Singleton (buffalo_l)
# -------------------------------------------------------
_app = None
_lock = threading.Lock()

app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"]
)
app.prepare(ctx_id=-1)


def _load_model():
    global _app

    if _app is not None:
        return _app

    with _lock:
        if _app is not None:
            return _app

        logger.info("Loading InsightFace model (buffalo_l)...")
        try:
            _app = FaceAnalysis(
                name="buffalo_l",
                providers=["CPUExecutionProvider"]
            )
            _app.prepare(ctx_id=0, det_size=(640, 640))
            logger.info("InsightFace model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load InsightFace model: {str(e)}")
            raise


    return _app


# -------------------------------------------------------
# Public API
# -------------------------------------------------------
def extract_face_embedding(image_path: str) -> list[float]:
    """
    Returns a 512-D normalized embedding using InsightFace
    """
    try:
        logger.info(f"Extracting face embedding from: {image_path}")
        
        # Load model
        app = _load_model()
        
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            logger.error(f"Cannot read image: {image_path}")
            raise ValueError("Image not readable or corrupted")
        
        logger.info(f"Image loaded: {img.shape}")
        
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        faces = app.get(img_rgb)
        
        if not faces:
            logger.error(f"No face detected in image: {image_path}")
            raise ValueError("No face detected in the image")
        
        logger.info(f"Found {len(faces)} face(s)")
        
        # Pick largest face
        face = max(
            faces,
            key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1])
        )
        
        logger.info(f"Selected face bbox: {face.bbox}")
        
        # Get embedding
        embedding = face.embedding  # (512,)
        logger.info(f"Raw embedding shape: {embedding.shape}")
        
        # L2 normalize (important for cosine similarity)
        norm = np.linalg.norm(embedding)
        if norm == 0:
            logger.error("Face embedding norm is zero")
            raise ValueError("Invalid face embedding (zero norm)")
            
        embedding = embedding / norm
        
        logger.info(f"Normalized embedding, norm: {np.linalg.norm(embedding):.4f}")
        
        return embedding.astype(float).tolist()
        
    except Exception as e:
        logger.error(f"Error extracting face embedding: {str(e)}")
        raise

def extract_face_embedding_db(image_bytes: bytes) -> list[float]:

    image = cv2.imdecode(
        np.frombuffer(image_bytes, np.uint8),
        cv2.IMREAD_COLOR,
    )
    if image is None:
            raise FaceNotFound

    faces = app.get(image)

    if len(faces) == 0:

        raise FaceNotFound

    face = max(

        faces,

        key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1])

    )

    embedding = face.embedding

    embedding /= np.linalg.norm(embedding)

    return embedding.tolist()