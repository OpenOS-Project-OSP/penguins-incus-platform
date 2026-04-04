#pragma once

#include <QString>
#include <QDateTime>

namespace PIP {

enum class ContainerStatus {
    Running,
    Stopped,
    Frozen,
    Error,
    Unknown,
};

enum class InstanceType {
    Container,
    VirtualMachine,
};

struct Instance {
    QString      name;
    InstanceType type;
    ContainerStatus status;
    QString      image;
    QString      project;
    QString      remote;
    QDateTime    createdAt;
};

struct Network {
    QString name;
    QString type;
    QString description;
    bool    managed;
};

struct StoragePool {
    QString name;
    QString driver;
    QString description;
    QString status;
};

struct Profile {
    QString name;
    QString description;
};

struct Image {
    QString fingerprint;
    QString description;
    QString os;
    QString release;
    QString architecture;
    QDateTime uploadedAt;
};

struct Operation {
    QString   id;
    QString   description;
    QString   status;
    QDateTime createdAt;
};

} // namespace PIP
