"""System metrics collector for the VisionCast monitoring panel.

Collects CPU usage, GPU usage (if available), and tracks FPS for
real-time display in the monitoring panel.  Metrics are exposed as a
plain dictionary so they can be forwarded to the C++ UI via ZeroMQ or
consumed directly in Python.
"""

import os
import time
from dataclasses import dataclass


@dataclass
class SystemMetrics:
    """Snapshot of system performance metrics."""

    cpu_percent: float = 0.0
    gpu_percent: float = 0.0
    fps: float = 0.0
    latency_ms: float = 0.0
    dropped_frames: int = 0

    def to_dict(self) -> dict:
        """Serialize to a plain dictionary."""
        return {
            "cpu_percent": self.cpu_percent,
            "gpu_percent": self.gpu_percent,
            "fps": self.fps,
            "latency_ms": self.latency_ms,
            "dropped_frames": self.dropped_frames,
        }


class SystemMonitor:
    """Lightweight system metrics collector.

    Reads CPU usage from ``/proc/stat`` (Linux) and tracks FPS via an
    internal frame counter.  GPU usage is read from
    ``/sys/class/drm/card0/device/gpu_busy_percent`` when available,
    falling back to ``0.0`` otherwise.

    Usage::

        monitor = SystemMonitor()
        monitor.tick()          # call once per frame
        metrics = monitor.snapshot()
        print(metrics.cpu_percent, metrics.fps)
    """

    _GPU_BUSY_PATH = "/sys/class/drm/card0/device/gpu_busy_percent"

    def __init__(self) -> None:
        self._prev_idle: float = 0.0
        self._prev_total: float = 0.0
        self._frame_times: list[float] = []
        self._dropped_frames: int = 0
        self._last_tick: float = 0.0

    # ------------------------------------------------------------------
    # CPU
    # ------------------------------------------------------------------

    def _read_cpu_percent(self) -> float:
        """Return current CPU usage as a percentage (0–100).

        Reads ``/proc/stat`` on Linux; returns ``0.0`` on other
        platforms or on read failure.
        """
        try:
            with open("/proc/stat", "r") as f:
                line = f.readline()  # first line: aggregated CPU
        except OSError:
            return 0.0

        parts = line.split()
        if len(parts) < 5 or parts[0] != "cpu":
            return 0.0

        values = [float(v) for v in parts[1:]]
        idle = values[3]
        total = sum(values)

        diff_idle = idle - self._prev_idle
        diff_total = total - self._prev_total
        self._prev_idle = idle
        self._prev_total = total

        if diff_total <= 0:
            return 0.0
        return round((1.0 - diff_idle / diff_total) * 100.0, 1)

    # ------------------------------------------------------------------
    # GPU
    # ------------------------------------------------------------------

    def _read_gpu_percent(self) -> float:
        """Return current GPU busy percentage (0–100).

        Reads the sysfs node exposed by some Linux DRM drivers.  Falls
        back to ``0.0`` when the file is missing or unreadable.
        """
        if not os.path.isfile(self._GPU_BUSY_PATH):
            return 0.0
        try:
            with open(self._GPU_BUSY_PATH, "r") as f:
                return float(f.read().strip())
        except (OSError, ValueError):
            return 0.0

    # ------------------------------------------------------------------
    # FPS tracking
    # ------------------------------------------------------------------

    def tick(self) -> None:
        """Record a frame timestamp for FPS calculation.

        Call this method once per rendered/processed frame.
        """
        now = time.monotonic()
        self._frame_times.append(now)
        # Keep only the last 120 frame timestamps (~2 s at 60 fps).
        if len(self._frame_times) > 120:
            self._frame_times = self._frame_times[-120:]
        self._last_tick = now

    def record_dropped_frame(self) -> None:
        """Increment the dropped-frame counter by one."""
        self._dropped_frames += 1

    def _compute_fps(self) -> float:
        """Return the average FPS over the recent frame window."""
        if len(self._frame_times) < 2:
            return 0.0
        elapsed = self._frame_times[-1] - self._frame_times[0]
        if elapsed <= 0:
            return 0.0
        return round((len(self._frame_times) - 1) / elapsed, 1)

    def _compute_latency(self) -> float:
        """Return the average frame interval in milliseconds."""
        fps = self._compute_fps()
        if fps <= 0:
            return 0.0
        return round(1000.0 / fps, 1)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def snapshot(self) -> SystemMetrics:
        """Collect and return a current metrics snapshot."""
        return SystemMetrics(
            cpu_percent=self._read_cpu_percent(),
            gpu_percent=self._read_gpu_percent(),
            fps=self._compute_fps(),
            latency_ms=self._compute_latency(),
            dropped_frames=self._dropped_frames,
        )
