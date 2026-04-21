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
                text: "多指标态势预测"
                font.pixelSize: 30
                color: "black"
            }

            Text {
                Layout.leftMargin: 20
                text: "预测多个指标的未来趋势"
                font.pixelSize: 20
                color: "grey"
            }
        }

        Item {
            Layout.fillWidth: true
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
                text: "批量预测"
                font.pixelSize: 20
                color: "white"
            }

            HoverHandler {
                cursorShape: Qt.PointingHandCursor
            }

            TapHandler {
                onTapped: {
                    DataManager.multiPredict()
                }
            }
        }
    }
}