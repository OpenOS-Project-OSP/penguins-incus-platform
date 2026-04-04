import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import PIP 1.0

Page {
    id: root
    required property var client
    title: "Profiles"
    ListModel { id: profileModel }
    ListModel { id: presetModel }
    function reload() { client.listProfiles(""); client.listProfilePresets() }
    Connections {
        target: client
        function onProfilesListed(profiles) {
            profileModel.clear()
            for (let i = 0; i < profiles.length; i++) {
                const p = profiles[i]
                profileModel.append({ name:p.name??"", description:p.description??"" })
            }
        }
        function onError(msg) { errorBar.text = msg; errorBar.visible = true }
    }
    Component.onCompleted: reload()
    header: ToolBar {
        RowLayout { anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 12
            Label { text: "Profiles"
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
    ColumnLayout {
        anchors { top: errorBar.bottom
        left: parent.left
        right: parent.right
        bottom: parent.bottom
        margins: 16 }
        spacing: 16
        Label { text: "Preset Library"
        font.pixelSize: 14
        font.bold: true }
        Flow { Layout.fillWidth: true
        spacing: 8
            Repeater { model: presetModel
                Button { text: "+ " + name + " (" + category + ")"
                font.pixelSize: 12
                    onClicked: { client.createProfile(JSON.parse(profile_json)); reload() }
                }
            }
        }
        Label { text: "Installed Profiles"
        font.pixelSize: 14
        font.bold: true }
        ListView { Layout.fillWidth: true
        Layout.fillHeight: true
        model: profileModel
        clip: true
            header: Row { height: 36
                Repeater { model: ["Name","Description","Actions"]
                    Label { width:[200,400,120][index]
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
                    Label { width:200
                    text:name
                    font.bold:true
                    leftPadding:12 }
                    Label { width:400
                    text:description||"—"
                    color:"#6b7280"
                    font.pixelSize:13
                    leftPadding:4
                    elide:Text.ElideRight }
                    Button { visible: name!=="default"
                    text:"Delete"
                    font.pixelSize:12
                    palette.button:"#ef4444"
                    palette.buttonText:"white"
                        onClicked: { confirmDialog.targetName=name; confirmDialog.open() } }
                }
            }
            Label { visible: profileModel.count===0
            text:"No profiles found"
            color:"#9ca3af"
            anchors.centerIn: parent }
        }
    }
    ConfirmDialog { id: confirmDialog; property string targetName:""
        title:"Delete profile"
        message:`Delete "${targetName}"?`
        confirmLabel:"Delete"
        onConfirmed: { client.deleteProfile(targetName); reload() }
    }
}
