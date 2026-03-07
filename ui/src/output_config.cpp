/// @file output_config.cpp
/// @brief OutputConfig implementation.

#include "visioncast_ui/output_config.h"

#include <QComboBox>
#include <QFormLayout>
#include <QPushButton>
#include <QVariant>

#include "visioncast_sdk/decklink_device.h"
#include "visioncast_sdk/aja_device.h"
#include "visioncast_sdk/magewell_device.h"
#include "visioncast_sdk/ndi_device.h"

namespace visioncast_ui {

OutputConfig::OutputConfig(QWidget* parent)
    : QWidget(parent) {
    auto* layout = new QFormLayout(this);

    deviceCombo_ = new QComboBox(this);

    resolutionCombo_ = new QComboBox(this);
    resolutionCombo_->addItems({"1920x1080 (1080p)", "3840x2160 (4K UHD)"});

    frameRateCombo_ = new QComboBox(this);
    frameRateCombo_->addItems({"23.98", "25", "29.97", "50", "59.94"});

    formatCombo_ = new QComboBox(this);
    formatCombo_->addItems({"SDI", "HDMI", "NDI", "SRT"});

    applyButton_ = new QPushButton("Apply", this);

    layout->addRow("Device:", deviceCombo_);
    layout->addRow("Resolution:", resolutionCombo_);
    layout->addRow("Frame Rate:", frameRateCombo_);
    layout->addRow("Output Format:", formatCombo_);
    layout->addRow(applyButton_);

    connect(applyButton_, &QPushButton::clicked, this, [this]() {
        emit settingsChanged(getCurrentSettings());
    });

    setLayout(layout);

    refreshDevices();
}

void OutputConfig::refreshDevices() {
    deviceCombo_->clear();

    auto addEntries = [this](const std::vector<DeviceConfig>& devices,
                             const QString& backendType) {
        for (const auto& cfg : devices) {
            const QString name = QString::fromStdString(cfg.name);
            DeviceEntry entry{backendType, cfg.deviceIndex};
            deviceCombo_->addItem(name, QVariant::fromValue(entry));
        }
    };

#if defined(HAS_DECKLINK)
    addEntries(DeckLinkDevice::enumerateDevices(), QStringLiteral("DeckLink"));
#endif

#if defined(HAS_AJA)
    addEntries(AJADevice::enumerateDevices(), QStringLiteral("AJA"));
#endif

#if defined(HAS_MAGEWELL)
    addEntries(MagewellDevice::enumerateDevices(), QStringLiteral("Magewell"));
#endif

#if defined(HAS_NDI)
    addEntries(NDIDevice::discoverSources(), QStringLiteral("NDI"));
#endif

    // Always provide a software Virtual fallback.
    DeviceEntry virtualEntry{QStringLiteral("Virtual"), 0};
    deviceCombo_->addItem(QStringLiteral("Virtual"), QVariant::fromValue(virtualEntry));
}

OutputSettings OutputConfig::getCurrentSettings() const {
    OutputSettings settings;
    settings.device = deviceCombo_->currentText();
    settings.resolution = resolutionCombo_->currentText();
    settings.frameRate = frameRateCombo_->currentText().toDouble();
    settings.format = formatCombo_->currentText();

    if (deviceCombo_->currentIndex() >= 0) {
        const auto entry =
            deviceCombo_->itemData(deviceCombo_->currentIndex()).value<DeviceEntry>();
        settings.deviceIndex = entry.deviceIndex;
        settings.backendType = entry.backendType;
    }

    return settings;
}

} // namespace visioncast_ui
