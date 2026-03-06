#pragma once

/// @file control_room.h
/// @brief VisionCast Control Room — video source listing, selection,
///        and engine start/stop.

#include <QWidget>

#include <vector>

class QListWidget;
class QPushButton;
class QLabel;

namespace visioncast_ui {

/// Describes a video source available for capture.
struct VideoSourceInfo {
    QString name;        ///< Human-readable source name (e.g. "Camera 1").
    QString deviceType;  ///< Device type (e.g. "DeckLink", "NDI", "Webcam").
    int     deviceIndex = 0; ///< Device index for the capture back-end.
};

/// Control Room panel: lists video sources, allows selection, and
/// starts / stops the video engine.
class ControlRoom : public QWidget {
    Q_OBJECT

public:
    explicit ControlRoom(QWidget* parent = nullptr);

    /// Replace the current source list with @p sources.
    void setSources(const std::vector<VideoSourceInfo>& sources);

    /// Append a single source to the list.
    void addSource(const VideoSourceInfo& source);

    /// Remove all sources from the list.
    void clearSources();

    /// Return the currently selected source (empty name if none).
    VideoSourceInfo selectedSource() const;

    /// Return true when the engine is reported as running.
    bool isEngineRunning() const;

signals:
    /// Emitted when the user selects a different video source.
    void sourceSelected(const QString& sourceName);

    /// Emitted when the user clicks the Start Engine button.
    void engineStartRequested(const QString& sourceName);

    /// Emitted when the user clicks the Stop Engine button.
    void engineStopRequested();

private slots:
    void onSourceClicked();
    void onStartStopClicked();

private:
    QListWidget* sourceList_  = nullptr;
    QPushButton* startButton_ = nullptr;
    QLabel*      statusLabel_ = nullptr;
    bool         engineRunning_ = false;

    std::vector<VideoSourceInfo> sources_;

    void updateButtonState();
};

} // namespace visioncast_ui
