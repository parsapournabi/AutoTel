import QtQuick 2.12
import QtQuick.Window 2.12

Window {
    width: 800
    height: 600
    visible: true
    title: "AutoTel"

    Rectangle {
        anchors.fill: parent
        color: "#202020"

        Text {
            anchors.centerIn: parent
            text: "Hello AutoTel"
            color: "white"
            font.pixelSize: 30
        }
    }
}
