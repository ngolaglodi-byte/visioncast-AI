/// @file control_room.cpp
/// @brief ControlRoom implementation — video source listing, selection,
///        and engine start / stop.

#include "visioncast_ui/control_room.h"

#include <QLabel>
#include <QListWidget>
#include <QPushButton>
#include <QVBoxLayout>

namespace visioncast_ui {

ControlRoom::ControlRoom(QWidget* parent)
    : QWidget(parent) {
    auto* layout = new QVBoxLayout(this);

    // --- Source list ---
    auto* listLabel = new QLabel("Video Sources:", this);
    layout->addWidget(listLabel);

    sourceList_ = new QListWidget(this);
    sourceList_->setSelectionMode(QAbstractItemView::SingleSelection);
    layout->addWidget(sourceList_);

    // --- Start / Stop button ---
    startButton_ = new QPushButton("Start Engine", this);
    startButton_->setEnabled(false);
    layout->addWidget(startButton_);

    // --- Status label ---
    statusLabel_ = new QLabel("Engine stopped", this);
    statusLabel_->setStyleSheet("color: grey;");
    layout->addWidget(statusLabel_);

    setLayout(layout);

    // Connections
    connect(sourceList_, &QListWidget::currentRowChanged,
            this, &ControlRoom::onSourceClicked);
    connect(startButton_, &QPushButton::clicked,
            this, &ControlRoom::onStartStopClicked);
}

// ---- Public API -----------------------------------------------------

void ControlRoom::setSources(const std::vector<VideoSourceInfo>& sources) {
    sources_ = sources;
    sourceList_->clear();
    for (const auto& src : sources_) {
        sourceList_->addItem(src.name + "  [" + src.deviceType + "]");
    }
    updateButtonState();
}

void ControlRoom::addSource(const VideoSourceInfo& source) {
    sources_.push_back(source);
    sourceList_->addItem(source.name + "  [" + source.deviceType + "]");
    updateButtonState();
}

void ControlRoom::clearSources() {
    sources_.clear();
    sourceList_->clear();
    updateButtonState();
}

VideoSourceInfo ControlRoom::selectedSource() const {
    int row = sourceList_->currentRow();
    if (row >= 0 && row < static_cast<int>(sources_.size())) {
        return sources_[static_cast<size_t>(row)];
    }
    return VideoSourceInfo{};
}

bool ControlRoom::isEngineRunning() const {
    return engineRunning_;
}

// ---- Private slots --------------------------------------------------

void ControlRoom::onSourceClicked() {
    auto src = selectedSource();
    if (!src.name.isEmpty()) {
        emit sourceSelected(src.name);
    }
    updateButtonState();
}

void ControlRoom::onStartStopClicked() {
    if (engineRunning_) {
        engineRunning_ = false;
        statusLabel_->setText("Engine stopped");
        statusLabel_->setStyleSheet("color: grey;");
        emit engineStopRequested();
    } else {
        auto src = selectedSource();
        if (src.name.isEmpty()) {
            return;
        }
        engineRunning_ = true;
        statusLabel_->setText("Engine running — " + src.name);
        statusLabel_->setStyleSheet("color: green;");
        emit engineStartRequested(src.name);
    }
    updateButtonState();
}

// ---- Helpers --------------------------------------------------------

void ControlRoom::updateButtonState() {
    if (engineRunning_) {
        startButton_->setEnabled(true);
        startButton_->setText("Stop Engine");
    } else {
        bool hasSelection = sourceList_->currentRow() >= 0;
        startButton_->setEnabled(hasSelection);
        startButton_->setText("Start Engine");
    }
}

} // namespace visioncast_ui
