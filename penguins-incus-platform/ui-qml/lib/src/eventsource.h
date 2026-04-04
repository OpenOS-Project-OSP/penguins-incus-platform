#pragma once

#include <QObject>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QVariantMap>
#include <QByteArray>

namespace PIP {

/**
 * SSE client that connects to the PIP daemon's /api/v1/events endpoint and
 * emits eventReceived() for each parsed event.
 *
 * Usage from QML:
 *   EventSource { id: es; url: "http://127.0.0.1:8765/api/v1/events" }
 *   Connections { target: es; function onEventReceived(e) { ... } }
 *
 * The component reconnects automatically after a 3-second delay if the
 * connection drops.
 */
class EventSource : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QUrl    url       READ url       WRITE setUrl       NOTIFY urlChanged)
    Q_PROPERTY(bool    active    READ isActive  WRITE setActive    NOTIFY activeChanged)
    Q_PROPERTY(QString typeFilter READ typeFilter WRITE setTypeFilter NOTIFY typeFilterChanged)

public:
    explicit EventSource(QObject *parent = nullptr);
    ~EventSource() override;

    QUrl    url()        const { return m_url; }
    bool    isActive()   const { return m_active; }
    QString typeFilter() const { return m_typeFilter; }

    void setUrl(const QUrl &url);
    void setActive(bool active);
    void setTypeFilter(const QString &filter);

    Q_INVOKABLE void open();
    Q_INVOKABLE void close();

signals:
    void urlChanged();
    void activeChanged();
    void typeFilterChanged();
    void eventReceived(const QVariantMap &event);
    void connected();
    void disconnected();
    void errorOccurred(const QString &message);

private slots:
    void onReadyRead();
    void onFinished();
    void reconnect();

private:
    void startRequest();
    void parseLines(const QByteArray &chunk);

    QNetworkAccessManager *m_nam    = nullptr;
    QNetworkReply         *m_reply  = nullptr;
    QUrl                   m_url;
    QString                m_typeFilter;
    bool                   m_active = false;
    QByteArray             m_buffer;
};

} // namespace PIP
