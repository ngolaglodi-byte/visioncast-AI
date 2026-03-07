/// @file license_config.cpp
/// @brief LicenseConfig implementation — reads environment variables.

#include "visioncast_ui/license_config.h"

#include <QProcessEnvironment>

namespace visioncast_ui {

// Static member definitions.
QString LicenseConfig::apiUrl_;
QString LicenseConfig::apiKey_;
bool    LicenseConfig::loaded_ = false;

bool LicenseConfig::load() {
    const auto env = QProcessEnvironment::systemEnvironment();
    apiUrl_ = env.value(QStringLiteral("LICENSE_API_URL"));
    apiKey_ = env.value(QStringLiteral("LICENSE_API_KEY"));
    loaded_ = !apiUrl_.isEmpty() && !apiKey_.isEmpty();
    return loaded_;
}

QString LicenseConfig::apiUrl()  { return apiUrl_; }
QString LicenseConfig::apiKey()  { return apiKey_; }
bool    LicenseConfig::isValid() { return loaded_; }

QString LicenseConfig::errorMessage() {
    if (apiUrl_.isEmpty() && apiKey_.isEmpty())
        return QStringLiteral(
            "LICENSE_API_URL and LICENSE_API_KEY environment variables "
            "are not set. VisionCast-AI cannot start.");
    if (apiUrl_.isEmpty())
        return QStringLiteral(
            "LICENSE_API_URL environment variable is not set. "
            "VisionCast-AI cannot start.");
    return QStringLiteral(
        "LICENSE_API_KEY environment variable is not set. "
        "VisionCast-AI cannot start.");
}

} // namespace visioncast_ui
