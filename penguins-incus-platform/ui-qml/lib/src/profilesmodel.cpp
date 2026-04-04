#include "profilesmodel.h"

namespace PIP {

ProfilesModel::ProfilesModel(PipClient *client, QObject *parent)
    : QAbstractListModel(parent)
{
    connect(client, &PipClient::profilesListed,
            this,   &ProfilesModel::onProfilesListed);
}

int ProfilesModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid()) return 0;
    return static_cast<int>(m_items.size());
}

QVariant ProfilesModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || index.row() >= m_items.size()) return {};
    const auto m = m_items.at(index.row()).toMap();
    switch (role) {
    case NameRole:        return m.value("name");
    case DescriptionRole: return m.value("description");
    case ProjectRole:     return m.value("project");
    default:              return {};
    }
}

QHash<int, QByteArray> ProfilesModel::roleNames() const
{
    return {
        { NameRole,        "name"        },
        { DescriptionRole, "description" },
        { ProjectRole,     "project"     },
    };
}

void ProfilesModel::onProfilesListed(const QVariantList &profiles)
{
    beginResetModel();
    m_items = profiles;
    endResetModel();
    emit countChanged();
}

} // namespace PIP
