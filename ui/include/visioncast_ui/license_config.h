#pragma once

/// @file license_config.h
/// @brief Secure configuration loader for license environment variables.

#include <QString>

namespace visioncast_ui {

/// Loads LICENSE_API_URL and LICENSE_API_KEY from environment variables.
/// If a required variable is missing the application must display an error
/// and refuse to start.
class LicenseConfig {
public:
    /// Attempt to load configuration from environment variables.
    /// @return true if both LICENSE_API_URL and LICENSE_API_KEY are set.
    static bool load();

    /// @return The license API base URL.
    static QString apiUrl();

    /// @return The license API key (bearer / anon key).
    static QString apiKey();

    /// @return true when both required variables have been loaded.
    static bool isValid();

    /// @return A human-readable error describing which variable is missing.
    static QString errorMessage();

private:
    static QString apiUrl_;
    static QString apiKey_;
    static bool    loaded_;
};

} // namespace visioncast_ui
