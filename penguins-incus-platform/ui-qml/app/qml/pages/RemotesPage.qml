import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import PIP 1.0

Page {
    id: root
    required property var client
    title: "Remotes"
    ListModel { id: remoteModel }
    function reload() { client.listRemotes() }
    Connections {
        target: client
        function onRemotesListed(remotes) {
            remoteModel.clear()
            for (let i = 0; i < remotes.length; i++) {
                const r = remotes[i]
                remoteModel.append({ name:r.name??"", url:r.url??"", protocol:r.protocol??"incus" })
            }
        }
        function onError(msg) { errorBar.text = msg; errorBar.visible = true }
    }
    Component.onCompleted: reload()
    header: ToolBar {
        RowLayout { anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 12
            Label { text: "Remotes"
            font.pixelSize: 16
            font.bold: true }
            Item { Layout.fillWidth: true }
            Button { text: "↻ Refresh"
            flat: true
            onClicked: reload() }
            Button { text: "+ Add"
            highlighted: true
            onClicked: addDialog.open() }
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
        model: remoteModel
        clip: true
        header: Row { height: 36
            Repeater { model: ["Name","URL","Protocol","Actions"]
                Label { width:[160,360,100,200][index]
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
                Label { width:160
                text:name
                font.bold:true
                leftPadding:12 }
                Label { width:360
                text:url
                color:"#6b7280"
                font.pixelSize:11
                font.family:"monospace"
                leftPadding:4
                elide:Text.ElideRight }
                Label { width:100
                text:protocol
                color:"#6b7280"
                leftPadding:4 }
                Row { spacing:4
                anchors.verticalCenter:parent.verticalCenter
                    Button { text:"Activate"
                    flat:true
                    font.pixelSize:12
                    onClicked:{ client.activateRemote(name); reload() } }
                    Button { visible:name!=="local"
                    text:"Remove"
                    font.pixelSize:12
                    palette.button:"#ef4444"
                    palette.buttonText:"white"
                        onClicked:{ confirmDialog.targetName=name; confirmDialog.open() } }
                }
            }
        }
        Label { visible: remoteModel.count===0
        text:"No remotes configured"
        color:"#9ca3af"
        anchors.centerIn: parent }
    }
    Dialog { id: addDialog
    modal: true
    anchors.centerIn: parent
    width: 420
    title: "Add Remote"
        ColumnLayout { width: parent.width
        spacing: 12
            Label { text: "Name" }
            TextField { id: rName
            Layout.fillWidth: true
            placeholderText: "my-server" }
            Label { text: "URL" }
            TextField { id: rUrl
            Layout.fillWidth: true
            text: "https://" }
            RowLayout { Layout.alignment: Qt.AlignRight
            spacing: 8
                Button { text:"Cancel"
                flat:true
                onClicked: addDialog.reject() }
                Button { text:"Add"
                highlighted:true
                onClicked: {
                    client.addRemote({name:rName.text.trim(),url:rUrl.text.trim(),protocol:"incus"})
                    reload(); addDialog.accept() } }
            }
        }
    }
    ConfirmDialog { id: confirmDialog; property string targetName:""
        title:"Remove remote"
        message:`Remove remote "${targetName}"?`
        confirmLabel:"Remove"
        onConfirmed: { client.removeRemote(targetName); reload() }
    }
}
