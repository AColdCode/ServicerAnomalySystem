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
            id: chart
            Layout.fillWidth: true
            Layout.fillHeight: true
            antialiasing: true

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

            HoverHandler {
                id: hover
                acceptedDevices: PointerDevice.Mouse

                onHoveredChanged: {
                    if (!hovered) {
                        tooltip.visible = false
                    }
                }

                onPointChanged: {
                    chart.handleHover()
                }
            }

            function handleHover() {
                var p = hover.point.position

                var value = chart.mapToValue(p, historSeries)
                var d = new Date(value.x)

                var result =
                    (d.getMonth() + 1) + "-" +
                    d.getDate() + " " +
                    String(d.getHours()).padStart(2, "0") + ":" +
                    String(d.getMinutes()).padStart(2, "0")
                tooltip.text = "时间: " + result + "\n" + singleShow.metricName + ": " + value.y.toFixed(4)
                tooltip.x = p.x - tooltip.width / 2
                tooltip.y = p.y + 10
                tooltip.visible = true
            }

            Rectangle {
                id: tooltip
                visible: false
                color: "#333333CC"
                radius: 4

                property string text: ""

                width: textItem.width + 12
                height: textItem.height + 12

                Text {
                    id: textItem
                    text: tooltip.text
                    anchors.centerIn: parent
                    color: "white"
                }
            }
        }
    }
}
