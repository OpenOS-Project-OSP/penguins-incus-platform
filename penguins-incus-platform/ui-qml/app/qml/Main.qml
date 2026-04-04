import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import PIP 1.0

ApplicationWindow {
    id: root
    visible: true
    width: 1280
    height: 800
    title: "Kapsule Incus Manager"

    PipClient {
        id: kimClient
        onError: (msg) => statusBar.showError(msg)
    }

    // Navigation sidebar + page stack layout
    RowLayout {
        anchors.fill: parent
        spacing: 0

        // Sidebar
        Rectangle {
            Layout.preferredWidth: 200
            Layout.fillHeight: true
            color: palette.base

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 8
                spacing: 4

                Repeater {
                    model: [
                        { label: "Containers",  page: "ContainersPage" },
                        { label: "VMs",         page: "VMsPage" },
                        { label: "Networks",    page: "NetworksPage" },
                        { label: "Storage",     page: "StoragePage" },
                        { label: "Images",      page: "ImagesPage" },
                        { label: "Profiles",    page: "ProfilesPage" },
                        { label: "Projects",    page: "ProjectsPage" },
                        { label: "Cluster",     page: "ClusterPage" },
                        { label: "Remotes",     page: "RemotesPage" },
                        { label: "Operations",  page: "OperationsPage" },
                        { label: "Events",      page: "EventsPage" },
                    ]

                    delegate: Button {
                        Layout.fillWidth: true
                        text: modelData.label
                        flat: true
                        onClicked: pageStack.replace(
                            Qt.resolvedUrl("pages/" + modelData.page + ".qml"),
                            { client: kimClient }
                        )
                    }
                }

                Item { Layout.fillHeight: true }

                // Connection status indicator
                Label {
                    Layout.fillWidth: true
                    text: kimClient.connected ? "● Connected" : "○ Disconnected"
                    color: kimClient.connected ? "green" : "red"
                    font.pointSize: 9
                }
            }
        }

        // Page area
        StackView {
            id: pageStack
            Layout.fillWidth: true
            Layout.fillHeight: true
            initialItem: Qt.resolvedUrl("pages/ContainersPage.qml")
        }
    }

    // Status bar stub
    footer: ToolBar {
        id: statusBar
        property string message: ""
        function showError(msg) { message = msg }
        Label { text: statusBar.message; anchors.verticalCenter: parent.verticalCenter; leftPadding: 8 }
    }
}
