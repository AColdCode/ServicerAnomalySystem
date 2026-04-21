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
    property real volatility: 0.0
    property real smoothness: 0.0
    property real trend: 0.0
    property real anomaly_ratio: 0.0
    property real jump: 0.0
    property real monotonic: 0.0
    property real entropy: 0.0

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

        GridLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.leftMargin: 10
            Layout.rightMargin: 10
            columns: 4

            Label {
                text: "综合健康分：" + evaluates.final_score
                Layout.fillWidth: true
            }
            Label {
                text: "波动率：" + evaluates.volatility
                Layout.fillWidth: true
            }
            Label {
                text: "平滑度：" + evaluates.smoothness
                Layout.fillWidth: true
            }
            Label {
                text: "趋势方向：" + evaluates.trend
                Layout.fillWidth: true
            }

            Label {
                text: "异常点占比：" + evaluates.anomaly_ratio
                Layout.fillWidth: true
            }
            Label {
                text: "突变程度：" + evaluates.jump
                Layout.fillWidth: true
            }
            Label {
                text: "单调性：" + evaluates.monotonic
                Layout.fillWidth: true
            }
            Label {
                text: "复杂度：" + evaluates.entropy
                Layout.fillWidth: true
            }
        }
    }
}