import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: evaluates
    color: "white"

    border.color: "gray"
    border.width: 1
    radius: 10

    property string evaluate: ""
    property real final_score: 0.0
    property real risk_intensity: 0.0
    property real risk_peak: 0.0
    property real risk_ratio: 0.0
    property real correlation_change: 0.0

    ColumnLayout {
        anchors.fill: parent

        Label {
            Layout.fillWidth: true
            Layout.leftMargin: 10
            Layout.topMargin: 10
            text: "综合态势评价：" + evaluates.evaluate
            font.pixelSize: 20
            color: "black"
            Layout.alignment: Qt.AlignHCenter
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.leftMargin: 10
            Layout.rightMargin: 10
            Layout.bottomMargin: 10

            Rectangle {
                Layout.fillHeight: true
                Layout.preferredWidth: 150
                color: "white"
                // border.color: "gray"
                // border.width: 1
                // radius: 10

                Label {
                    anchors.centerIn: parent
                    text: "总体健康评分\n\n" + evaluates.final_score
                    font.pixelSize: 16
                    color: "black"
                }
            }

            Item {
                Layout.fillWidth: true
            }

            Rectangle {
                Layout.fillHeight: true
                Layout.preferredWidth: 150
                color: "white"
                // border.color: "gray"
                // border.width: 1
                // radius: 10

                Label {
                    anchors.centerIn: parent
                    text: "平均风险\n\n" + evaluates.risk_intensity
                    font.pixelSize: 16
                    color: "black"
                }
            }

            Item {
                Layout.fillWidth: true
            }

            Rectangle {
                Layout.fillHeight: true
                Layout.preferredWidth: 150
                color: "white"
                // border.color: "gray"
                // border.width: 1
                // radius: 10

                Label {
                    anchors.centerIn: parent
                    text: "最大风险\n\n" + evaluates.risk_peak
                    font.pixelSize: 16
                    color: "black"
                }
            }

            Item {
                Layout.fillWidth: true
            }

            Rectangle {
                Layout.fillHeight: true
                Layout.preferredWidth: 150
                color: "white"
                // border.color: "gray"
                // border.width: 1
                // radius: 10

                Label {
                    anchors.centerIn: parent
                    text: "风险持续性\n\n" + evaluates.risk_ratio
                    font.pixelSize: 16
                    color: "black"
                }
            }

            Item {
                Layout.fillWidth: true
            }

            Rectangle {
                Layout.fillHeight: true
                Layout.preferredWidth: 150
                color: "white"
                // border.color: "gray"
                // border.width: 1
                // radius: 10

                Label {
                    anchors.centerIn: parent
                    text: "系统结构异常\n\n" + evaluates.correlation_change
                    font.pixelSize: 16
                    color: "black"
                }
            }

            Item {
                Layout.fillWidth: true
            }
        }
    }
}