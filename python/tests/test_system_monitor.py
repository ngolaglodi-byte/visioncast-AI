"""Unit tests for the VisionCast system monitoring module.

Validates that:
- The SystemMonitor class and SystemMetrics dataclass exist and are importable,
- SystemMetrics exposes the expected fields and serializes to dict,
- SystemMonitor.tick() records frame timestamps for FPS calculation,
- SystemMonitor.snapshot() returns a SystemMetrics instance,
- SystemMonitor.record_dropped_frame() increments the counter,
- The monitoring __init__.py exports SystemMonitor,
- The ipc/__init__.py exports LogMessage and Heartbeat.
"""

import os
import sys

# Ensure the python/ directory is importable.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

MONITORING_DIR = os.path.join(PROJECT_ROOT, "python", "monitoring")


# =====================================================================
# File structure tests
# =====================================================================

class TestMonitoringModuleStructure:
    """Verify the monitoring module files exist."""

    def test_monitoring_init_exists(self):
        assert os.path.isfile(os.path.join(MONITORING_DIR, "__init__.py"))

    def test_system_monitor_exists(self):
        assert os.path.isfile(os.path.join(MONITORING_DIR, "system_monitor.py"))


# =====================================================================
# SystemMetrics dataclass tests
# =====================================================================

class TestSystemMetrics:
    """Validate the SystemMetrics dataclass."""

    def test_importable(self):
        from monitoring.system_monitor import SystemMetrics
        assert SystemMetrics is not None

    def test_default_values(self):
        from monitoring.system_monitor import SystemMetrics
        m = SystemMetrics()
        assert m.cpu_percent == 0.0
        assert m.gpu_percent == 0.0
        assert m.fps == 0.0
        assert m.latency_ms == 0.0
        assert m.dropped_frames == 0

    def test_custom_values(self):
        from monitoring.system_monitor import SystemMetrics
        m = SystemMetrics(cpu_percent=45.2, gpu_percent=80.0, fps=60.0,
                          latency_ms=16.7, dropped_frames=3)
        assert m.cpu_percent == 45.2
        assert m.gpu_percent == 80.0
        assert m.fps == 60.0
        assert m.latency_ms == 16.7
        assert m.dropped_frames == 3

    def test_to_dict(self):
        from monitoring.system_monitor import SystemMetrics
        m = SystemMetrics(cpu_percent=10.0, fps=30.0)
        d = m.to_dict()
        assert d["cpu_percent"] == 10.0
        assert d["fps"] == 30.0
        assert "gpu_percent" in d
        assert "latency_ms" in d
        assert "dropped_frames" in d


# =====================================================================
# SystemMonitor class tests
# =====================================================================

class TestSystemMonitor:
    """Validate the SystemMonitor class."""

    def test_importable(self):
        from monitoring.system_monitor import SystemMonitor
        assert SystemMonitor is not None

    def test_importable_from_package(self):
        from monitoring import SystemMonitor
        assert SystemMonitor is not None

    def test_snapshot_returns_metrics(self):
        from monitoring.system_monitor import SystemMonitor, SystemMetrics
        monitor = SystemMonitor()
        metrics = monitor.snapshot()
        assert isinstance(metrics, SystemMetrics)

    def test_tick_updates_fps(self):
        from unittest.mock import patch
        from monitoring.system_monitor import SystemMonitor
        monitor = SystemMonitor()
        # Mock time.monotonic to produce deterministic frame timestamps
        # Simulate 20 frames at exactly 100 fps (0.01s apart)
        fake_time = 1000.0
        with patch("time.monotonic") as mock_time:
            for i in range(20):
                mock_time.return_value = fake_time + i * 0.01
                monitor.tick()
        metrics = monitor.snapshot()
        assert metrics.fps > 0

    def test_dropped_frame_counter(self):
        from monitoring.system_monitor import SystemMonitor
        monitor = SystemMonitor()
        assert monitor.snapshot().dropped_frames == 0
        monitor.record_dropped_frame()
        monitor.record_dropped_frame()
        assert monitor.snapshot().dropped_frames == 2

    def test_cpu_percent_is_non_negative(self):
        from monitoring.system_monitor import SystemMonitor
        monitor = SystemMonitor()
        metrics = monitor.snapshot()
        assert metrics.cpu_percent >= 0.0

    def test_gpu_percent_is_non_negative(self):
        from monitoring.system_monitor import SystemMonitor
        monitor = SystemMonitor()
        metrics = monitor.snapshot()
        assert metrics.gpu_percent >= 0.0

    def test_latency_from_fps(self):
        from unittest.mock import patch
        from monitoring.system_monitor import SystemMonitor
        monitor = SystemMonitor()
        # Mock time.monotonic to simulate known frame rate
        fake_time = 1000.0
        with patch("time.monotonic") as mock_time:
            for i in range(30):
                mock_time.return_value = fake_time + i * 0.01
                monitor.tick()
        metrics = monitor.snapshot()
        if metrics.fps > 0:
            assert metrics.latency_ms > 0


# =====================================================================
# IPC exports tests
# =====================================================================

class TestIpcExports:
    """Verify LogMessage and Heartbeat are exported from ipc package."""

    def test_log_message_exported(self):
        from ipc import LogMessage
        assert LogMessage is not None

    def test_heartbeat_exported(self):
        from ipc import Heartbeat
        assert Heartbeat is not None
