/// @file license_storage.cpp
/// @brief LicenseStorage implementation — encrypted license.dat I/O.

#include "visioncast_ui/license_storage.h"

#include <QCryptographicHash>
#include <QFile>
#include <QJsonDocument>
#include <QJsonObject>

namespace visioncast_ui {

LicenseStorage::LicenseStorage(const QString& machineId)
    : machineId_(machineId)
    , xorKey_(QCryptographicHash::hash(machineId.toUtf8(),
                                       QCryptographicHash::Sha256))
{
}

// ── Read ────────────────────────────────────────────────────────────

bool LicenseStorage::load(const QString& path) {
    tampered_ = false;
    licenseKey_.clear();
    offlineValidUntil_ = QDateTime();

    QFile file(path);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
        return false;

    QJsonParseError err;
    auto doc = QJsonDocument::fromJson(file.readAll(), &err);
    file.close();
    if (err.error != QJsonParseError::NoError)
        return false;

    const auto obj       = doc.object();
    const QString keyEnc = obj.value("key_enc").toString();
    const QString until  = obj.value("offline_valid_until").toString();
    const QString stored = obj.value("integrity").toString();

    // Integrity check.
    const QByteArray expected = computeIntegrity(keyEnc, until);
    if (stored != QString::fromLatin1(expected)) {
        tampered_ = true;
        return false;
    }

    // Decrypt the key.
    QByteArray encBytes = QByteArray::fromHex(keyEnc.toLatin1());
    QByteArray plain    = xorObfuscate(encBytes);
    licenseKey_         = QString::fromUtf8(plain);

    offlineValidUntil_ = QDateTime::fromString(until, Qt::ISODate);
    return true;
}

QString   LicenseStorage::licenseKey()        const { return licenseKey_; }
QDateTime LicenseStorage::offlineValidUntil() const { return offlineValidUntil_; }
bool      LicenseStorage::isTampered()        const { return tampered_; }

// ── Write ───────────────────────────────────────────────────────────

bool LicenseStorage::save(const QString& path,
                          const QString& licenseKey,
                          const QDateTime& offlineValidUntil) const {
    QByteArray enc    = xorObfuscate(licenseKey.toUtf8());
    QString    keyHex = QString::fromLatin1(enc.toHex());
    QString    until  = offlineValidUntil.toString(Qt::ISODate);

    QJsonObject obj;
    obj["key_enc"]              = keyHex;
    obj["offline_valid_until"]  = until;
    obj["integrity"]            = QString::fromLatin1(
        computeIntegrity(keyHex, until));

    QFile file(path);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
        return false;
    file.write(QJsonDocument(obj).toJson(QJsonDocument::Indented));
    file.close();
    return true;
}

// ── Helpers ─────────────────────────────────────────────────────────

QByteArray LicenseStorage::xorObfuscate(const QByteArray& data) const {
    QByteArray result;
    result.resize(data.size());
    for (int i = 0; i < data.size(); ++i)
        result[i] = data[i] ^ xorKey_[i % xorKey_.size()];
    return result;
}

QByteArray LicenseStorage::computeIntegrity(const QString& keyEnc,
                                             const QString& offlineUntil) {
    QByteArray payload = (keyEnc + offlineUntil).toUtf8();
    return QCryptographicHash::hash(payload, QCryptographicHash::Sha256)
        .toHex();
}

} // namespace visioncast_ui
