import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtCharts

Rectangle {
    id: singleShow
    width: parent.width
    height: 800
    color: "white"
    radius: 10
    border.color: "gray"
    border.width: 1

    property alias text: metricLabel.text
    property alias minY: metricAxisY.min
    property alias maxY: metricAxisY.max
    property alias minX: metricAxisX.min
    property alias maxX: metricAxisX.max
    property var series: metricSeries
    property var anomaly: metricAnomaly
    property real acc: 0.0

    ColumnLayout {
    anchors.fill: parent
        spacing: 10

        RowLayout {
            Layout.fillWidth: true
            Layout.topMargin: 20
            Layout.leftMargin: 20
            Layout.rightMargin: 20

            Label {
                id: metricLabel
                Layout.alignment: Qt.AlignLeft
                font.pixelSize: 20
                text: ""
            }

            Item {
                Layout.fillWidth: true
            }

            Label {
                id: accLabel
                Layout.alignment: Qt.AlignRight
                font.pixelSize: 20
                text: "异常检测准确性" + singleShow.acc + "%"
            }
        }



        ChartView {
            Layout.fillWidth: true
            Layout.fillHeight: true

            LineSeries {
                name: "正常点"
                id: metricSeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            ScatterSeries {
                name: "异常点"
                id: metricAnomaly
                axisX: metricAxisX
                axisY: metricAxisY
            }

            ValueAxis {
                id: metricAxisY
                min: 0
                max: 1
            }

            DateTimeAxis {
                id: metricAxisX
                format: "MM-dd hh:mm"
            }
        }
    }
}