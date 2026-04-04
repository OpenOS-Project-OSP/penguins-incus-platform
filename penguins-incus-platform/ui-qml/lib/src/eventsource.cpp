#include "eventsource.h"
#include <QJsonDocument>
#include <QJsonObject>
#include <QNetworkRequest>
#include <QTimer>
#include <QUrlQuery>

namespace PIP {

static constexpr int kReconnectMs = 3000;

EventSource::EventSource(QObject *parent)
    : QObject(parent)
    , m_nam(new QNetworkAccessManager(this))
{}

EventSource::~EventSource()
{
    close();
}

// ── property setters ──────────────────────────────────────────────────────────

void EventSource::setUrl(const QUrl &url)
{
    if (m_url == url) return;
    m_url = url;
    emit urlChanged();
    if (m_active) { close(); open(); }
}

void EventSource::setActive(bool active)
{
    if (m_active == active) return;
    m_active = active;
    emit activeChanged();
    active ? open() : close();
}

void EventSource::setTypeFilter(const QString &filter)
{
    if (m_typeFilter == filter) return;
    m_typeFilter = filter;
    emit typeFilterChanged();
    if (m_active) { close(); open(); }
}

// ── public slots ──────────────────────────────────────────────────────────────

void EventSource::open()
{
    if (m_reply) return; // already open
    if (!m_url.isValid()) return;
    m_active = true;
    startRequest();
}

void EventSource::close()
{
    m_active = false;
    if (m_reply) {
        m_reply->abort();
        m_reply->deleteLater();
        m_reply = nullptr;
        emit disconnected();
    }
    m_buffer.clear();
}

// ── private ───────────────────────────────────────────────────────────────────

void EventSource::startRequest()
{
    QUrl url = m_url;
    if (!m_typeFilter.isEmpty()) {
        QUrlQuery q(url.query());
        q.addQueryItem("type", m_typeFilter);
        url.setQuery(q);
    }

    QNetworkRequest req(url);
    req.setRawHeader("Accept", "text/event-stream");
    req.setAttribute(QNetworkRequest::CacheLoadControlAttribute,
                     QNetworkRequest::AlwaysNetwork);
    // Keep the connection alive for streaming
    req.setAttribute(QNetworkRequest::Http2AllowedAttribute, false);

    m_reply = m_nam->get(req);
    connect(m_reply, &QNetworkReply::readyRead, this, &EventSource::onReadyRead);
    connect(m_reply, &QNetworkReply::finished,  this, &EventSource::onFinished);
    emit connected();
}

void EventSource::onReadyRead()
{
    m_buffer += m_reply->readAll();
    // SSE lines are separated by '\n'; events are separated by blank lines.
    // We process complete lines only, leaving any partial line in the buffer.
    int pos = 0;
    while (true) {
        int nl = m_buffer.indexOf('\n', pos);
        if (nl < 0) break;
        const QByteArray line = m_buffer.mid(pos, nl - pos).trimmed();
        pos = nl + 1;
        parseLines(line);
    }
    m_buffer = m_buffer.mid(pos);
}

void EventSource::parseLines(const QByteArray &line)
{
    if (!line.startsWith("data:")) return;
    const QByteArray payload = line.mid(5).trimmed();
    const auto doc = QJsonDocument::fromJson(payload);
    if (!doc.isObject()) return;
    emit eventReceived(doc.object().toVariantMap());
}

void EventSource::onFinished()
{
    if (!m_reply) return;
    const auto err = m_reply->error();
    m_reply->deleteLater();
    m_reply = nullptr;
    emit disconnected();

    if (!m_active) return; // intentional close — don't reconnect

    if (err != QNetworkReply::NoError && err != QNetworkReply::OperationCanceledError) {
        emit errorOccurred(m_reply ? m_reply->errorString() : "Connection lost");
    }
    // Reconnect after a short delay
    QTimer::singleShot(kReconnectMs, this, &EventSource::reconnect);
}

void EventSource::reconnect()
{
    if (m_active && !m_reply) startRequest();
}

} // namespace PIP
