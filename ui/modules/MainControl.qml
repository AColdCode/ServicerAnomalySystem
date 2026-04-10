import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "dataManage"

ScrollView {
    id: mainControl
    anchors.fill: parent

    property int index: -1

    contentItem: Flickable {
        id: mainInterface
        contentWidth: parent.width
        contentHeight: 1200

        ColumnLayout {
            anchors.fill: parent

            Text {
                Layout.leftMargin: 20
                Layout.topMargin: 20
                text: "主控台"
                font.pixelSize: 30
                color: "black"
            }

            Text {
                Layout.leftMargin: 20
                text: "系统运行状态总览"
                font.pixelSize: 20
                color: "grey"
            }

            Item {
                Layout.fillHeight: true
            }
        }
    }
}
