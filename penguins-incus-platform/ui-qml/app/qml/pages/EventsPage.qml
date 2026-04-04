import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import PIP 1.0

Page {
    id: root
    required property var client
    title: "Events"

    property bool paused: false
    property string filterText: ""
    readonly property int maxEvents: 200

    ListModel { id: eventModel }

    Connections {
        target: client
        function onEventReceived(event) {
            if (root.paused) return
            if (root.filterText && !JSON.stringify(event).includes(root.filterText)) return
            if (eventModel.count >= root.maxEvents) eventModel.remove(0)
            eventModel.append({
                timestamp: event.timestamp ?? "",
                type:      event.type ?? "",
                project:   event.project ?? "",
                payload:   JSON.stringify(event.metadata ?? {})
            })
            listView.positionViewAtEnd()
        }
    }

    header: ToolBar {
        RowLayout { anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 12
            Label { text: "Events"
            font.pixelSize: 16
            font.bold: true }
            Item { Layout.fillWidth: true }
            TextField {
                placeholderText: "Filter…"
                onTextChanged: root.filterText = text
                implicitWidth: 160
            }
            Button {
                text: root.paused ? "▶ Resume" : "⏸ Pause"
                flat: true
                onClicked: root.paused = !root.paused
            }
            Button {
                text: "Clear"
                flat: true
                onClicked: eventModel.clear()
            }
        }
    }

    Rectangle {
        anchors.fill: parent
        anchors.margins: 12
        color: "#0f172a"
        radius: 8

        ListView {
            id: listView
            anchors.fill: parent
            anchors.margins: 12
            model: eventModel
            clip: true

            Label {
                visible: eventModel.count === 0
                text: "Waiting for events…"
                color: "#475569"
                anchors.centerIn: parent
                font.family: "monospace"
            }

            delegate: Item {
                width: ListView.view.width
                height: eventRow.implicitHeight + 8

                Row {
                    id: eventRow
                    anchors { left: parent.left
                    right: parent.right
                    verticalCenter: parent.verticalCenter }
                    spacing: 8

                    Label { text: timestamp
                    color: "#94a3b8"
                    font.family: "monospace"
                    font.pixelSize: 11 }
                    Label { text: "[" + type + "]"
                    color: "#60a5fa"
                    font.family: "monospace"
                    font.pixelSize: 11 }
                    Label { visible: project.length > 0
                    text: project
                    color: "#a78bfa"
                    font.family: "monospace"
                    font.pixelSize: 11 }
                    Label {
                        text: payload
                        color: "#e2e8f0"
                        font.family: "monospace"
                        font.pixelSize: 11
                        wrapMode: Text.WrapAnywhere
                        width: parent.width - 400
                    }
                }

                Rectangle {
                    anchors { left: parent.left
                    right: parent.right
                    bottom: parent.bottom }
                    height: 1
                    color: "#1e293b"
                }
            }
        }
    }
}
