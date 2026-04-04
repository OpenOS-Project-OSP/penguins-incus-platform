#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "pipclient.h"
#include "containersmodel.h"
#include "networksmodel.h"
#include "storagemodel.h"
#include "imagesmodel.h"
#include "profilesmodel.h"
#include "eventsource.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    app.setOrganizationName("KapsuleIncusManager");
    app.setOrganizationDomain("penguins-incus-platform.org");
    app.setApplicationName("Kapsule Incus Manager");
    app.setApplicationVersion("0.1.0");

    qmlRegisterType<PIP::PipClient>      ("PIP", 1, 0, "PipClient");
    qmlRegisterType<PIP::ContainersModel>("PIP", 1, 0, "ContainersModel");
    qmlRegisterType<PIP::NetworksModel>  ("PIP", 1, 0, "NetworksModel");
    qmlRegisterType<PIP::StorageModel>   ("PIP", 1, 0, "StorageModel");
    qmlRegisterType<PIP::ImagesModel>    ("PIP", 1, 0, "ImagesModel");
    qmlRegisterType<PIP::ProfilesModel>  ("PIP", 1, 0, "ProfilesModel");
    qmlRegisterType<PIP::EventSource>    ("PIP", 1, 0, "EventSource");

    QQmlApplicationEngine engine;

    const QUrl url(u"qrc:/PIP/qml/Main.qml"_qs);
    QObject::connect(
        &engine, &QQmlApplicationEngine::objectCreationFailed,
        &app, [](const QUrl &) { QCoreApplication::exit(-1); },
        Qt::QueuedConnection);

    engine.load(url);
    return app.exec();
}
