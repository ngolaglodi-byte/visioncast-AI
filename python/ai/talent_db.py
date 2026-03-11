"""Talent database loader and manager."""

import json
import logging
import os
from typing import Optional

import numpy as np

try:
    import face_recognition
except ImportError:
    face_recognition = None

logger = logging.getLogger(__name__)


class TalentDB:
    """Loads talent faces and metadata from the JSON database.

    Args:
        talents_path: Path to talents.json file.
        project_root: Root directory for resolving relative image paths.
    """

    def __init__(self, talents_path: str, project_root: Optional[str] = None):
        self.talents_path = talents_path
        self.project_root = project_root or os.path.dirname(
            os.path.dirname(os.path.abspath(talents_path))
        )
        self.talents: list = []
        self.encodings: list = []

    def load(self) -> None:
        """Load talent metadata and compute face encodings."""
        if face_recognition is None:
            raise ImportError(
                "face_recognition is required. Install with: "
                "pip install face_recognition"
            )

        if not os.path.isfile(self.talents_path):
            logger.error("Talents file not found: %s", self.talents_path)
            return

        with open(self.talents_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.talents = []
        self.encodings = []

        for talent in data.get("talents", []):
            photo_path = talent.get("photo", "")
            if not photo_path:
                logger.warning(
                    "[TalentDB] No photo path for talent '%s'. Skipping.",
                    talent.get("name", "unknown")
                )
                continue

            image_path = os.path.join(self.project_root, photo_path)
            if not os.path.exists(image_path):
                logger.warning("[TalentDB] Image not found: %s", image_path)
                continue

            try:
                img = face_recognition.load_image_file(image_path)
                enc = face_recognition.face_encodings(img)
            except Exception as exc:
                logger.warning(
                    "[TalentDB] Failed to process image %s: %s", image_path, exc
                )
                continue

            if len(enc) > 0:
                self.encodings.append(enc[0])
                self.talents.append(talent)
            else:
                logger.warning("[TalentDB] No face found in %s", image_path)

        logger.info("[TalentDB] Loaded %d talent(s).", len(self.talents))

    def get_talent(self, index: int) -> dict:
        """Get talent metadata by index."""
        return self.talents[index]

    def get_encoding(self, index: int) -> np.ndarray:
        """Get face encoding by index."""
        return self.encodings[index]

    def count(self) -> int:
        """Return number of loaded talents."""
        return len(self.talents)
