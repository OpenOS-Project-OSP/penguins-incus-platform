#pragma once

#include "pipclient.h"
#include <QAbstractListModel>
#include <QVariantList>

namespace PIP {

/**
 * QAbstractListModel backed by PipClient::instancesListed.
 * Exposes every key from the JSON instance object as a named role so QML
 * delegates can bind directly: model.name, model.status, model.image, etc.
 */
class ContainersModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(int count READ rowCount NOTIFY countChanged)

public:
    enum Roles {
        NameRole = Qt::UserRole + 1,
        StatusRole,
        ImageRole,
        ProjectRole,
        RemoteRole,
        TypeRole,
        CpuUsageRole,
        MemoryUsageBytesRole,
        DiskUsageBytesRole,
    };

    explicit ContainersModel(PipClient *client, QObject *parent = nullptr);

    int      rowCount(const QModelIndex &parent = {}) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;
    QHash<int, QByteArray> roleNames() const override;

signals:
    void countChanged();

private slots:
    void onInstancesListed(const QVariantList &instances);

private:
    QVariantList m_items;
};

} // namespace PIP
