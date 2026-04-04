import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import PIP 1.0

Page {
    id: root
    required property var client
    title: "Images"
    ListModel { id: imgModel }
    function reload() { client.listImages("") }
    Connections {
        target: client
        function onImagesListed(images) {
            imgModel.clear()
            for (let i = 0; i < images.length; i++) {
                const img = images[i]
                imgModel.append({ fingerprint:img.fingerprint??"", description:img.description??"",
                    os:img.os??"", release:img.release??"", architecture:img.architecture??"",
                    size_bytes:img.size_bytes??0 })
            }
        }
        function onError(msg) { errorBar.text = msg; errorBar.visible = true }
    }
    Component.onCompleted: reload()
    header: ToolBar {
        RowLayout { anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 12
            Label { text: "Images"
            font.pixelSize: 16
            font.bold: true }
            Item { Layout.fillWidth: true }
            Button { text: "↻ Refresh"
            flat: true
            onClicked: reload() }
            Button { text: "↓ Pull"
            highlighted: true
            onClicked: pullDialog.open() }
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
        model: imgModel
        clip: true
        header: Row { height: 36
            Repeater { model: ["Fingerprint","Description","OS","Release","Arch","Size","Actions"]
                Label { width:[130,220,80,80,80,90,100][index]
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
                Label { width:130
                text:fingerprint.slice(0,12)+"…"
                font.family:"monospace"
                font.pixelSize:12
                leftPadding:12 }
                Label { width:220
                text:description
                leftPadding:4
                elide:Text.ElideRight }
                Label { width:80;  text:os||"—"
                color:"#6b7280"
                leftPadding:4 }
                Label { width:80;  text:release||"—"
                color:"#6b7280"
                leftPadding:4 }
                Label { width:80;  text:architecture||"—"
                color:"#6b7280"
                leftPadding:4 }
                Label { width:90;  text:size_bytes>0?(size_bytes/1048576).toFixed(0)+" MB":"—"
                color:"#6b7280"
                leftPadding:4 }
                Button { text:"Delete"
                font.pixelSize:12
                palette.button:"#ef4444"
                palette.buttonText:"white"
                    onClicked: { confirmDialog.targetFp=fingerprint; confirmDialog.open() } }
            }
        }
        Label { visible: imgModel.count===0
        text:"No images found"
        color:"#9ca3af"
        anchors.centerIn: parent }
    }
    Dialog { id: pullDialog
    modal: true
    anchors.centerIn: parent
    width: 380
    title: "Pull Image"
        ColumnLayout { width: parent.width
        spacing: 12
            Label { text: "Remote" }
            TextField { id: pullRemote
            Layout.fillWidth: true
            text: "images" }
            Label { text: "Image" }
            TextField { id: pullImage
            Layout.fillWidth: true
            text: "ubuntu/24.04" }
            Label { text: "Alias (optional)" }
            TextField { id: pullAlias
            Layout.fillWidth: true }
            RowLayout { Layout.alignment: Qt.AlignRight
            spacing: 8
                Button { text:"Cancel"
                flat:true
                onClicked: pullDialog.reject() }
                Button { text:"Pull"
                highlighted:true
                onClicked: {
                    client.pullImage(pullRemote.text.trim(), pullImage.text.trim(), pullAlias.text.trim())
                    reload(); pullDialog.accept() } }
            }
        }
    }
    ConfirmDialog { id: confirmDialog; property string targetFp:""
        title:"Delete image"
        message:`Delete image ${targetFp.slice(0,12)}…?`
        confirmLabel:"Delete"
        onConfirmed: { client.deleteImage(targetFp); reload() }
    }
}
