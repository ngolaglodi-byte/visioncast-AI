"""VisionCast-AI inter-process communication sub-module."""

from .protocol import (
    FaceLocation,
    Heartbeat,
    LogMessage,
    TalentInfo,
    TalentOverlayMessage,
    RecognizedFace,
    RecognitionResult,
)
from .metadata_sender import MetadataSender
from .zmq_sender import ZmqSender

__all__ = [
    "FaceLocation",
    "Heartbeat",
    "LogMessage",
    "TalentInfo",
    "TalentOverlayMessage",
    "RecognizedFace",
    "RecognitionResult",
    "MetadataSender",
    "ZmqSender",
]
