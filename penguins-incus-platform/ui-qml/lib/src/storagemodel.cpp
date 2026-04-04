#include "storagemodel.h"

namespace PIP {

StorageModel::StorageModel(PipClient *client, QObject *parent)
    : QAbstractListModel(parent)
{
    connect(client, &PipClient::storagePoolsListed,
            this,   &StorageModel::onStoragePoolsListed);
}

int StorageModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid()) return 0;
    return static_cast<int>(m_items.size());
}

QVariant StorageModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || index.row() >= m_items.size()) return {};
    const auto m = m_items.at(index.row()).toMap();
    switch (role) {
    case NameRole:        return m.value("name");
    case DriverRole:      return m.value("driver");
    case StatusRole:      return m.value("status");
    case DescriptionRole: return m.value("description");
    default:              return {};
    }
}

QHash<int, QByteArray> StorageModel::roleNames() const
{
    return {
        { NameRole,        "name"        },
        { DriverRole,      "driver"      },
        { StatusRole,      "status"      },
        { DescriptionRole, "description" },
    };
}

void StorageModel::onStoragePoolsListed(const QVariantList &pools)
{
    beginResetModel();
    m_items = pools;
    endResetModel();
    emit countChanged();
}

} // namespace PIP
