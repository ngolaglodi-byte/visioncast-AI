"""Unit tests for the VisionCast Control Room UI component.

Validates that:
- The control_room header and source files exist,
- The header declares the ControlRoom class inheriting from QWidget,
- The header declares the VideoSourceInfo struct,
- The source file includes the corresponding header,
- The CMakeLists.txt includes the new source file,
- The MainWindow integrates the ControlRoom panel.
"""

import os
import re
import sys

# Ensure the python/ directory is importable.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Resolve project root (two levels up from tests/).
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

UI_INCLUDE = os.path.join(PROJECT_ROOT, "ui", "include", "visioncast_ui")
UI_SRC = os.path.join(PROJECT_ROOT, "ui", "src")
UI_CMAKE = os.path.join(PROJECT_ROOT, "ui", "CMakeLists.txt")


def _read(path):
    assert os.path.isfile(path), f"File not found: {path}"
    with open(path, "r") as f:
        return f.read()


# =====================================================================
# Header file tests
# =====================================================================

class TestControlRoomHeader:
    """Validate the control_room.h header."""

    def test_header_exists(self):
        path = os.path.join(UI_INCLUDE, "control_room.h")
        assert os.path.isfile(path)

    def test_header_has_pragma_once(self):
        text = _read(os.path.join(UI_INCLUDE, "control_room.h"))
        assert "#pragma once" in text

    def test_header_includes_qwidget(self):
        text = _read(os.path.join(UI_INCLUDE, "control_room.h"))
        assert "<QWidget>" in text

    def test_header_declares_video_source_info(self):
        text = _read(os.path.join(UI_INCLUDE, "control_room.h"))
        assert "VideoSourceInfo" in text

    def test_video_source_info_has_name(self):
        text = _read(os.path.join(UI_INCLUDE, "control_room.h"))
        assert re.search(r"QString\s+name", text)

    def test_video_source_info_has_device_type(self):
        text = _read(os.path.join(UI_INCLUDE, "control_room.h"))
        assert re.search(r"QString\s+deviceType", text)

    def test_control_room_inherits_qwidget(self):
        text = _read(os.path.join(UI_INCLUDE, "control_room.h"))
        pattern = r"class\s+ControlRoom\s*:\s*public\s+QWidget"
        assert re.search(pattern, text)

    def test_has_set_sources(self):
        text = _read(os.path.join(UI_INCLUDE, "control_room.h"))
        assert "setSources(" in text

    def test_has_add_source(self):
        text = _read(os.path.join(UI_INCLUDE, "control_room.h"))
        assert "addSource(" in text

    def test_has_clear_sources(self):
        text = _read(os.path.join(UI_INCLUDE, "control_room.h"))
        assert "clearSources()" in text

    def test_has_selected_source(self):
        text = _read(os.path.join(UI_INCLUDE, "control_room.h"))
        assert "selectedSource()" in text

    def test_has_source_selected_signal(self):
        text = _read(os.path.join(UI_INCLUDE, "control_room.h"))
        assert "sourceSelected(" in text

    def test_has_engine_start_signal(self):
        text = _read(os.path.join(UI_INCLUDE, "control_room.h"))
        assert "engineStartRequested(" in text

    def test_has_engine_stop_signal(self):
        text = _read(os.path.join(UI_INCLUDE, "control_room.h"))
        assert "engineStopRequested()" in text

    def test_has_is_engine_running(self):
        text = _read(os.path.join(UI_INCLUDE, "control_room.h"))
        assert "isEngineRunning()" in text


# =====================================================================
# Source file tests
# =====================================================================

class TestControlRoomSource:
    """Validate the control_room.cpp source."""

    def test_source_exists(self):
        path = os.path.join(UI_SRC, "control_room.cpp")
        assert os.path.isfile(path)

    def test_source_includes_header(self):
        text = _read(os.path.join(UI_SRC, "control_room.cpp"))
        assert "visioncast_ui/control_room.h" in text

    def test_source_has_set_sources(self):
        text = _read(os.path.join(UI_SRC, "control_room.cpp"))
        assert "ControlRoom::setSources" in text

    def test_source_has_add_source(self):
        text = _read(os.path.join(UI_SRC, "control_room.cpp"))
        assert "ControlRoom::addSource" in text

    def test_source_has_clear_sources(self):
        text = _read(os.path.join(UI_SRC, "control_room.cpp"))
        assert "ControlRoom::clearSources" in text

    def test_source_has_selected_source(self):
        text = _read(os.path.join(UI_SRC, "control_room.cpp"))
        assert "ControlRoom::selectedSource" in text

    def test_source_has_start_stop_handler(self):
        text = _read(os.path.join(UI_SRC, "control_room.cpp"))
        assert "ControlRoom::onStartStopClicked" in text


# =====================================================================
# CMakeLists.txt integration
# =====================================================================

class TestControlRoomCMake:
    """Verify ui/CMakeLists.txt includes the new source file."""

    def test_control_room_in_cmake(self):
        text = _read(UI_CMAKE)
        assert "control_room.cpp" in text


# =====================================================================
# MainWindow integration
# =====================================================================

class TestMainWindowIntegration:
    """Verify the MainWindow integrates the ControlRoom panel."""

    def test_main_window_header_has_control_room(self):
        text = _read(os.path.join(UI_INCLUDE, "main_window.h"))
        assert "ControlRoom" in text

    def test_main_window_source_includes_control_room(self):
        text = _read(os.path.join(UI_SRC, "main_window.cpp"))
        assert "control_room.h" in text

    def test_main_window_creates_control_room_dock(self):
        text = _read(os.path.join(UI_SRC, "main_window.cpp"))
        assert "Control Room" in text

    def test_main_window_connects_engine_start(self):
        text = _read(os.path.join(UI_SRC, "main_window.cpp"))
        assert "engineStartRequested" in text

    def test_main_window_connects_engine_stop(self):
        text = _read(os.path.join(UI_SRC, "main_window.cpp"))
        assert "engineStopRequested" in text
