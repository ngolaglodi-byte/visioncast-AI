/// @file device_scanner.cpp
/// @brief Aggregates SDK device enumeration into VideoSourceInfo structs.

#include "visioncast_ui/device_scanner.h"

#include "visioncast_sdk/decklink_device.h"
#include "visioncast_sdk/aja_device.h"
#include "visioncast_sdk/magewell_device.h"
#include "visioncast_sdk/ndi_device.h"

namespace visioncast_ui {

std::vector<VideoSourceInfo> scanAllDevices() {
    std::vector<VideoSourceInfo> sources;

    auto appendDevices = [&sources](const std::vector<DeviceConfig>& devices,
                                    const QString& backendType) {
        for (const auto& cfg : devices) {
            VideoSourceInfo info;
            info.name        = QString::fromStdString(cfg.name);
            info.deviceType  = backendType;
            info.deviceIndex = cfg.deviceIndex;
            sources.push_back(std::move(info));
        }
    };

#if defined(HAS_DECKLINK)
    appendDevices(DeckLinkDevice::enumerateDevices(), QStringLiteral("DeckLink"));
#endif

#if defined(HAS_AJA)
    appendDevices(AJADevice::enumerateDevices(), QStringLiteral("AJA"));
#endif

#if defined(HAS_MAGEWELL)
    appendDevices(MagewellDevice::enumerateDevices(), QStringLiteral("Magewell"));
#endif

#if defined(HAS_NDI)
    appendDevices(NDIDevice::discoverSources(), QStringLiteral("NDI"));
#endif

    // Always provide a software Virtual fallback.
    VideoSourceInfo virtualSource;
    virtualSource.name       = QStringLiteral("Virtual");
    virtualSource.deviceType = QStringLiteral("Virtual");
    virtualSource.deviceIndex = 0;
    sources.push_back(std::move(virtualSource));

    return sources;
}

} // namespace visioncast_ui
