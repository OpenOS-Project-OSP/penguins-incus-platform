import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: root
    modal: true
    anchors.centerIn: parent
    width: 360

    property string message: ""
    property string confirmLabel: "Confirm"

    signal confirmed()

    title: title

    ColumnLayout {
        width: parent.width
        spacing: 16

        Label {
            text: root.message
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
            color: palette.text
        }

        RowLayout {
            Layout.alignment: Qt.AlignRight
            spacing: 8

            Button {
                text: "Cancel"
                flat: true
                onClicked: root.reject()
            }
            Button {
                text: root.confirmLabel
                palette.button: "#ef4444"
                palette.buttonText: "white"
                onClicked: { root.confirmed(); root.accept() }
            }
        }
    }
}
