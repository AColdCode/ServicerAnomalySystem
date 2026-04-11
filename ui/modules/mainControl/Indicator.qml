import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtCharts

Rectangle {
    id: indicator
    width: parent.width / 2
    height: 200
    radius: 10
    border.color: "black"
    border.width: 1
    property string name: ""
    property real value: 0.0
    property string unit: ""
    property bool isNormal: true
    property var series: m_series
    property alias minY: axisY.min
    property alias maxY: axisY.max

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10

        RowLayout {
            Layout.fillWidth: true

            Text {
                text: name
                font.pixelSize: 15
                color: "black"
            }

            Item {
                Layout.fillWidth: true
            }

            Rectangle {
                Layout.preferredWidth: 50
                Layout.preferredHeight: 20
                color: isNormal ? "#F1F5F9" : "red"
                radius: 10

                Text {
                    anchors.centerIn: parent
                    text: indicator.isNormal ? "正常" : "异常"
                }
            }
        }

        Text {
            text: value + " " + unit
            font.pixelSize: 30
            color: "black"
        }

        ChartView {
            id: chart
            Layout.fillWidth: true
            Layout.fillHeight: true
            antialiasing: true
            legend.visible: false

            ValueAxis { id: axisX; visible: false }
            ValueAxis { id: axisY; visible: false }

            LineSeries {
                id: m_series
                axisX: axisX
                axisY: axisY
            }
        }
    }
}