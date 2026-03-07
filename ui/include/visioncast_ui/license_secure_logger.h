#pragma once

/// @file license_secure_logger.h
/// @brief Secure logging for license operations — never logs the full key.

#include <QString>

namespace visioncast_ui {

/// Thread-safe logger that writes to license_secure.log.
/// The full license key is never written; only the first 4 characters are
/// shown followed by "****".
class LicenseSecureLogger {
public:
    /// Log a validation result.
    static void logValidation(const QString& status);

    /// Log an error condition.
    static void logError(const QString& error);

    /// Log that offline mode has been enabled.
    static void logOfflineModeEnabled();

    /// Log an informational message.
    static void logInfo(const QString& message);

private:
    static void write(const QString& category, const QString& message);
    static QString timestamp();
};

} // namespace visioncast_ui
