#pragma once

#include "pipclient.h"
#include <QAbstractListModel>
#include <QVariantList>

namespace PIP {

class NetworksModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(int count READ rowCount NOTIFY countChanged)

public:
    enum Roles {
        NameRole = Qt::UserRole + 1,
        TypeRole,
        ManagedRole,
        DescriptionRole,
        ProjectRole,
    };

    explicit NetworksModel(PipClient *client, QObject *parent = nullptr);

    int      rowCount(const QModelIndex &parent = {}) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;
    QHash<int, QByteArray> roleNames() const override;

signals:
    void countChanged();

private slots:
    void onNetworksListed(const QVariantList &networks);

private:
    QVariantList m_items;
};

} // namespace PIP
