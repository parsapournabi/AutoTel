import QtQuick 2.12
import QtQuick.Controls 2.12 as Q

Q.Button {
    id: root

    property alias labelText: labelText
    property alias backgroundPane: bgPane
    implicitWidth: 120
    implicitHeight: 40

    background: Pane {
        id: bgPane
        implicitWidth: 100
        implicitHeight: 30
    }

    contentItem: CusText {
        id: labelText
        text: root.text
        font: root.font
        opacity: enabled ? 1.0 : 0.3
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRigh
    }
}
