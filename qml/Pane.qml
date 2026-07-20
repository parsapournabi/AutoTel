import QtQuick 2.12

Rectangle {
    id: root

    property int level: 0

    radius: 8
    color: global.paneBackgroundColor[level]
    border.color: global.paneBorderColor[level]
}
