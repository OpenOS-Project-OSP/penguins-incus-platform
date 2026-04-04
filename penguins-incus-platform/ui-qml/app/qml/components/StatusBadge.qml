import QtQuick
import QtQuick.Controls

// Coloured dot + label for instance/operation status
Row {
    property string status: "Unknown"
    spacing: 6

    readonly property var colors: ({
        "Running":   "#22c55e",
        "Stopped":   "#94a3b8",
        "Frozen":    "#60a5fa",
        "Error":     "#ef4444",
        "Unknown":   "#f59e0b",
        "Online":    "#22c55e",
        "Offline":   "#ef4444",
        "Evacuated": "#f59e0b",
        "succeeded": "#22c55e",
        "failed":    "#ef4444",
        "running":   "#60a5fa",
        "pending":   "#f59e0b",
        "cancelled": "#94a3b8",
    })

    Rectangle {
        width: 8; height: 8; radius: 4
        anchors.verticalCenter: parent.verticalCenter
        color: colors[status] ?? "#94a3b8"
    }
    Label {
        text: status
        font.pixelSize: 12
        color: colors[status] ?? "#94a3b8"
        anchors.verticalCenter: parent.verticalCenter
    }
}
