import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import PIP 1.0

Page {
    id: root
    required property var client
    title: "Containers"

    // ── Model ─────────────────────────────────────────────────────────────
    ListModel { id: instanceModel }

    function reload() {
        client.listInstances("", "")
    }

    Connections {
        target: client

        function onInstancesListed(instances) {
            instanceModel.clear()
            for (let i = 0; i < instances.length; i++) {
                const inst = instances[i]
                if (inst.type !== "container") continue
                instanceModel.append({
                    name:               inst.name   ?? "",
                    status:             inst.status ?? "Unknown",
                    image:              inst.image  ?? "",
                    project:            inst.project ?? "default",
                    cpu_usage:          inst.cpu_usage ?? 0,
                    memory_usage_bytes: inst.memory_usage_bytes ?? 0,
                })
            }
        }

        function onInstanceStateChanged(name, status) {
            for (let i = 0; i < instanceModel.count; i++) {
                if (instanceModel.get(i).name === name) {
                    instanceModel.setProperty(i, "status", status)
                    break
                }
            }
        }

        function onResourceUsageUpdated(usage) {
            for (let i = 0; i < instanceModel.count; i++) {
                if (instanceModel.get(i).name === usage.name) {
                    instanceModel.setProperty(i, "cpu_usage",          usage.cpu_usage)
                    instanceModel.setProperty(i, "memory_usage_bytes", usage.memory_usage_bytes)
                    break
                }
            }
        }

        function onError(msg) { errorBar.text = msg; errorBar.visible = true }
    }

    Component.onCompleted: reload()

    // ── Header ────────────────────────────────────────────────────────────
    header: ToolBar {
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 12
            anchors.rightMargin: 12

            Label { text: "Containers"
            font.pixelSize: 16
            font.bold: true }
            Item  { Layout.fillWidth: true }

            Button {
                text: "↻ Refresh"
                flat: true
                onClicked: reload()
            }
            Button {
                text: "+ Create"
                highlighted: true
                onClicked: createDialog.open()
            }
        }
    }

    // ── Error bar ─────────────────────────────────────────────────────────
    Rectangle {
        id: errorBar
        property string text: ""
        visible: false
        anchors { top: parent.top
        left: parent.left
        right: parent.right }
        height: visible ? errorLabel.implicitHeight + 16 : 0
        color: "#fef2f2"
        border.color: "#fca5a5"
        z: 10

        Label {
            id: errorLabel
            text: errorBar.text
            color: "#b91c1c"
            anchors { verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: 12 }
        }
        Button {
            text: "✕"
            flat: true
            anchors { right: parent.right
            verticalCenter: parent.verticalCenter }
            onClicked: errorBar.visible = false
        }
    }

    // ── Table ─────────────────────────────────────────────────────────────
    HorizontalHeaderView {
        id: header
        anchors { top: errorBar.bottom
        left: parent.left
        right: parent.right }
        syncView: tableView
        model: ["Name", "Status", "Image", "Project", "CPU", "Memory", "Actions"]
    }

    TableView {
        id: tableView
        anchors {
            top: header.bottom
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
        model: instanceModel
        clip: true
        columnWidthProvider: (col) => [180, 110, 200, 120, 70, 100, 260][col] ?? 120

        delegate: Rectangle {
            implicitHeight: 44
            color: row % 2 === 0 ? "transparent" : "#f9fafb"
            border.color: "#f3f4f6"
            border.width: 0

            // Resolve model fields by column index
            readonly property var inst: instanceModel.get(row) ?? {}

            Loader {
                anchors.fill: parent
                anchors.leftMargin: 12
                anchors.rightMargin: 4

                sourceComponent: {
                    switch (column) {
                    case 0: return nameComp
                    case 1: return statusComp
                    case 2: return textComp
                    case 3: return textComp
                    case 4: return cpuComp
                    case 5: return memComp
                    case 6: return actionsComp
                    default: return textComp
                    }
                }

                // ── Cell components ───────────────────────────────────────
                Component {
                    id: nameComp
                    Label {
                        text: inst.name ?? ""
                        font.bold: true
                        verticalAlignment: Text.AlignVCenter
                        height: parent.height
                    }
                }
                Component {
                    id: statusComp
                    StatusBadge {
                        status: inst.status ?? "Unknown"
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }
                Component {
                    id: textComp
                    Label {
                        text: column === 2 ? (inst.image ?? "—")
                            : column === 3 ? (inst.project ?? "default")
                            : ""
                        color: "#6b7280"
                        font.pixelSize: 13
                        verticalAlignment: Text.AlignVCenter
                        height: parent.height
                        elide: Text.ElideRight
                    }
                }
                Component {
                    id: cpuComp
                    Label {
                        text: inst.cpu_usage > 0
                            ? (inst.cpu_usage * 100).toFixed(1) + "%"
                            : "—"
                        color: "#6b7280"
                        font.pixelSize: 13
                        verticalAlignment: Text.AlignVCenter
                        height: parent.height
                    }
                }
                Component {
                    id: memComp
                    Label {
                        text: inst.memory_usage_bytes > 0
                            ? (inst.memory_usage_bytes / 1048576).toFixed(0) + " MB"
                            : "—"
                        color: "#6b7280"
                        font.pixelSize: 13
                        verticalAlignment: Text.AlignVCenter
                        height: parent.height
                    }
                }
                Component {
                    id: actionsComp
                    RowLayout {
                        spacing: 4
                        anchors.verticalCenter: parent.verticalCenter

                        Button {
                            text: "Start"
                            visible: inst.status === "Stopped"
                            flat: true
                            font.pixelSize: 12
                            onClicked: client.startInstance(inst.name, inst.project)
                        }
                        Button {
                            text: "Stop"
                            visible: inst.status === "Running"
                            flat: true
                            font.pixelSize: 12
                            onClicked: client.stopInstance(inst.name, false, inst.project)
                        }
                        Button {
                            text: "Restart"
                            visible: inst.status === "Running"
                            flat: true
                            font.pixelSize: 12
                            onClicked: client.restartInstance(inst.name, false, inst.project)
                        }
                        Button {
                            text: "Freeze"
                            visible: inst.status === "Running"
                            flat: true
                            font.pixelSize: 12
                            onClicked: client.freezeInstance(inst.name, inst.project)
                        }
                        Button {
                            text: "Unfreeze"
                            visible: inst.status === "Frozen"
                            flat: true
                            font.pixelSize: 12
                            onClicked: client.startInstance(inst.name, inst.project)
                        }
                        Button {
                            text: "Delete"
                            font.pixelSize: 12
                            palette.button: "#ef4444"
                            palette.buttonText: "white"
                            onClicked: {
                                confirmDialog.targetName    = inst.name
                                confirmDialog.targetProject = inst.project
                                confirmDialog.open()
                            }
                        }
                    }
                }
            }
        }
    }

    // ── Empty state ───────────────────────────────────────────────────────
    Label {
        visible: instanceModel.count === 0
        text: "No containers found"
        color: "#9ca3af"
        anchors.centerIn: parent
    }

    // ── Dialogs ───────────────────────────────────────────────────────────
    CreateInstanceDialog {
        id: createDialog
        instanceType: "container"
        onCreateRequested: (name, image, type) => {
            client.createInstance({ name, image, type, profiles: ["default"] })
            reload()
        }
    }

    ConfirmDialog {
        id: confirmDialog
        property string targetName: ""
        property string targetProject: ""
        title: "Delete container"
        message: `Delete "${targetName}"? This cannot be undone.`
        confirmLabel: "Delete"
        onConfirmed: {
            client.deleteInstance(targetName, true, targetProject)
            reload()
        }
    }
}
