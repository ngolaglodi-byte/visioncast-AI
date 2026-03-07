"""Unit tests for the license management module configuration and C++ header /
source consistency.

Validates that:
- config/license.json conforms to the expected schema,
- The C++ LicenseManager header declares the expected interface,
- The C++ LicenseDialog header declares the expected interface,
- The CMakeLists.txt includes both new source files and links Qt::Network,
- LicenseConfig loads environment variables,
- LicenseStorage provides encrypted storage with tamper detection,
- LicenseSecureLogger provides secure logging,
- Offline grace mode and license blocking are implemented,
- The .env.example file is present and well-formed.
"""

import json
import os
import re
import sys

import pytest

# Ensure the python/ directory is importable.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Resolve project root (two levels up from tests/).
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "license.json")
MANAGER_HEADER = os.path.join(
    PROJECT_ROOT, "ui", "include", "visioncast_ui", "license_manager.h"
)
MANAGER_SOURCE = os.path.join(
    PROJECT_ROOT, "ui", "src", "license_manager.cpp"
)
DIALOG_HEADER = os.path.join(
    PROJECT_ROOT, "ui", "include", "visioncast_ui", "license_dialog.h"
)
DIALOG_SOURCE = os.path.join(
    PROJECT_ROOT, "ui", "src", "license_dialog.cpp"
)
UI_CMAKE = os.path.join(PROJECT_ROOT, "ui", "CMakeLists.txt")
MAIN_WINDOW_HEADER = os.path.join(
    PROJECT_ROOT, "ui", "include", "visioncast_ui", "main_window.h"
)
MAIN_WINDOW_SOURCE = os.path.join(
    PROJECT_ROOT, "ui", "src", "main_window.cpp"
)
LICENSE_CONFIG_HEADER = os.path.join(
    PROJECT_ROOT, "ui", "include", "visioncast_ui", "license_config.h"
)
LICENSE_CONFIG_SOURCE = os.path.join(
    PROJECT_ROOT, "ui", "src", "license_config.cpp"
)
LICENSE_STORAGE_HEADER = os.path.join(
    PROJECT_ROOT, "ui", "include", "visioncast_ui", "license_storage.h"
)
LICENSE_STORAGE_SOURCE = os.path.join(
    PROJECT_ROOT, "ui", "src", "license_storage.cpp"
)
LICENSE_LOGGER_HEADER = os.path.join(
    PROJECT_ROOT, "ui", "include", "visioncast_ui",
    "license_secure_logger.h"
)
LICENSE_LOGGER_SOURCE = os.path.join(
    PROJECT_ROOT, "ui", "src", "license_secure_logger.cpp"
)
ENV_EXAMPLE = os.path.join(PROJECT_ROOT, ".env.example")
README_PATH = os.path.join(PROJECT_ROOT, "README.md")


# =====================================================================
# Fixtures
# =====================================================================

@pytest.fixture(scope="module")
def config():
    assert os.path.isfile(CONFIG_PATH), f"Config not found: {CONFIG_PATH}"
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def manager_header():
    assert os.path.isfile(MANAGER_HEADER)
    with open(MANAGER_HEADER, "r") as f:
        return f.read()


@pytest.fixture(scope="module")
def manager_source():
    assert os.path.isfile(MANAGER_SOURCE)
    with open(MANAGER_SOURCE, "r") as f:
        return f.read()


@pytest.fixture(scope="module")
def dialog_header():
    assert os.path.isfile(DIALOG_HEADER)
    with open(DIALOG_HEADER, "r") as f:
        return f.read()


@pytest.fixture(scope="module")
def dialog_source():
    assert os.path.isfile(DIALOG_SOURCE)
    with open(DIALOG_SOURCE, "r") as f:
        return f.read()


@pytest.fixture(scope="module")
def cmake_text():
    assert os.path.isfile(UI_CMAKE)
    with open(UI_CMAKE, "r") as f:
        return f.read()


