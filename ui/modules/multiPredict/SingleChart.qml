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

    property string metricName: ""

    property alias minY: metricAxisY.min
    property alias maxY: metricAxisY.max
    property alias minX: metricAxisX.min
    property alias maxX: metricAxisX.max

    property var hSeries: historSeries
    property var pSeries: predictSeries


    ColumnLayout {
    anchors.fill: parent
        spacing: 10

        Label {
            id: metricLabel
            Layout.leftMargin: 20
            Layout.topMargin: 20
            Layout.alignment: Qt.AlignLeft
            font.pixelSize: 20
            text: singleShow.metricName
        }

        ChartView {
            Layout.fillWidth: true
            Layout.fillHeight: true

            LineSeries {
                name: "历史值"
                id: historSeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            LineSeries {
                name: "预测值"
                id: predictSeries
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
