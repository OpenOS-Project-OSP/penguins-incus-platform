import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import PIP 1.0

Page {
    id: root
    required property var client
    title: "Virtual Machines"

    ListModel { id: vmModel }

    function reload() { client.listInstances("", "") }

    Connections {
        target: client
        function onInstancesListed(instances) {
            vmModel.clear()
            for (let i = 0; i < instances.length; i++) {
                const inst = instances[i]
                if (inst.type !== "virtual-machine") continue
                vmModel.append({
                    name: inst.name ?? "", status: inst.status ?? "Unknown",
                    image: inst.image ?? "", project: inst.project ?? "default",
                    cpu_usage: inst.cpu_usage ?? 0,
                    memory_usage_bytes: inst.memory_usage_bytes ?? 0,
                })
            }
        }
        function onInstanceStateChanged(name, status) {
            for (let i = 0; i < vmModel.count; i++) {
                if (vmModel.get(i).name === name) { vmModel.setProperty(i, "status", status); break }
            }
        }
        function onResourceUsageUpdated(usage) {
            for (let i = 0; i < vmModel.count; i++) {
                if (vmModel.get(i).name === usage.name) {
                    vmModel.setProperty(i, "cpu_usage", usage.cpu_usage)
                    vmModel.setProperty(i, "memory_usage_bytes", usage.memory_usage_bytes)
                    break
                }
            }
        }
        function onError(msg) { errorBar.text = msg; errorBar.visible = true }
    }

    Component.onCompleted: reload()

    header: ToolBar {
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 12
            anchors.rightMargin: 12
            Label { text: "Virtual Machines"
            font.pixelSize: 16
            font.bold: true }
            Item  { Layout.fillWidth: true }
            Button { text: "↻ Refresh"
            flat: true
            onClicked: reload() }
            Button {
                text: "+ Create"
                highlighted: true
                onClicked: createDialog.open()
            }
        }
    }

    Rectangle {
        id: errorBar; property string text: ""
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
        model: vmModel
        clip: true
        header: Row {
            width: parent.width
            height: 36
            Repeater {
                model: ["Name","Status","Image","Project","CPU","Memory","Actions"]
                Label {
                    width: [180,110,200,120,70,100,220][index]
                    height: 36
                    text: modelData
                    font.bold: true
                    color: "#374151"
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: 12
                }
            }
        }
        delegate: Rectangle {
            width: ListView.view.width
            height: 44
            color: index % 2 === 0 ? "transparent" : "#f9fafb"
            Row {
                anchors.verticalCenter: parent.verticalCenter
                Label { width:180
                text: name
                font.bold:true
                leftPadding:12
                elide:Text.ElideRight }
                StatusBadge { width:110
                status: model.status
                anchors.verticalCenter: parent.verticalCenter }
                Label { width:200
                text: image||"—"
                color:"#6b7280"
                font.pixelSize:13
                leftPadding:4
                elide:Text.ElideRight }
                Label { width:120
                text: project
                color:"#6b7280"
                leftPadding:4 }
                Label { width:70;  text: cpu_usage>0?(cpu_usage*100).toFixed(1)+"%":"—"
                color:"#6b7280"
                leftPadding:4 }
                Label { width:100
                text: memory_usage_bytes>0?(memory_usage_bytes/1048576).toFixed(0)+" MB":"—"
                color:"#6b7280"
                leftPadding:4 }
                Row {
                    spacing: 4
                    anchors.verticalCenter: parent.verticalCenter
                    Button { text:"Start";   visible: model.status==="Stopped";  flat:true
                    font.pixelSize:12
                    onClicked: client.startInstance(name, project) }
                    Button { text:"Stop";    visible: model.status==="Running";  flat:true
                    font.pixelSize:12
                    onClicked: client.stopInstance(name,false,project) }
                    Button { text:"Restart"
                    visible: model.status==="Running";  flat:true
                    font.pixelSize:12
                    onClicked: client.restartInstance(name,false,project) }
                    Button {
                        text:"Delete"
                        font.pixelSize:12
                        palette.button:"#ef4444"
                        palette.buttonText:"white"
                        onClicked: { confirmDialog.targetName=name; confirmDialog.targetProject=project; confirmDialog.open() }
                    }
                }
            }
        }
        Label { visible: vmModel.count===0
        text:"No virtual machines found"
        color:"#9ca3af"
        anchors.centerIn: parent }
    }

    CreateInstanceDialog {
        id: createDialog
        instanceType: "virtual-machine"
        onCreateRequested: (name, image, type) => { client.createInstance({name,image,type,profiles:["default"]}); reload() }
    }
    ConfirmDialog {
        id: confirmDialog; property string targetName:""; property string targetProject:""
        title:"Delete virtual machine"
        message:`Delete "${targetName}"? This cannot be undone.`
        confirmLabel:"Delete"
        onConfirmed: { client.deleteInstance(targetName,true,targetProject); reload() }
    }
}