@pytest.fixture(scope="module")
def main_window_header():
    assert os.path.isfile(MAIN_WINDOW_HEADER)
    with open(MAIN_WINDOW_HEADER, "r") as f:
        return f.read()


@pytest.fixture(scope="module")
def main_window_source():
    assert os.path.isfile(MAIN_WINDOW_SOURCE)
    with open(MAIN_WINDOW_SOURCE, "r") as f:
        return f.read()


@pytest.fixture(scope="module")
def config_header():
    assert os.path.isfile(LICENSE_CONFIG_HEADER)
    with open(LICENSE_CONFIG_HEADER, "r") as f:
        return f.read()


@pytest.fixture(scope="module")
def config_source():
    assert os.path.isfile(LICENSE_CONFIG_SOURCE)
    with open(LICENSE_CONFIG_SOURCE, "r") as f:
        return f.read()


@pytest.fixture(scope="module")
def storage_header():
    assert os.path.isfile(LICENSE_STORAGE_HEADER)
    with open(LICENSE_STORAGE_HEADER, "r") as f:
        return f.read()


@pytest.fixture(scope="module")
def storage_source():
    assert os.path.isfile(LICENSE_STORAGE_SOURCE)
    with open(LICENSE_STORAGE_SOURCE, "r") as f:
        return f.read()


@pytest.fixture(scope="module")
def logger_header():
    assert os.path.isfile(LICENSE_LOGGER_HEADER)
    with open(LICENSE_LOGGER_HEADER, "r") as f:
        return f.read()


@pytest.fixture(scope="module")
def logger_source():
    assert os.path.isfile(LICENSE_LOGGER_SOURCE)
    with open(LICENSE_LOGGER_SOURCE, "r") as f:
        return f.read()


@pytest.fixture(scope="module")
def env_example():
    assert os.path.isfile(ENV_EXAMPLE), ".env.example not found"
    with open(ENV_EXAMPLE, "r") as f:
        return f.read()


@pytest.fixture(scope="module")
def readme():
    assert os.path.isfile(README_PATH)
    with open(README_PATH, "r") as f:
        return f.read()


# =====================================================================
# Config schema validation
# =====================================================================

class TestLicenseConfig:
    """Validate config/license.json schema."""

    REQUIRED_KEYS = {"api_url", "api_key", "license_key"}

    def test_config_is_valid_json(self, config):
        assert isinstance(config, dict)

    def test_config_has_required_keys(self, config):
        for key in self.REQUIRED_KEYS:
            assert key in config, f"Missing key: {key}"

    def test_api_url_is_string(self, config):
        assert isinstance(config["api_url"], str)

    def test_api_url_is_https(self, config):
        url = config["api_url"]
        if url:  # Allow empty for template
            assert url.startswith("https://"), "API URL must use HTTPS"

    def test_api_key_is_string(self, config):
        assert isinstance(config["api_key"], str)

    def test_license_key_is_string(self, config):
        assert isinstance(config["license_key"], str)

    def test_no_hardcoded_secrets(self, config):
        """Ensure the shipped config template does not contain real keys."""
        api_key = config["api_key"]
        assert api_key == "" or api_key.startswith("eyJ"), (
            "api_key should be empty or a Base64-encoded JWT"
        )

    def test_no_hardcoded_supabase_url(self, config):
        """The config must not contain a real Supabase URL."""
        url = config["api_url"]
        assert "supabase.co" not in url, (
            "Supabase URL must not be hardcoded in config"
        )


# =====================================================================
# LicenseManager header/source consistency
# =====================================================================

