import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import PIP 1.0

Page {
    id: root
    required property var client
    title: "Networks"
    ListModel { id: netModel }
    function reload() { client.listNetworks("") }
    Connections {
        target: client
        function onNetworksListed(networks) {
            netModel.clear()
            for (let i = 0; i < networks.length; i++) {
                const n = networks[i]
                netModel.append({ name: n.name??"", type: n.type??"", managed: n.managed??false, description: n.description??"" })
            }
        }
        function onError(msg) { errorBar.text = msg; errorBar.visible = true }
    }
    Component.onCompleted: reload()
    header: ToolBar {
        RowLayout { anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 12
            Label { text: "Networks"
            font.pixelSize: 16
            font.bold: true }
            Item { Layout.fillWidth: true }
            Button { text: "↻ Refresh"
            flat: true
            onClicked: reload() }
            Button { text: "+ Create"
            highlighted: true
            onClicked: createDialog.open() }
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
        model: netModel
        clip: true
        header: Row { height: 36
            Repeater { model: ["Name","Type","Managed","Description","Actions"]
                Label { width: [200,120,90,260,160][index]
                height: 36
                text: modelData
                font.bold: true
                color: "#374151"
                verticalAlignment: Text.AlignVCenter
                leftPadding: 12 }
            }
        }
        delegate: Rectangle {
            width: ListView.view.width
            height: 44
            color: index%2===0?"transparent":"#f9fafb"
            Row { anchors.verticalCenter: parent.verticalCenter
                Label { width:200
                text: name
                font.bold:true
                leftPadding:12
                elide:Text.ElideRight }
                Label { width:120
                text: type
                color:"#6b7280"
                leftPadding:4 }
                Label { width:90;  text: managed?"Yes":"No"
                color:"#6b7280"
                leftPadding:4 }
                Label { width:260
                text: description||"—"
                color:"#6b7280"
                font.pixelSize:13
                leftPadding:4
                elide:Text.ElideRight }
                Button { visible: managed
                text:"Delete"
                font.pixelSize:12
                palette.button:"#ef4444"
                palette.buttonText:"white"
                    onClicked: { confirmDialog.targetName=name; confirmDialog.open() } }
            }
        }
        Label { visible: netModel.count===0
        text:"No networks found"
        color:"#9ca3af"
        anchors.centerIn: parent }
    }
    Dialog { id: createDialog
    modal: true
    anchors.centerIn: parent
    width: 360
    title: "Create Network"
        ColumnLayout { width: parent.width
        spacing: 12
            Label { text: "Name" }
            TextField { id: netName
            Layout.fillWidth: true
            placeholderText: "my-network" }
            Label { text: "Type" }
            ComboBox { id: netType
            Layout.fillWidth: true
            model: ["bridge","macvlan","sriov","ovn","physical"] }
            RowLayout { Layout.alignment: Qt.AlignRight
            spacing: 8
                Button { text:"Cancel"
                flat:true
                onClicked: createDialog.reject() }
                Button { text:"Create"
                highlighted:true
                onClicked: {
                    client.createNetwork({name:netName.text.trim(),type:netType.currentText})
                    reload(); createDialog.accept() } }
            }
        }
    }
    ConfirmDialog { id: confirmDialog; property string targetName:""
        title:"Delete network"
        message:`Delete "${targetName}"?`
        confirmLabel:"Delete"
        onConfirmed: { client.deleteNetwork(targetName); reload() }
    }
}
