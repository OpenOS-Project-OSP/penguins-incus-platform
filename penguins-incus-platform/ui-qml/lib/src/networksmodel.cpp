#include "networksmodel.h"

namespace PIP {

NetworksModel::NetworksModel(PipClient *client, QObject *parent)
    : QAbstractListModel(parent)
{
    connect(client, &PipClient::networksListed,
            this,   &NetworksModel::onNetworksListed);
}

int NetworksModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid()) return 0;
    return static_cast<int>(m_items.size());
}

QVariant NetworksModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || index.row() >= m_items.size()) return {};
    const auto m = m_items.at(index.row()).toMap();
    switch (role) {
    case NameRole:        return m.value("name");
    case TypeRole:        return m.value("type");
    case ManagedRole:     return m.value("managed");
    case DescriptionRole: return m.value("description");
    case ProjectRole:     return m.value("project");
    default:              return {};
    }
}

QHash<int, QByteArray> NetworksModel::roleNames() const
{
    return {
        { NameRole,        "name"        },
        { TypeRole,        "type"        },
        { ManagedRole,     "managed"     },
        { DescriptionRole, "description" },
        { ProjectRole,     "project"     },
    };
}

void NetworksModel::onNetworksListed(const QVariantList &networks)
{
    beginResetModel();
    m_items = networks;
    endResetModel();
    emit countChanged();
}

} // namespace PIP