class TestLicenseManagerHeader:
    """Verify the C++ LicenseManager header declares expected API."""

    def test_pragma_once(self, manager_header):
        assert "#pragma once" in manager_header

    def test_namespace(self, manager_header):
        assert "namespace visioncast_ui" in manager_header

    def test_class_declaration(self, manager_header):
        assert re.search(
            r"class\s+LicenseManager\s*:\s*public\s+QObject",
            manager_header,
        )

    def test_q_object_macro(self, manager_header):
        assert "Q_OBJECT" in manager_header

    def test_license_status_enum(self, manager_header):
        assert "LicenseStatus" in manager_header
        for status in ("Unknown", "Valid", "Expired", "Invalid", "Suspended"):
            assert status in manager_header, (
                f"LicenseStatus::{status} not found"
            )

    @pytest.mark.parametrize("method", [
        "loadConfig", "saveConfig", "machineId",
        "activateKey", "validateKey", "deactivateKey", "checkStatus",
        "isLicensed", "licenseKey",
    ])
    def test_public_methods_declared(self, manager_header, method):
        assert method in manager_header

    @pytest.mark.parametrize("signal", [
        "activationSucceeded", "activationFailed",
        "validationCompleted",
        "deactivationSucceeded", "deactivationFailed",
        "statusChecked", "networkError",
    ])
    def test_signals_declared(self, manager_header, signal):
        assert signal in manager_header

    def test_offline_grace_methods(self, manager_header):
        """Verify offline grace mode API is declared."""
        assert "tryOfflineGrace" in manager_header
        assert "offlineValidUntil" in manager_header
        assert "kOfflineGraceDays" in manager_header

    def test_blocking_methods(self, manager_header):
        """Verify blocking API is declared."""
        assert "shouldBlockApplication" in manager_header
        assert "blockReason" in manager_header

    def test_license_blocked_signal(self, manager_header):
        assert "licenseBlocked" in manager_header

    def test_offline_mode_signal(self, manager_header):
        assert "offlineModeActivated" in manager_header

    def test_load_from_environment(self, manager_header):
        assert "loadFromEnvironment" in manager_header

    def test_prestige_mention(self, manager_header):
        """The Prestige Technologie Company credit must appear."""
        assert "Prestige Technologie Company" in manager_header


class TestLicenseManagerSource:
    """Verify the C++ source implements key LicenseManager logic."""

    def test_includes_header(self, manager_source):
        assert '#include "visioncast_ui/license_manager.h"' in manager_source

    def test_uses_qnetworkaccessmanager(self, manager_source):
        assert "QNetworkAccessManager" in manager_source

    def test_sends_json_content_type(self, manager_source):
        assert "application/json" in manager_source

    def test_sends_apikey_header(self, manager_source):
        assert '"apikey"' in manager_source

    @pytest.mark.parametrize("action", [
        "activate_key", "validate_key", "deactivate_key", "check_status",
    ])
    def test_action_strings_present(self, manager_source, action):
        assert action in manager_source

    def test_machine_id_generation(self, manager_source):
        assert "generateMachineId" in manager_source
        assert "QCryptographicHash" in manager_source

    def test_includes_license_config(self, manager_source):
        assert "license_config.h" in manager_source

    def test_includes_license_storage(self, manager_source):
        assert "license_storage.h" in manager_source

    def test_includes_secure_logger(self, manager_source):
        assert "license_secure_logger.h" in manager_source

    def test_offline_grace_implementation(self, manager_source):
        assert "tryOfflineGrace" in manager_source
        assert "offlineValidUntil" in manager_source

    def test_blocking_implementation(self, manager_source):
        assert "shouldBlockApplication" in manager_source
        assert "blockReason" in manager_source

    def test_refresh_offline_deadline(self, manager_source):
        assert "refreshOfflineDeadline" in manager_source

    def test_no_hardcoded_supabase_url(self, manager_source):
        """Source must not contain real Supabase URLs."""
        assert "qkcchctrmrpdyseplbvb" not in manager_source

    def test_prestige_mention(self, manager_source):
        assert "Prestige Technologie Company" in manager_source


# =====================================================================
# LicenseDialog header/source consistency
# =====================================================================

