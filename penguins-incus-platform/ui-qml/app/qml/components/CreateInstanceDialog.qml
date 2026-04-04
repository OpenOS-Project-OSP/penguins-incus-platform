import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: root
    modal: true
    anchors.centerIn: parent
    width: 400
    title: "Create Container"

    property string instanceType: "container"

    signal createRequested(string name, string image, string type)

    ColumnLayout {
        width: parent.width
        spacing: 12

        Label { text: "Name" }
        TextField {
            id: nameField
            Layout.fillWidth: true
            placeholderText: "my-container"
        }

        Label { text: "Image" }
        TextField {
            id: imageField
            Layout.fillWidth: true
            text: "images:ubuntu/24.04"
        }

        Label {
            text: errorLabel.text
            id: errorLabel
            color: "#ef4444"
            visible: text.length > 0
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
        }

        RowLayout {
            Layout.alignment: Qt.AlignRight
            spacing: 8

            Button {
                text: "Cancel"
                flat: true
                onClicked: { errorLabel.text = ""; root.reject() }
            }
            Button {
                text: "Create"
                highlighted: true
                onClicked: {
                    if (!nameField.text.trim()) {
                        errorLabel.text = "Name is required"
                        return
                    }
                    errorLabel.text = ""
                    root.createRequested(nameField.text.trim(),
                                         imageField.text.trim(),
                                         root.instanceType)
                    root.accept()
                }
            }
        }
    }
}
