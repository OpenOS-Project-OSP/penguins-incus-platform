qt_add_executable(penguins-incus-app
    src/main.cpp
)

qt_add_qml_module(penguins-incus-app
    URI PIP
    VERSION 1.0
    QML_FILES
        qml/Main.qml
        qml/pages/ContainersPage.qml
        qml/pages/VMsPage.qml
        qml/pages/NetworksPage.qml
        qml/pages/StoragePage.qml
        qml/pages/ImagesPage.qml
        qml/pages/ProfilesPage.qml
        qml/pages/ProjectsPage.qml
        qml/pages/ClusterPage.qml
        qml/pages/RemotesPage.qml
        qml/pages/OperationsPage.qml
        qml/pages/EventsPage.qml
        qml/components/StatusBadge.qml
        qml/components/ConfirmDialog.qml
        qml/components/CreateInstanceDialog.qml
)

target_link_libraries(penguins-incus-app PRIVATE
    penguins-incus-qt
    Qt6::Quick
    Qt6::QuickControls2
    Qt6::WebSockets
)

if(KF6_FOUND)
    target_link_libraries(penguins-incus-app PRIVATE
        KF6::CoreAddons
        KF6::Notifications
        KF6::WindowSystem
    )
    target_compile_definitions(penguins-incus-app PRIVATE KDE_INTEGRATION)
endif()

install(TARGETS penguins-incus-app DESTINATION ${CMAKE_INSTALL_BINDIR})
