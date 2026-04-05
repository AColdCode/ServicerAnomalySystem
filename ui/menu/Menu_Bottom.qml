import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: menu_bottom
    width: parent.width
    height: 50
    color: "#F9FAFB"

    property string userName: "用户名"
    property string userRole: "角色"
    property string prefix: "A"

    Rectangle {
        anchors.top: parent.top
        width: parent.width
        height: 1
        color: "grey"
    }

    RowLayout {
        anchors.fill: parent
        spacing: 10

        Item {
            Layout.preferredWidth: 10
        }

        Rectangle {
            id: userBtn
            Layout.preferredWidth: 40
            Layout.preferredHeight: 40
            radius: 25
            color: "#3C83F6"

            Text {
                anchors.centerIn: parent
                text: prefix
                font.pixelSize: 30
                color: "white"
            }
        }

        ColumnLayout {
            Layout.preferredWidth: 100
            spacing: 2
            Layout.fillHeight: true

            Text {
                Layout.fillWidth: true
                text: userName
                font.pixelSize: 10
                color: "black"
            }

            Text {
                Layout.fillWidth: true
                text: userRole
                font.pixelSize: 10
                color: "#6B7B90"
            }
        }

        Item {
            Layout.fillWidth: true
        }
    }

    Connections {
        target: DataManager

        function onLoginSuccess(username, role) {
            menu_bottom.userName = username
            if (role === "admin") {
                menu_bottom.userRole = "管理员"
            } else {
                menu_bottom.userRole = "普通用户"
            }

            let firstLetter = username[0]
            if (firstLetter >= 'a' && firstLetter <= 'z') {
                firstLetter = firstLetter.toUpperCase()
            }
            menu_bottom.prefix = firstLetter
        }
    }
}
