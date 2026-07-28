import QtQuick 2.12
import QtQuick.Window 2.12

Window {
    width: 550
    height: 490
    visible: true
    title: "AutoTel"
    color: "black"

    MainWindow {
        anchors.fill: parent
    }

    GlobalContext {
        id: global
    }
}