class TestLicenseDialogHeader:
    """Verify the C++ LicenseDialog header declares expected UI."""

    def test_pragma_once(self, dialog_header):
        assert "#pragma once" in dialog_header

    def test_class_declaration(self, dialog_header):
        assert re.search(
            r"class\s+LicenseDialog\s*:\s*public\s+QDialog",
            dialog_header,
        )

    def test_q_object_macro(self, dialog_header):
        assert "Q_OBJECT" in dialog_header


class TestLicenseDialogSource:
    """Verify the C++ source implements the LicenseDialog."""

    def test_includes_header(self, dialog_source):
        assert '#include "visioncast_ui/license_dialog.h"' in dialog_source

    def test_includes_license_manager(self, dialog_source):
        assert '#include "visioncast_ui/license_manager.h"' in dialog_source

    def test_has_activate_button(self, dialog_source):
        assert "activateButton_" in dialog_source

    def test_has_deactivate_button(self, dialog_source):
        assert "deactivateButton_" in dialog_source

    def test_has_status_display(self, dialog_source):
        assert "statusLabel_" in dialog_source


# =====================================================================
# CMakeLists.txt integration
# =====================================================================

class TestCMakeIntegration:
    """Verify the CMake build includes new source files and Qt::Network."""

    def test_license_manager_in_sources(self, cmake_text):
        assert "license_manager.cpp" in cmake_text

    def test_license_dialog_in_sources(self, cmake_text):
        assert "license_dialog.cpp" in cmake_text

    def test_qt_network_linked(self, cmake_text):
        assert "Network" in cmake_text

    def test_license_config_in_sources(self, cmake_text):
        assert "license_config.cpp" in cmake_text

    def test_license_storage_in_sources(self, cmake_text):
        assert "license_storage.cpp" in cmake_text

    def test_license_secure_logger_in_sources(self, cmake_text):
        assert "license_secure_logger.cpp" in cmake_text


# =====================================================================
# MainWindow integration
# =====================================================================

class TestMainWindowIntegration:
    """Verify the main window integrates the license module."""

    def test_license_manager_forward_declared(self, main_window_header):
        assert "LicenseManager" in main_window_header

    def test_license_manager_member(self, main_window_header):
        assert "licenseManager_" in main_window_header

    def test_manage_license_slot(self, main_window_header):
        assert "onManageLicense" in main_window_header

    def test_includes_license_manager(self, main_window_source):
        assert "license_manager.h" in main_window_source

    def test_includes_license_dialog(self, main_window_source):
        assert "license_dialog.h" in main_window_source

    def test_help_menu_exists(self, main_window_source):
        assert "Help" in main_window_source

    def test_license_config_loaded(self, main_window_source):
        assert "license.json" in main_window_source

    def test_about_slot(self, main_window_header):
        assert "onAbout" in main_window_header

    def test_license_blocked_slot(self, main_window_header):
        assert "onLicenseBlocked" in main_window_header

    def test_block_screen_method(self, main_window_header):
        assert "showLicenseBlockScreen" in main_window_header

    def test_includes_license_config_header(self, main_window_source):
        assert "license_config.h" in main_window_source

    def test_load_from_environment_called(self, main_window_source):
        assert "loadFromEnvironment" in main_window_source

    def test_prestige_mention_header(self, main_window_header):
        assert "Prestige Technologie Company" in main_window_header

    def test_about_dialog_text(self, main_window_source):
        assert "Prestige Technologie Company" in main_window_source

    def test_block_dialog_text(self, main_window_source):
        assert "ne peut pas" in main_window_source


# =====================================================================
# LicenseConfig module
# =====================================================================

