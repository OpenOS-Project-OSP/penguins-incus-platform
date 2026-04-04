#pragma once

#include "pipclient.h"
#include <QAbstractListModel>
#include <QVariantList>

namespace PIP {

class StorageModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(int count READ rowCount NOTIFY countChanged)

public:
    enum Roles {
        NameRole = Qt::UserRole + 1,
        DriverRole,
        StatusRole,
        DescriptionRole,
    };

    explicit StorageModel(PipClient *client, QObject *parent = nullptr);

    int      rowCount(const QModelIndex &parent = {}) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;
    QHash<int, QByteArray> roleNames() const override;

signals:
    void countChanged();

private slots:
    void onStoragePoolsListed(const QVariantList &pools);

private:
    QVariantList m_items;
};

} // namespace PIP
