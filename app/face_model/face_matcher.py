# app/utils/face_matcher.py
import numpy as np
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


def arcface_match(
    stored_embedding: list[float],
    live_embedding: list[float],
) -> Tuple[float, float]:
    """
    Returns:
      similarity: cosine similarity (-1.0 to 1.0)
      confidence: human readable percentage (0–100, UI only)
    """
    try:
        a = np.asarray(stored_embedding, dtype=np.float32)
        b = np.asarray(live_embedding, dtype=np.float32)
        
        logger.info(f"Comparing embeddings: stored shape={a.shape}, live shape={b.shape}")
        
        # Cosine similarity (ArcFace standard)
        similarity = float(np.dot(a, b))
        similarity = max(-1.0, min(1.0, similarity))
        
        # Convert to percentage for UI
        confidence = (similarity + 1.0) * 50.0
        
        logger.info(f"Match result: similarity={similarity:.4f}, confidence={confidence:.1f}%")
        
        return round(similarity, 4), round(confidence, 2)
        
    except Exception as e:
        logger.error(f"Error in arcface_match: {str(e)}")
        raise