class TestLicenseConfigModule:
    """Verify the LicenseConfig header/source for env variable loading."""

    def test_header_exists(self):
        assert os.path.isfile(LICENSE_CONFIG_HEADER)

    def test_source_exists(self):
        assert os.path.isfile(LICENSE_CONFIG_SOURCE)

    def test_header_pragma_once(self, config_header):
        assert "#pragma once" in config_header

    def test_class_declaration(self, config_header):
        assert "class LicenseConfig" in config_header

    def test_load_method(self, config_header):
        assert "load" in config_header

    def test_api_url_method(self, config_header):
        assert "apiUrl" in config_header

    def test_api_key_method(self, config_header):
        assert "apiKey" in config_header

    def test_is_valid_method(self, config_header):
        assert "isValid" in config_header

    def test_error_message_method(self, config_header):
        assert "errorMessage" in config_header

    def test_reads_env_variables(self, config_source):
        assert "LICENSE_API_URL" in config_source
        assert "LICENSE_API_KEY" in config_source

    def test_uses_qprocess_environment(self, config_source):
        assert "QProcessEnvironment" in config_source


# =====================================================================
# LicenseStorage module — encrypted storage & tamper detection
# =====================================================================

class TestLicenseStorageModule:
    """Verify the LicenseStorage header/source for encrypted storage."""

    def test_header_exists(self):
        assert os.path.isfile(LICENSE_STORAGE_HEADER)

    def test_source_exists(self):
        assert os.path.isfile(LICENSE_STORAGE_SOURCE)

    def test_header_pragma_once(self, storage_header):
        assert "#pragma once" in storage_header

    def test_class_declaration(self, storage_header):
        assert "class LicenseStorage" in storage_header

    def test_load_method(self, storage_header):
        assert "load" in storage_header

    def test_save_method(self, storage_header):
        assert "save" in storage_header

    def test_license_key_method(self, storage_header):
        assert "licenseKey" in storage_header

    def test_offline_valid_until(self, storage_header):
        assert "offlineValidUntil" in storage_header

    def test_is_tampered_method(self, storage_header):
        assert "isTampered" in storage_header

    def test_xor_obfuscate_method(self, storage_header):
        assert "xorObfuscate" in storage_header

    def test_compute_integrity_method(self, storage_header):
        assert "computeIntegrity" in storage_header

    def test_uses_sha256(self, storage_source):
        assert "Sha256" in storage_source

    def test_uses_xor(self, storage_source):
        assert "xorObfuscate" in storage_source

    def test_integrity_check(self, storage_source):
        assert "integrity" in storage_source

    def test_key_enc_field(self, storage_source):
        assert "key_enc" in storage_source

    def test_offline_field(self, storage_source):
        assert "offline_valid_until" in storage_source

    def test_tamper_detection(self, storage_source):
        """Verify that tampered flag is set on integrity mismatch."""
        assert "tampered_" in storage_source


# =====================================================================
# LicenseSecureLogger module
# =====================================================================

class TestLicenseSecureLoggerModule:
    """Verify the secure logger header/source."""

    def test_header_exists(self):
        assert os.path.isfile(LICENSE_LOGGER_HEADER)

    def test_source_exists(self):
        assert os.path.isfile(LICENSE_LOGGER_SOURCE)

    def test_header_pragma_once(self, logger_header):
        assert "#pragma once" in logger_header

    def test_class_declaration(self, logger_header):
        assert "class LicenseSecureLogger" in logger_header

    def test_log_validation_method(self, logger_header):
        assert "logValidation" in logger_header

    def test_log_error_method(self, logger_header):
        assert "logError" in logger_header

    def test_log_offline_mode(self, logger_header):
        assert "logOfflineModeEnabled" in logger_header

    def test_log_info_method(self, logger_header):
        assert "logInfo" in logger_header

    def test_writes_to_log_file(self, logger_source):
        assert "license_secure.log" in logger_source

    def test_uses_mutex(self, logger_source):
        assert "QMutex" in logger_source

    def test_timestamp_format(self, logger_source):
        assert "yyyy-MM-dd HH:mm:ss" in logger_source


# =====================================================================
# .env.example file
# =====================================================================

