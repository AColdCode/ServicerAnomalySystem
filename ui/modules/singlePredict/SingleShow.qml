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

    property string metric: ""
    property alias minY: metricAxisY.min
    property alias maxY: metricAxisY.max
    property alias minX: metricAxisX.min
    property alias maxX: metricAxisX.max
    property var hSeries: metricSeries
    property var pSeries: metricPredictSeries

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
                text: singleShow.metric + " - 历史值与预测值"
            }

            Item {
                Layout.fillWidth: true
            }
        }



        ChartView {
            Layout.fillWidth: true
            Layout.fillHeight: true

            LineSeries {
                name: singleShow.metric + "历史值"
                id: metricSeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            LineSeries {
                name: singleShow.metric + "预测值"
                id: metricPredictSeries
                axisX: metricAxisX
                axisY: metricAxisY
                color: "grey"
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