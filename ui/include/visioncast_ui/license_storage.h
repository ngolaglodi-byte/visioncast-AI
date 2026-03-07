#pragma once

/// @file license_storage.h
/// @brief Encrypted local license storage with tamper detection.
///
/// The license key is never stored in plain text.  It is XOR-obfuscated
/// with a key derived from the SHA-256 of the machine_id, and the file
/// carries a SHA-256 integrity hash so that manual edits are detected.
///
/// File format (license.dat) — JSON:
/// {
///   "key_enc":               "<hex-encoded XOR-obfuscated key>",
///   "offline_valid_until":   "<ISO 8601 date-time>",
///   "integrity":             "<SHA-256 hex of key_enc + offline_valid_until>"
/// }

#include <QDateTime>
#include <QString>

namespace visioncast_ui {

/// Handles reading and writing the encrypted license.dat file.
class LicenseStorage {
public:
    /// Construct a storage manager for the given machine identifier.
    explicit LicenseStorage(const QString& machineId);

    // ── Read ────────────────────────────────────────────────────────

    /// Load and decrypt license.dat.
    /// @return true if the file exists, parses, and passes integrity check.
    bool load(const QString& path);

    /// @return The decrypted license key (empty if not loaded / tampered).
    QString licenseKey() const;

    /// @return The offline-valid-until deadline stored in the file.
    QDateTime offlineValidUntil() const;

    /// @return true if the file was tampered with (integrity mismatch).
    bool isTampered() const;

    // ── Write ───────────────────────────────────────────────────────

    /// Encrypt and persist the license key and offline deadline.
    bool save(const QString& path,
              const QString& licenseKey,
              const QDateTime& offlineValidUntil) const;

    // ── Helpers ─────────────────────────────────────────────────────

    /// XOR-obfuscate @p data with a key derived from the machine ID.
    /// XOR is symmetric — the same function encrypts and decrypts.
    QByteArray xorObfuscate(const QByteArray& data) const;

    /// Compute the SHA-256 integrity hash for the given fields.
    static QByteArray computeIntegrity(const QString& keyEnc,
                                       const QString& offlineUntil);

private:
    QString   machineId_;
    QByteArray xorKey_;       ///< SHA-256 of machineId_ (32 bytes).
    QString   licenseKey_;
    QDateTime offlineValidUntil_;
    bool      tampered_ = false;
};

} // namespace visioncast_ui
