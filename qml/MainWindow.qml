import QtQuick 2.12
import QtQuick.Layouts 1.12
import Qt.labs.platform 1.1 as QL
import com.wearily.WeaQuick 1.0 as WeaQuick

Item {
    id: root

    ColumnLayout {
        anchors {
            fill: parent
            margins: 10
        }

        // Header
        WeaQuick.WaveText {
            frequency: 18
            amplitude: 0.01
            font {
                pixelSize: 20
                italic: true
            }
            text: qsTr("WeaTel")
        }

        // Main
        WeaQuick.Pane {
            Layout.fillWidth: true
            Layout.fillHeight: true
            level: 1
            flat: false

            ColumnLayout {
                anchors {
                    fill: parent
                    topMargin: 25
                    margins: 15
                }
                spacing: 10

                RowLayout {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 40
                    WeaQuick.LineEdit {
                        id: lineEditFolderPath
                        Layout.fillWidth: true
                        Layout.preferredWidth: 75
                        Layout.preferredHeight: 40
                        level: 2
                        placeholderText: "Path/To/Your/Folder"
                        text: folderDialog.currentFolder
                        font {
                            pixelSize: 16
                        }
                    }

                    WeaQuick.Button {
                        id: btnBrowse
                        Layout.fillWidth: true
                        Layout.preferredWidth: 25
                        Layout.preferredHeight: 40
                        level: 2
                        flat: false
                        font {
                            pixelSize: 16
                        }

                        text: "Browse"
                        onClicked: folderDialog.open()
                    }
                }

                Item {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 10
                }

                WeaQuick.Label {
                    Layout.preferredWidth: lineEditFolderPath.width
                    font.pixelSize: 16
                    horizontalAlignment: Qt.AlignHCenter
                    text: "Telegram Login"
                }

                RowLayout {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 40
                    spacing: 20

                    WeaQuick.LineEdit {
                        id: lineEditPhoneNumber
                        Layout.preferredWidth: lineEditFolderPath.width
                        Layout.preferredHeight: 40
                        level: 2
                        placeholderText: "+98-9381234567"
                        horizontalAlignment: Qt.AlignHCenter
                        font {
                            pixelSize: 16
                        }
                    }

                    Item {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 40
                        CusBusyIndicator {
                            id: busyIndicator
                            anchors.verticalCenter: parent.verticalCenter
                            running: true
                            scale: 0.6
                        }
                    }
                }

                WeaQuick.LineEdit {
                    id: lineEditSecurityCode
                    Layout.preferredWidth: lineEditFolderPath.width
                    Layout.preferredHeight: 40
                    // visible: false
                    level: 2
                    placeholderText: "XXXXX"
                    horizontalAlignment: Qt.AlignHCenter
                    font {
                        pixelSize: 16
                    }
                }

                WeaQuick.LineEdit {
                    id: lineEdit2FA
                    Layout.preferredWidth: lineEditFolderPath.width
                    Layout.preferredHeight: 40
                    visible: false
                    level: 2
                    placeholderText: "2FA"
                    horizontalAlignment: Qt.AlignHCenter
                    font {
                        pixelSize: 16
                    }
                }

                WeaQuick.Button {
                    id: btnLogin
                    Layout.preferredWidth: lineEditFolderPath.width
                    Layout.preferredHeight: 40
                    level: 2
                    flat: false
                    text: "Login"
                    font {
                        pixelSize: 16
                    }
                }

                // Spacer
                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                }
            }
        }

        // Footer
        Footer {
            Layout.fillWidth: true
            Layout.preferredHeight: paintedHeight

            text: qsTr(" Developed by wearily on July, 28, 2026 ")
        }
    }

    // Popup
    QL.FolderDialog {
        id: folderDialog
    }

    // Resources
    WeaQuick.GlobalContext {
        id: wQuick
    }
}