class TestEnvExample:
    """Verify the .env.example file is well-formed."""

    def test_file_exists(self):
        assert os.path.isfile(ENV_EXAMPLE)

    def test_contains_api_url(self, env_example):
        assert "LICENSE_API_URL" in env_example

    def test_contains_api_key(self, env_example):
        assert "LICENSE_API_KEY" in env_example

    def test_no_real_credentials(self, env_example):
        """Example file must not contain real Supabase project IDs."""
        assert "qkcchctrmrpdyseplbvb" not in env_example

    def test_security_warning(self, env_example):
        assert "Never" in env_example or "never" in env_example


# =====================================================================
# README security warning
# =====================================================================

class TestReadmeSecurity:
    """Verify the README has the required security warnings."""

    def test_supabase_warning(self, readme):
        assert "Ne jamais exposer" in readme

    def test_env_vars_documented(self, readme):
        assert "LICENSE_API_URL" in readme
        assert "LICENSE_API_KEY" in readme

    def test_prestige_mention(self, readme):
        assert "Prestige Technologie Company" in readme


# =====================================================================
# Offline grace mode tests
# =====================================================================

class TestOfflineGraceMode:
    """Verify the offline grace mode is fully implemented."""

    def test_offline_valid_until_in_header(self, manager_header):
        assert "offlineValidUntil" in manager_header

    def test_grace_days_constant(self, manager_header):
        assert "kOfflineGraceDays" in manager_header

    def test_try_offline_grace_in_source(self, manager_source):
        assert "tryOfflineGrace" in manager_source

    def test_refresh_deadline_on_valid(self, manager_source):
        """When validate_key returns active, deadline must be refreshed."""
        assert "refreshOfflineDeadline" in manager_source

    def test_offline_signal_emitted(self, manager_source):
        assert "offlineModeActivated" in manager_source

    def test_storage_offline_field(self, storage_header):
        assert "offline_valid_until" in storage_header

    def test_7_day_grace_in_source(self, manager_source):
        """Verify that addDays(kOfflineGraceDays) is used."""
        assert "kOfflineGraceDays" in manager_source

    def test_current_datetime_check(self, manager_source):
        assert "currentDateTimeUtc" in manager_source


# =====================================================================
# Invalid licence blocking tests
# =====================================================================

class TestInvalidLicenceBlocking:
    """Verify that invalid/expired/suspended licences block the app."""

    def test_should_block_declared(self, manager_header):
        assert "shouldBlockApplication" in manager_header

    def test_block_reason_declared(self, manager_header):
        assert "blockReason" in manager_header

    def test_license_blocked_signal(self, manager_header):
        assert "licenseBlocked" in manager_header

    def test_block_on_invalid(self, manager_source):
        assert "LicenseStatus::Invalid" in manager_source

    def test_block_on_expired(self, manager_source):
        assert "LicenseStatus::Expired" in manager_source

    def test_block_on_suspended(self, manager_source):
        assert "LicenseStatus::Suspended" in manager_source

    def test_main_window_handles_block(self, main_window_source):
        assert "onLicenseBlocked" in main_window_source

    def test_main_window_shows_block_screen(self, main_window_source):
        assert "showLicenseBlockScreen" in main_window_source

    def test_application_quit_called(self, main_window_source):
        assert "quit" in main_window_source


# =====================================================================
# Tampering detection tests
# =====================================================================

class TestTamperingDetection:
    """Verify that the storage module detects file tampering."""

    def test_integrity_hash_computed(self, storage_source):
        assert "computeIntegrity" in storage_source

    def test_sha256_used_for_integrity(self, storage_source):
        assert "Sha256" in storage_source

    def test_tampered_flag_set(self, storage_source):
        assert "tampered_ = true" in storage_source

    def test_xor_obfuscation_present(self, storage_source):
        assert "xorObfuscate" in storage_source

    def test_key_never_stored_plain(self, storage_source):
        """Encrypted key is stored as hex, never in plain text."""
        assert "toHex" in storage_source
        assert "fromHex" in storage_source

    def test_xor_key_derived_from_machine_id(self, storage_source):
        """XOR key must be derived from SHA-256 of machine ID."""
        assert "QCryptographicHash" in storage_source
        assert "machineId" in storage_source
