#pragma once

/// @file output_config.h
/// @brief Output device and encoder configuration panel.

#include <QWidget>
#include <QString>

class QComboBox;
class QPushButton;

namespace visioncast_ui {

/// Output settings structure.
struct OutputSettings {
    QString device;
    QString resolution;
    double frameRate = 25.0;
    QString format;
    int     deviceIndex = 0;     ///< Index within the back-end (from DeviceConfig).
    QString backendType;         ///< Back-end tag: "DeckLink", "AJA", "Magewell", "NDI", "Virtual".
};

/// Per-entry metadata stored in deviceCombo_ via QVariant.
///
/// Each combo item carries a DeviceEntry so that the correct SDK
/// device can be opened when the selection changes.
struct DeviceEntry {
    QString backendType;   ///< One of "DeckLink", "AJA", "Magewell", "NDI", "Virtual".
    int     deviceIndex = 0;
};

/// Configuration panel for broadcast output devices and encoding settings.
class OutputConfig : public QWidget {
    Q_OBJECT

public:
    explicit OutputConfig(QWidget* parent = nullptr);

    /// Repopulate deviceCombo_ with real hardware names from the SDK.
    void refreshDevices();
    OutputSettings getCurrentSettings() const;

signals:
    void settingsChanged(const OutputSettings& settings);

private:
    QComboBox* deviceCombo_ = nullptr;
    QComboBox* resolutionCombo_ = nullptr;
    QComboBox* frameRateCombo_ = nullptr;
    QComboBox* formatCombo_ = nullptr;
    QPushButton* applyButton_ = nullptr;
};

} // namespace visioncast_ui

Q_DECLARE_METATYPE(visioncast_ui::DeviceEntry)
