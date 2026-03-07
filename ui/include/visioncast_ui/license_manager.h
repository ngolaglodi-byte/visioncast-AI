#pragma once

/// @file license_manager.h
/// @brief License management with offline grace mode, encrypted storage,
///        and environment-variable-based configuration.
///
/// VisionCast-AI — Licence officielle Prestige Technologie Company,
/// développée par Glody Dimputu Ngola.

#include <QObject>
#include <QString>
#include <QDateTime>
#include <QJsonObject>

class QNetworkAccessManager;
class QNetworkReply;

namespace visioncast_ui {

class LicenseStorage;

/// Manages license activation, validation, and status checks against a
/// remote licensing API.  Supports offline grace mode (TTL) and blocks
/// the application when the licence is invalid, expired, or suspended.
class LicenseManager : public QObject {
    Q_OBJECT

public:
    /// Current state of the license.
    enum class LicenseStatus {
        Unknown,    ///< Status has not been checked yet.
        Valid,      ///< License is active and valid.
        Expired,    ///< License has expired.
        Invalid,    ///< License key is invalid.
        Suspended   ///< License has been suspended.
    };
    Q_ENUM(LicenseStatus)

    /// Default offline grace period in days.
    static constexpr int kOfflineGraceDays = 7;

    /// Path to the encrypted local licence file.
    static constexpr const char* kLicenseDatPath = "license.dat";

    explicit LicenseManager(QObject* parent = nullptr);

    // ── Configuration ──────────────────────────────────────────────

    /// Load API settings and cached license key from a JSON file.
    /// @return true if the file was parsed successfully.
    bool loadConfig(const QString& configPath);

    /// Persist the current license key back to the configuration file.
    bool saveConfig(const QString& configPath) const;

    /// Load API URL and key from environment variables
    /// (LICENSE_API_URL, LICENSE_API_KEY).
    bool loadFromEnvironment();

    void setApiUrl(const QString& url);
    QString apiUrl() const;

    void setApiKey(const QString& key);

    // ── Machine Identification ─────────────────────────────────────

    /// Return a persistent, platform-specific machine identifier.
    QString machineId() const;

    // ── License Operations ─────────────────────────────────────────

    /// Activate a license key on this machine.
    void activateKey(const QString& licenseKey);

    /// Validate that a previously-activated key is still valid.
    void validateKey(const QString& licenseKey);

    /// Deactivate the key on this machine, freeing a seat.
    void deactivateKey(const QString& licenseKey);

    /// Query the current status of a license key.
    void checkStatus(const QString& licenseKey);

    // ── Offline Grace Mode ─────────────────────────────────────────

    /// Try to authorize via the locally stored offline grace period.
    /// @return true if the current date is within the offline window.
    bool tryOfflineGrace();

    /// @return The offline-valid-until deadline from the local store.
    QDateTime offlineValidUntil() const;

    // ── Blocking Check ─────────────────────────────────────────────

    /// @return true if the current status should block application start.
    bool shouldBlockApplication() const;

    /// @return A user-facing message explaining why the app is blocked.
    QString blockReason() const;

    // ── Current State ──────────────────────────────────────────────

    LicenseStatus status() const;
    QString licenseKey() const;
    bool isLicensed() const;

signals:
    /// Emitted after a successful key activation.
    void activationSucceeded(const QString& message);
    /// Emitted when activation fails.
    void activationFailed(const QString& error);

    /// Emitted after a validation request completes.
    void validationCompleted(bool valid, const QString& message);

    /// Emitted after a successful deactivation.
    void deactivationSucceeded(const QString& message);
    /// Emitted when deactivation fails.
    void deactivationFailed(const QString& error);

    /// Emitted after a status-check request completes.
    void statusChecked(LicenseStatus status, const QString& message);

    /// Emitted on any transport-level error (timeout, DNS, TLS …).
    void networkError(const QString& error);

    /// Emitted when the licence state requires the application to quit.
    void licenseBlocked(const QString& reason);

    /// Emitted when offline grace mode has been activated.
    void offlineModeActivated();

private slots:
    void onReplyFinished(QNetworkReply* reply);

private:
    void sendRequest(const QJsonObject& payload, const QString& action);
    static QString generateMachineId();

    /// Refresh the offline deadline after a successful server validation.
    void refreshOfflineDeadline();

    /// Persist the encrypted licence to disk.
    void persistLicenseDat() const;

    QString apiUrl_;
    QString apiKey_;
    QString licenseKey_;
    QString machineId_;
    LicenseStatus status_ = LicenseStatus::Unknown;

    QNetworkAccessManager* networkManager_ = nullptr;
    QString pendingAction_;

    QDateTime offlineValidUntil_;
    LicenseStorage* storage_ = nullptr;
};

} // namespace visioncast_ui
