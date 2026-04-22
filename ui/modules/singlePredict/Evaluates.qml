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
    property real risk_series: []

    ColumnLayout {
        anchors.fill: parent

        Label {
            Layout.fillWidth: true
            Layout.leftMargin: 10
            Layout.topMargin: 10
            text: "综合态势评估：" + evaluates.evaluate
            font.pixelSize: 20
            color: "black"
            Layout.alignment: Qt.AlignHCenter
        }

        GridLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.leftMargin: 10
            Layout.rightMargin: 10
            columns: 2

            Label {
                text: "综合健康分：" + evaluates.final_score
                Layout.fillWidth: true
            }
            Label {
                text: "风险强度：" + evaluates.risk_intensity
                Layout.fillWidth: true
            }

            Label {
                text: "风险峰值：" + evaluates.risk_peak
                Layout.fillWidth: true
            }
            Label {
                text: "高风险比例：" + evaluates.risk_ratio
                Layout.fillWidth: true
            }
        }
    }
}
