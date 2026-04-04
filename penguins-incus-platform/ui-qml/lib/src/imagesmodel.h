#pragma once

#include "pipclient.h"
#include <QAbstractListModel>
#include <QVariantList>

namespace PIP {

class ImagesModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(int count READ rowCount NOTIFY countChanged)

public:
    enum Roles {
        FingerprintRole = Qt::UserRole + 1,
        DescriptionRole,
        OsRole,
        ReleaseRole,
        ArchitectureRole,
        UploadedAtRole,
    };

    explicit ImagesModel(PipClient *client, QObject *parent = nullptr);

    int      rowCount(const QModelIndex &parent = {}) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;
    QHash<int, QByteArray> roleNames() const override;

signals:
    void countChanged();

private slots:
    void onImagesListed(const QVariantList &images);

private:
    QVariantList m_items;
};

} // namespace PIP
