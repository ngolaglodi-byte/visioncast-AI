#pragma once

/// @file device_scanner.h
/// @brief Aggregates hardware device enumeration across all SDK back-ends.
///
/// scanAllDevices() queries DeckLink, AJA, Magewell and NDI (when the
/// corresponding vendor SDK is compiled in) and returns a flat list of
/// VideoSourceInfo structs suitable for ControlRoom::setSources().

#include "visioncast_ui/control_room.h"

#include <vector>

namespace visioncast_ui {

/// Query all compiled-in SDK back-ends and return a unified source list.
///
/// - DeckLink sources are returned by DeckLinkDevice::enumerateDevices()
/// - AJA sources are returned by AJADevice::enumerateDevices()
/// - Magewell sources are returned by MagewellDevice::enumerateDevices()
/// - NDI sources are returned by NDIDevice::discoverSources()
///
/// If a vendor SDK is not compiled in, that back-end is skipped
/// gracefully.  A "Virtual" fallback entry is always appended last.
std::vector<VideoSourceInfo> scanAllDevices();

} // namespace visioncast_ui
