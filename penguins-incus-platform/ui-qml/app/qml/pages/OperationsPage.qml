import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import PIP 1.0

Page {
    id: root
    required property var client
    title: "Operations"
    ListModel { id: opModel }
    function reload() { client.listOperations() }
    Connections {
        target: client
        function onOperationsListed(ops) {
            opModel.clear()
            for (let i = 0; i < ops.length; i++) {
                const o = ops[i]
                opModel.append({ id:o.id??"", description:o.description??"", status:o.status??"", created_at:o.created_at??"" })
            }
        }
        function onEventReceived(event) {
            if (event.type === "operation") reload()
        }
        function onError(msg) { errorBar.text = msg; errorBar.visible = true }
    }
    Component.onCompleted: reload()
    header: ToolBar {
        RowLayout { anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 12
            Label { text: "Operations"
            font.pixelSize: 16
            font.bold: true }
            Item { Layout.fillWidth: true }
            Button { text: "↻ Refresh"
            flat: true
            onClicked: reload() }
        }
    }
    Rectangle { id: errorBar; property string text: ""
    visible: false
        anchors { top: parent.top
        left: parent.left
        right: parent.right }
        height: visible ? 40 : 0
        color: "#fef2f2"
        border.color: "#fca5a5"
        z: 10
        Label { text: errorBar.text
        color: "#b91c1c"
        anchors { verticalCenter: parent.verticalCenter
        left: parent.left
        leftMargin: 12 } }
        Button { text: "✕"
        flat: true
        anchors { right: parent.right
        verticalCenter: parent.verticalCenter }
        onClicked: errorBar.visible = false }
    }
    ListView {
        anchors { top: errorBar.bottom
        left: parent.left
        right: parent.right
        bottom: parent.bottom }
        model: opModel
        clip: true
        header: Row { height: 36
            Repeater { model: ["ID","Description","Status","Created","Actions"]
                Label { width:[120,300,110,180,120][index]
                height:36
                text:modelData
                font.bold:true
                color:"#374151"
                verticalAlignment:Text.AlignVCenter
                leftPadding:12 }
            }
        }
        delegate: Rectangle {
            width: ListView.view.width
            height: 44
            color: index%2===0?"transparent":"#f9fafb"
            Row { anchors.verticalCenter: parent.verticalCenter
                Label { width:120
                text:id.slice(0,8)+"…"
                font.family:"monospace"
                font.pixelSize:12
                leftPadding:12 }
                Label { width:300
                text:description
                leftPadding:4
                elide:Text.ElideRight }
                StatusBadge { width:110
                status:model.status
                anchors.verticalCenter:parent.verticalCenter }
                Label { width:180
                text:created_at
                color:"#6b7280"
                font.pixelSize:12
                leftPadding:4 }
                Button { visible:model.status==="running"||model.status==="pending"
                    text:"Cancel"
                    font.pixelSize:12
                    palette.button:"#ef4444"
                    palette.buttonText:"white"
                    onClicked:{ client.cancelOperation(id); reload() } }
            }
        }
        Label { visible: opModel.count===0
        text:"No operations"
        color:"#9ca3af"
        anchors.centerIn: parent }
    }
}
