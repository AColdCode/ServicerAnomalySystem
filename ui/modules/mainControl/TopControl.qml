import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: topControl
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
        }

        Item {
            Layout.fillWidth: true
        }

        Rectangle {
            id: refreshBtn
            Layout.preferredWidth: 100
            Layout.preferredHeight: 50
            border.width: 1
            border.color: "grey"
            radius: 10
            color: refreshHover.hovered ? "#F1F5F9" : "white"

            RowLayout {
                anchors.centerIn: parent
                spacing: 5

                Image {
                    Layout.preferredWidth: 30
                    Layout.preferredHeight: 30
                    source: "../../../images/refresh.svg"
                    fillMode: Image.PreserveAspectFit
                }

                Text {
                    text: "刷新"
                    font.pixelSize: 20
                    color: "black"
                }
            }

            HoverHandler {
                id: refreshHover
                cursorShape: Qt.PointingHandCursor
            }

            TapHandler {
                id: refreshTap

                onTapped: {
                    DataManager.update_trend()
                }
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
                    DataManager.setTrendRange("1h")
                } else if (currentIndex === 1) {
                    DataManager.setTrendRange("6h")
                } else if (currentIndex === 2) {
                    DataManager.setTrendRange("1d")
                } else if (currentIndex === 3) {
                    DataManager.setTrendRange("7d")
                }
            }

            HoverHandler {
                cursorShape: Qt.PointingHandCursor
            }
        }
    }
}