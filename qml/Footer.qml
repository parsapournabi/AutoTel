import QtQuick 2.12
import com.wearily.WeaQuick 1.0 as WeaQuick

Item {
    id: root

    property int animationInterval: 750
    property alias text: label.text

    readonly property alias paintedHeight: label.paintedHeight
    readonly property alias paintedWidth: label.paintedWidth
    readonly property alias contentHeight: label.contentHeight
    readonly property alias contentWidth: label.contentWidth

    property alias label: label
    property alias palette: palette

    clip: true

    WeaQuick.Label {
        id: label
        anchors.fill: parent

        horizontalAlignment: Qt.AlignHCenter

        Component.onCompleted: {
            _private.defaultText = text;
            _private.defaultPaintedWidth = paintedWidth;
            addPrefixAndSuffix(this);
        }

        SequentialAnimation on color {
            id: grad

            running: true
            loops: SequentialAnimation.Infinite

            ColorAnimation {
                from: palette.colors[0]
                to: palette.colors[1]
                duration: animationInterval
                easing.type: Easing.InOutQuad
            }

            ColorAnimation {
                from: palette.colors[1]
                to: palette.colors[2]
                duration: animationInterval
                easing.type: Easing.InOutQuad
            }

            ColorAnimation {
                from: palette.colors[2]
                to: palette.colors[3]
                duration: animationInterval
                easing.type: Easing.InOutQuad
            }

            ColorAnimation {
                from: palette.colors[3]
                to: palette.colors[4]
                duration: animationInterval
                easing.type: Easing.InOutQuad
            }
        }
    }

    QtObject {
        id: _private
        property string defaultText: ""
        property real defaultPaintedWidth
    }

    QtObject {
        id: palette
        property var colors: ["#7B61FF", "#FF4EBD", "#00DDD1", "#FF924A", "#F2F2F2"]
    }

    function addPrefixAndSuffix(target) {
        var text = _private.defaultText;

        const remainPixels = target.width - _private.defaultPaintedWidth;
        const offset = -100;
        const repeatCount = Math.floor(remainPixels / 20) - offset;

        const prefix = "\\".repeat(repeatCount);
        const suffix = "/".repeat(repeatCount);

        target.text = prefix + text + suffix;
    }
}
