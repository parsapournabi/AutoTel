import QtQuick 2.12
import QtQuick.Window 2.12

Window {
    width: 250
    height: 380
    visible: true
    title: "AutoTel"

    MainWindow {
        anchors.fill: parent
    }

    GlobalContext {
        id: global
    }
}
