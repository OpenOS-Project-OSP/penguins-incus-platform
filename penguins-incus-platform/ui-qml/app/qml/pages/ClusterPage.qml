import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import PIP 1.0

Page {
    id: root
    required property var client
    title: "Cluster"
    ListModel { id: memberModel }
    function reload() { client.listClusterMembers() }
    Connections {
        target: client
        function onClusterMembersListed(members) {
            memberModel.clear()
            for (let i = 0; i < members.length; i++) {
                const m = members[i]
                memberModel.append({ name:m.name??"", url:m.url??"", status:m.status??"Unknown",
                    roles:(m.roles??[]).join(", "), architecture:m.architecture??"" })
            }
        }
        function onError(msg) { errorBar.text = msg; errorBar.visible = true }
    }
    Component.onCompleted: reload()
    header: ToolBar {
        RowLayout { anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 12
            Label { text: "Cluster"
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
        model: memberModel
        clip: true
        header: Row { height: 36
            Repeater { model: ["Name","URL","Status","Roles","Architecture","Actions"]
                Label { width:[160,260,110,160,120,200][index]
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
                Label { width:260
                text:url
                color:"#6b7280"
                font.pixelSize:11
                font.family:"monospace"
                leftPadding:4
                elide:Text.ElideRight }
                StatusBadge { width:110
                status:model.status
                anchors.verticalCenter:parent.verticalCenter }
                Label { width:160
                text:roles||"—"
                color:"#6b7280"
                font.pixelSize:13
                leftPadding:4 }
                Label { width:120
                text:architecture||"—"
                color:"#6b7280"
                leftPadding:4 }
                Row { spacing:4
                anchors.verticalCenter:parent.verticalCenter
                    Button { visible:model.status==="Online"
                    text:"Evacuate"
                    flat:true
                    font.pixelSize:12
                    onClicked:{ client.evacuateClusterMember(name); reload() } }
                    Button { visible:model.status==="Evacuated"
                    text:"Restore"
                    flat:true
                    font.pixelSize:12
                    onClicked:{ client.restoreClusterMember(name); reload() } }
                    Button { text:"Remove"
                    font.pixelSize:12
                    palette.button:"#ef4444"
                    palette.buttonText:"white"
                        onClicked:{ confirmDialog.targetName=name; confirmDialog.open() } }
                }
            }
        }
        Label { visible: memberModel.count===0
        text:"No cluster members (standalone mode)"
        color:"#9ca3af"
        anchors.centerIn: parent }
    }
    ConfirmDialog { id: confirmDialog; property string targetName:""
        title:"Remove cluster member"
        message:`Remove "${targetName}" from cluster?`
        confirmLabel:"Remove"
        onConfirmed: { client.removeClusterMember(targetName); reload() }
    }
}
