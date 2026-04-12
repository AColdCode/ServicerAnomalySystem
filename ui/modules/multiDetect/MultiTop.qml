import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: multiTop
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
                text: "多指标异常检测"
                font.pixelSize: 30
                color: "black"
            }

            Text {
                Layout.leftMargin: 20
                text: "同时分析多个指标的异常情况"
                font.pixelSize: 20
                color: "grey"
            }
        }

        Item {
            Layout.fillWidth: true
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
                    DataManager.setMultiDetectRange("1h")
                } else if (currentIndex === 1) {
                    DataManager.setMultiDetectRange("6h")
                } else if (currentIndex === 2) {
                    DataManager.setMultiDetectRange("1d")
                } else if (currentIndex === 3) {
                    DataManager.setMultiDetectRange("7d")
                }
            }

            HoverHandler {
                cursorShape: Qt.PointingHandCursor
            }
        }
    }
}