import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Drawer{
    id: drawer
    width: 300
    height: parent.height
    edge: Qt.LeftEdge // 从左侧弹出

    property alias currentMenu: menus.currentIndex

    background: Rectangle {
        color: "#F9FAFB"
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        Menu_Top {
            id: topMenu
            Layout.fillWidth: true

            onExitClikedChanged: {
                drawer.close()
            }
        }

        Menus {
            id: menus
            Layout.fillWidth: true
            currentIndex: 1
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        Menu_Bottom {
            id: bottomMenu
            Layout.fillWidth: true
            Layout.preferredHeight: 50
        }
    }
}