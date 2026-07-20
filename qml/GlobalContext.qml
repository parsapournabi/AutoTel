import QtQuick 2.12

QtObject {
    id: root

    property var backgroundColor: ["#202020"]
    property var paneBackgroundColor: ["#202020"]
    property var paneBorderColor: darker(paneBackgroundColor, 1.75)

    /** Functions **/

    function darker(colors, factor) {
        return colors.map(color => Qt.darker(color, factor));
    }
}
