#include "imagesmodel.h"

namespace PIP {

ImagesModel::ImagesModel(PipClient *client, QObject *parent)
    : QAbstractListModel(parent)
{
    connect(client, &PipClient::imagesListed,
            this,   &ImagesModel::onImagesListed);
}

int ImagesModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid()) return 0;
    return static_cast<int>(m_items.size());
}

QVariant ImagesModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || index.row() >= m_items.size()) return {};
    const auto m = m_items.at(index.row()).toMap();
    switch (role) {
    case FingerprintRole:  return m.value("fingerprint");
    case DescriptionRole:  return m.value("description");
    case OsRole:           return m.value("os");
    case ReleaseRole:      return m.value("release");
    case ArchitectureRole: return m.value("architecture");
    case UploadedAtRole:   return m.value("uploaded_at");
    default:               return {};
    }
}

QHash<int, QByteArray> ImagesModel::roleNames() const
{
    return {
        { FingerprintRole,  "fingerprint"  },
        { DescriptionRole,  "description"  },
        { OsRole,           "os"           },
        { ReleaseRole,      "release"      },
        { ArchitectureRole, "architecture" },
        { UploadedAtRole,   "uploadedAt"   },
    };
}

void ImagesModel::onImagesListed(const QVariantList &images)
{
    beginResetModel();
    m_items = images;
    endResetModel();
    emit countChanged();
}

} // namespace PIP
