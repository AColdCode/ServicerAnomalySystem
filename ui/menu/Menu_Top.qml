import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

Rectangle {
    id: topMenu
    width: parent.width
    height: 50
    color: "#F9FAFB"

    property bool exitCliked: false

    RowLayout {
        anchors.fill: parent
        spacing: 10

        Text {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter
            horizontalAlignment: Text.AlignHCenter
            text: "监控系统"
            font.pixelSize: 25
            color: "black"
            font.bold: true
        }

        Rectangle {
            id: exitBtn
            Layout.preferredWidth: 30
            Layout.preferredHeight: 30
            color: exit_hover.hovered ? "#D4E0ED" : "#F9FAFB"
            radius: 5

            Image {
                anchors.fill: parent
                fillMode: Image.PreserveAspectFit
                source: "../../images/exit.svg"
            }

            HoverHandler {
                id: exit_hover
                cursorShape: Qt.PointingHandCursor
            }

            TapHandler {
                id: exit_tap
                onTapped: {
                    topMenu.exitCliked = !topMenu.exitCliked
                }
            }

            // 阴影效果
            layer.enabled: true
            layer.effect: MultiEffect {
                shadowEnabled: exit_hover.hovered
                shadowBlur: 0.8
                shadowColor: "#80000000"
                shadowVerticalOffset: 4
            }
        }

        Item {
            width: 10
        }
    }

    Rectangle {
        anchors.bottom: parent.bottom
        height: 1
        width: parent.width
        color: "grey"
    }
}