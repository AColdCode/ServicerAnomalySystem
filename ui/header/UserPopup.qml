import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: popup
    x: - width + parent.width / 2
    y: parent.height
    width: 150
    height: 110
    modal: false

    property string userName: ""
    property string userRole: ""

    background: Rectangle {
        color: "white"
        border.color: "grey"
        border.width: 1
        radius: 5
    }

    ColumnLayout {
        anchors.fill: parent

        Rectangle {
            Layout.preferredHeight: 40
            Layout.fillWidth: true
            color: "white"

            ColumnLayout {
                anchors.fill: parent
                spacing: 0

                Text {
                    width: parent.width
                    text: userName
                    font.pixelSize: 15
                    color: "black"
                }

                Text {
                    width: parent.width
                    text: userRole
                    font.pixelSize: 15
                    color: "#6B7B90"
                }
            }

            Rectangle {
                width: parent.width
                height: 1
                color: "grey"
                anchors.bottom: parent.bottom
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.leftMargin: 5
            Layout.rightMargin: 5
            Layout.topMargin: 5
            Layout.bottomMargin: 5
            Layout.preferredHeight: 40
            color: popupHover.hovered ? "#D4E0ED" : "white"

            RowLayout {
                anchors.fill: parent
                spacing: 10

                Image {
                    Layout.alignment: Qt.AlignVCenter
                    Layout.leftMargin: 10

                    Layout.minimumWidth: 24
                    Layout.maximumWidth: 24
                    Layout.minimumHeight: 24
                    Layout.maximumHeight: 24
                    fillMode: Image.PreserveAspectFit

                    source: RESOURCE_PATH + "images/back.svg"
                }

                Text {
                    Layout.alignment: Qt.AlignVCenter
                    Layout.rightMargin: 10
                    Layout.fillWidth: true

                    font.pixelSize: 16
                    color: "black"

                    text: "退出登录"
                }

                Item {
                    Layout.fillWidth: true
                }
            }

            HoverHandler {
                id: popupHover
                cursorShape: Qt.PointingHandCursor
            }

            TapHandler {
                id: menu_itemTap
                onTapped: {
                    DataManager.logout()
                    popup.close()
                }
            }
        }
    }
}