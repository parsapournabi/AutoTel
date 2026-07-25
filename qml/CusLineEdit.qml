import QtQuick 2.12
import QtQuick.Controls 2.12

TextField {
    id: control

    property int level: 0

    property color backgroundColor: global.paneBackgroundColor[level]
    property color borderColor: global.paneBorderColor[level]

    placeholderText: qsTr("Enter description")

    background: Rectangle {
        implicitWidth: 200
        implicitHeight: 40
        color: control.enabled ? "transparent" : borderColor
        border.color: control.enabled ? borderColor : "transparent"
    }
}
