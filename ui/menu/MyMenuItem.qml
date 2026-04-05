import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: menuItem
    width: parent.width
    height: 40
    color: "white"

    signal clicked

    property alias text: label.text
    property alias icon: icon.source
    property alias hovered: menu_itemHover.hovered

    property int index: -1

    RowLayout {
        anchors.fill: parent
        spacing: 10

        Image {
            id: icon
            Layout.alignment: Qt.AlignVCenter
            Layout.leftMargin: 10

            Layout.minimumWidth: 24
            Layout.maximumWidth: 24
            Layout.minimumHeight: 24
            Layout.maximumHeight: 24
            fillMode: Image.PreserveAspectFit
        }

        Text {
            id: label
            Layout.alignment: Qt.AlignVCenter
            Layout.rightMargin: 10
            Layout.fillWidth: true

            font.pixelSize: 16
            color: "black"
        }

        Item {
            Layout.fillWidth: true
        }
    }

    HoverHandler {
        id: menu_itemHover
        cursorShape: Qt.PointingHandCursor
    }

    TapHandler {
        id: menu_itemTap
        onTapped: menuItem.clicked()
    }
}