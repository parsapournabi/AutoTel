import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    width: 800
    height: 600
    visible: true
    title: "Hello PyQt5"

    Rectangle {
        anchors.fill: parent
        color: "#202020"

        Text {
            anchors.centerIn: parent
            text: "Hello QML"
            color: "white"
            font.pixelSize: 30
        }
    }
}
