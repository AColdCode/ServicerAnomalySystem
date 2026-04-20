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
                text: "单指标态势预测"
                font.pixelSize: 30
                color: "black"
            }

            Text {
                Layout.leftMargin: 20
                text: "预测单个指标的未来趋势"
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
                DataManager.setPredictMetric(currentIndex)
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
            model: ["未来1小时", "未来6小时", "未来一天"]

            onCurrentIndexChanged: {
                if (currentIndex === 0) {
                    DataManager.setPredictRange(1)
                } else if (currentIndex === 1) {
                    DataManager.setPredictRange(6)
                } else if (currentIndex === 2) {
                    DataManager.setPredictRange(24)
                }
            }

            HoverHandler {
                cursorShape: Qt.PointingHandCursor
            }
        }

        Rectangle {
            id: predictButton
            Layout.preferredWidth: 100
            Layout.preferredHeight: 50
            Layout.rightMargin: 20
            color: "black"
            radius: 10

            Text {
                anchors.centerIn: parent
                text: "执行预测"
                font.pixelSize: 20
                color: "white"
            }

            HoverHandler {
                cursorShape: Qt.PointingHandCursor
            }

            TapHandler {
                onTapped: {
                    DataManager.singlePredict()
                }
            }
        }
    }
}