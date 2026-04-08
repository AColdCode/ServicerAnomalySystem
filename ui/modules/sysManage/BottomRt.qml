import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    width: parent.width
    height: 50
    color: "white"
    radius: 10
    border.color: "grey"
    border.width: 1

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        Text {
            Layout.leftMargin: 10
            text: "说明"
            color: "black"
            font.pixelSize: 20
        }

        Text {
            Layout.leftMargin: 10
            text: "• 第一个注册的用户将自动成为管理员\n" +
                "\n" +
                "• 管理员可以修改其他用户的角色和状态\n" +
                "\n" +
                "• 不能修改自己的角色和状态\n" +
                "\n" +
                "• 禁用的用户无法登录系统\n" +
                "\n" +
                "• 管理员的上级管理员可以将其降为普通用户\n" +
                "\n" +
                "• 新用户请在登录页面自行注册"
            color: "grey"
            font.pixelSize: 12
        }

        Item {
            Layout.fillHeight: true
        }
    }
}