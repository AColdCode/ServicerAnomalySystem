import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: singleTop
    width: parent.width
    height: 50

    RowLayout {
        anchors.fill: parent
        spacing: 10

        ColumnLayout {
            Layout.preferredWidth: 120
            Layout.fillHeight: true

            Text {
                Layout.leftMargin: 20
                Layout.topMargin: 20
                text: "单指标异常检测"
                font.pixelSize: 30
                color: "black"
            }

            Text {
                Layout.leftMargin: 20
                text: "分析单个指标的异常情况"
                font.pixelSize: 20
                color: "grey"
            }
        }

        Item {
            Layout.fillWidth: true
        }

        ComboBox {
            id: selectMetric
            Layout.preferredWidth: 200
            Layout.preferredHeight: 50
            font.pixelSize: 20
            currentIndex: 0
            model: ["CPU使用率", "CPU响应时间", "内存使用率", "磁盘使用率", "磁盘读吞吐量", "磁盘写吞吐量", "服务器响应时间", "服务QPS"]

            onCurrentIndexChanged: {
                DataManager.setDetectMetric(currentIndex)
            }

            HoverHandler {
                cursorShape: Qt.PointingHandCursor
            }
        }

        ComboBox {
            id: selectTime
            Layout.preferredWidth: 150
            Layout.preferredHeight: 50
            Layout.rightMargin: 20
            font.pixelSize: 20
            currentIndex: 0
            model: ["最近1小时", "最近6小时", "最近一天", "最近7天"]

            onCurrentIndexChanged: {
                if (currentIndex === 0) {
                    DataManager.setDetectRange("1h")
                } else if (currentIndex === 1) {
                    DataManager.setDetectRange("6h")
                } else if (currentIndex === 2) {
                    DataManager.setDetectRange("1d")
                } else if (currentIndex === 3) {
                    DataManager.setDetectRange("7d")
                }
            }

            HoverHandler {
                cursorShape: Qt.PointingHandCursor
            }
        }
    }
}