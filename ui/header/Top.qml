import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

ToolBar {
    id: top

    property bool menu_opened: false
    property string prefix: "A"

    background: Rectangle {
        color: "#F9FAFB"

        Rectangle {
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            height: 1
            color: "grey"
        }
    }

    RowLayout {
        anchors.fill: parent
        spacing: 10

        Item {
            width: 10
        }

        Rectangle {
            id: menuBtn
            Layout.preferredWidth: 40
            Layout.preferredHeight: 40
            color: menu_hover.hovered ? "#D4E0ED" : "#F9FAFB"
            radius: 10

            Image {
                anchors.fill: parent
                fillMode: Image.PreserveAspectFit
                source: "../../images/menu.svg"
            }

            HoverHandler {
                id: menu_hover
                cursorShape: Qt.PointingHandCursor
            }

            TapHandler {
                id: menu_tap
                onTapped: {
                    top.menu_opened = !top.menu_opened
                }
            }

            // 阴影效果
            layer.enabled: true
            layer.effect: MultiEffect {
                shadowEnabled: menu_hover.hovered
                shadowBlur: 0.8
                shadowColor: "#80000000"
                shadowVerticalOffset: 4
            }
        }

        Text {
            Layout.fillWidth: true
            text: "态势预测与异常检测系统"
            font.pixelSize: 20
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        Rectangle {
            id: userBtn
            Layout.preferredWidth: 40
            Layout.preferredHeight: 40
            radius: 25
            color: "#3C83F6"

            // 阴影效果
            layer.enabled: true
            layer.effect: MultiEffect {
                shadowEnabled: user_hover.hovered
                shadowBlur: 0.8
                shadowColor: "#80000000"
                shadowVerticalOffset: 4
            }

            Text {
                anchors.centerIn: parent
                text: prefix
                font.pixelSize: 30
                color: "white"
            }

            HoverHandler {
                id: user_hover
                cursorShape: Qt.PointingHandCursor
            }

            TapHandler {
                id: user_tap
                onTapped: {
                    user_popup.open()
                }
            }

            UserPopup {
                id: user_popup
            }
        }

        Item {
            width: 10
        }
    }

    Connections {
        target: DataManager

        function onLoginSuccess(username, role) {
            user_popup.userName = username

            if (role === "admin") {
                user_popup.userRole = "管理员"
            } else {
                user_popup.userRole = "普通用户"
            }

            let firstLetter = username[0]
            if (firstLetter >= 'a' && firstLetter <= 'z') {
                firstLetter = firstLetter.toUpperCase()
            }
            top.prefix = firstLetter
        }
    }
}