import QtQuick 2.12
import QtQuick.Window 2.12

Window {
    id: appWindow
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

    Connections {
        target: _main
        function onRequestWindowVisible(vis) {
            appWindow.visible = vis;
        }
    }
}
