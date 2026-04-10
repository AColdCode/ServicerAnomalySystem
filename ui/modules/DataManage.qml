import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "dataManage"

ScrollView {
    id: dataManage
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
                text: "数据管理"
                font.pixelSize: 30
                color: "black"
            }

            Text {
                Layout.leftMargin: 20
                text: "生成和管理监控数据"
                font.pixelSize: 20
                color: "grey"
            }

            DataStat {
                id: dataStat
                Layout.fillWidth: true
                Layout.preferredHeight: 180
                Layout.leftMargin: 20
                Layout.rightMargin: 20
            }

            MonitorDataGen {
                id: dataGen
                Layout.fillWidth: true
                Layout.preferredHeight: 600
                Layout.leftMargin: 20
                Layout.rightMargin: 20
                Layout.topMargin: 20
            }

            DataClear {
                id: dataClear
                Layout.fillWidth: true
                Layout.preferredHeight: 250
                Layout.leftMargin: 20
                Layout.rightMargin: 20
                Layout.topMargin: 20
            }

            Item {
                Layout.fillHeight: true
            }
        }
    }
}
