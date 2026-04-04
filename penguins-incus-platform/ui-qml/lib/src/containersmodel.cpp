#include "containersmodel.h"

namespace PIP {

ContainersModel::ContainersModel(PipClient *client, QObject *parent)
    : QAbstractListModel(parent)
{
    connect(client, &PipClient::instancesListed,
            this,   &ContainersModel::onInstancesListed);
}

int ContainersModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid()) return 0;
    return static_cast<int>(m_items.size());
}

QVariant ContainersModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || index.row() >= m_items.size()) return {};
    const auto m = m_items.at(index.row()).toMap();
    switch (role) {
    case NameRole:              return m.value("name");
    case StatusRole:            return m.value("status");
    case ImageRole:             return m.value("image");
    case ProjectRole:           return m.value("project");
    case RemoteRole:            return m.value("remote");
    case TypeRole:              return m.value("type");
    case CpuUsageRole:          return m.value("cpu_usage");
    case MemoryUsageBytesRole:  return m.value("memory_usage_bytes");
    case DiskUsageBytesRole:    return m.value("disk_usage_bytes");
    default:                    return {};
    }
}

QHash<int, QByteArray> ContainersModel::roleNames() const
{
    return {
        { NameRole,             "name"              },
        { StatusRole,           "status"            },
        { ImageRole,            "image"             },
        { ProjectRole,          "project"           },
        { RemoteRole,           "remote"            },
        { TypeRole,             "type"              },
        { CpuUsageRole,         "cpuUsage"          },
        { MemoryUsageBytesRole, "memoryUsageBytes"  },
        { DiskUsageBytesRole,   "diskUsageBytes"    },
    };
}

void ContainersModel::onInstancesListed(const QVariantList &instances)
{
    beginResetModel();
    m_items = instances;
    endResetModel();
    emit countChanged();
}

} // namespace PIP
