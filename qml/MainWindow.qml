import QtQuick 2.12
import QtQuick.Layouts 1.12

Item {
    id: root

    ColumnLayout {
        anchors {
            fill: parent
            margins: 10
        }

        ProfileImage {
            id: profileImage
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        CusLineEdit {
            id: txtPhoneNumber
            Layout.fillWidth: true
            Layout.fillHeight: true
            placeholderText: "+98-1234567"
        }

        CusButton {
            id: btnLogin
            Layout.fillWidth: true
            Layout.fillHeight: true
            text: "Login"
        }
    }
}
