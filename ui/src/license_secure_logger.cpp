/// @file license_secure_logger.cpp
/// @brief LicenseSecureLogger implementation — writes to license_secure.log.

#include "visioncast_ui/license_secure_logger.h"

#include <QDateTime>
#include <QFile>
#include <QMutex>
#include <QTextStream>

namespace visioncast_ui {

static QMutex s_logMutex;

void LicenseSecureLogger::logValidation(const QString& status) {
    write(QStringLiteral("VALIDATION"), QStringLiteral("status=") + status);
}

void LicenseSecureLogger::logError(const QString& error) {
    write(QStringLiteral("ERROR"), error);
}

void LicenseSecureLogger::logOfflineModeEnabled() {
    write(QStringLiteral("OFFLINE MODE ENABLED"), QString());
}

void LicenseSecureLogger::logInfo(const QString& message) {
    write(QStringLiteral("INFO"), message);
}

void LicenseSecureLogger::write(const QString& category,
                                const QString& message) {
    QMutexLocker lock(&s_logMutex);
    QFile file(QStringLiteral("license_secure.log"));
    if (!file.open(QIODevice::Append | QIODevice::Text))
        return;
    QTextStream out(&file);
    out << "[" << timestamp() << "] " << category;
    if (!message.isEmpty())
        out << " - " << message;
    out << "\n";
}

QString LicenseSecureLogger::timestamp() {
    return QDateTime::currentDateTime().toString(
        QStringLiteral("yyyy-MM-dd HH:mm:ss"));
}

} // namespace visioncast_ui
