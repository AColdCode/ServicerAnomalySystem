import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "sysManage"

ScrollView {
    id: systemManage
    anchors.fill: parent

    property int index: -1

    contentItem: Flickable {
        id: mainInterface
        contentWidth: parent.width
        contentHeight: 1000

        ColumnLayout {
            anchors.fill: parent

            Text {
                Layout.leftMargin: 20
                Layout.topMargin: 20
                text: "用户管理"
                font.pixelSize: 30
                color: "black"
            }

            Text {
                Layout.leftMargin: 20
                text: "管理系统用户和权限"
                font.pixelSize: 20
                color: "grey"
            }

            UserList {
                id: userList
                Layout.fillWidth: true
                Layout.preferredHeight: 600
                Layout.leftMargin: 20
                Layout.rightMargin: 20
                color: "white"
            }

            BottomRt {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.leftMargin: 20
                Layout.rightMargin: 20
                Layout.bottomMargin: 20
                Layout.topMargin: 20
                color: "white"
            }
        }
    }
}
