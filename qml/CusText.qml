import QtQuick 2.12

Text {
    id: root

    property int level: 0

    // font: global.defaultFont
    color: global.textColor[level]
}
