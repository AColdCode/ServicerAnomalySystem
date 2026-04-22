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
            id: chart
            Layout.fillWidth: true
            Layout.fillHeight: true
            antialiasing: true

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

                var value = chart.mapToValue(p, metricSeries)
                var d = new Date(value.x)

                var result =
                    (d.getMonth() + 1) + "-" +
                    d.getDate() + " " +
                    String(d.getHours()).padStart(2, "0") + ":" +
                    String(d.getMinutes()).padStart(2, "0")
                tooltip.text = "时间: " + result + "\n" + singleShow.metric + ": " + value.y.toFixed(4)
                tooltip.x = p.x - tooltip.width / 2
                tooltip.y = p.y + 10
                tooltip.visible = true

                // var nearestIndex = -1
                // var minDist = 1e12
                //
                // for (var i = 0; i < metricSeries.count; i++) {
                //     var pt = metricSeries.at(i)
                //     var dx = pt.x - value.x
                //     var dy = pt.y - value.y
                //     var dist = dx * dx + dy * dy
                //
                //     if (dist < minDist) {
                //         minDist = dist
                //         nearestIndex = i
                //     }
                // }
                //
                // if (nearestIndex >= 0) {
                //     var pt = metricSeries.at(nearestIndex)
                //
                //     tooltip.x = p.x + 10
                //     tooltip.y = p.y + 10
                //     tooltip.text = "x: " + pt.x + "\ny: " + pt.y
                //     tooltip.visible = true
                // }
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