import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtCharts

Rectangle {
    id: multiShow
    width: parent.width
    height: 800
    color: "white"
    radius: 10
    border.color: "gray"
    border.width: 1

    property alias minY: metricAxisY.min
    property alias maxY: metricAxisY.max
    property alias minX: metricAxisX.min
    property alias maxX: metricAxisX.max

    property var cpuSeries: m_cpuSeries
    property var rtSeries: responseSeries
    property var memSeries: memorySeries
    property var diskSeries: m_diskSeries
    property var readSeries: io_readSeries
    property var writeSeries: io_writeSeries
    property var srtSeries: service_rtSeries
    property var qpsSeries: m_qpsSeries
    property var multiAnomaly: anomaly


    ColumnLayout {
    anchors.fill: parent
        spacing: 10

        Label {
            id: metricLabel
            Layout.leftMargin: 20
            Layout.topMargin: 20
            Layout.alignment: Qt.AlignLeft
            font.pixelSize: 20
            text: "多指标时间序列与异常点"
        }

        ChartView {
            id: chart
            Layout.fillWidth: true
            Layout.fillHeight: true
            antialiasing: true

            LineSeries {
                name: "CPU使用率"
                id: m_cpuSeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            LineSeries {
                name: "CPU响应时间"
                id: responseSeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            LineSeries {
                name: "内存使用率"
                id: memorySeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            LineSeries {
                name: "磁盘使用率"
                id: m_diskSeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            LineSeries {
                name: "磁盘读吞吐量"
                id: io_readSeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            LineSeries {
                name: "磁盘写吞吐量"
                id: io_writeSeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            LineSeries {
                name: "服务器响应时间"
                id: service_rtSeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            LineSeries {
                name: "服务器QPS"
                id: m_qpsSeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            ScatterSeries {
                name: "异常点"
                id: anomaly
                axisX: metricAxisX
                axisY: metricAxisY

                color: "red"
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

                var text = ""

                if (m_cpuSeries.count > 0) {
                    var value = chart.mapToValue(p, m_cpuSeries)
                    var d = new Date(value.x)
                    text += "\n" + "CPU使用率: " + value.y.toFixed(4)
                }

                if (responseSeries.count > 0) {
                    var value = chart.mapToValue(p, responseSeries)
                    var d = new Date(value.x)
                    text += "\n" + "CPU响应时间: " + value.y.toFixed(4)
                }

                if (memorySeries.count > 0) {
                    var value = chart.mapToValue(p, memorySeries)
                    var d = new Date(value.x)
                    text += "\n" + "内存使用率: " + value.y.toFixed(4)
                }

                if (m_diskSeries.count > 0) {
                    var value = chart.mapToValue(p, m_diskSeries)
                    var d = new Date(value.x)
                    text += "\n" + "磁盘使用率: " + value.y.toFixed(4)
                }

                if (io_readSeries.count > 0) {
                    var value = chart.mapToValue(p, io_readSeries)
                    var d = new Date(value.x)
                    text += "\n" + "磁盘读吞吐量: " + value.y.toFixed(4)
                }

                if (io_writeSeries.count > 0) {
                    var value = chart.mapToValue(p, io_writeSeries)
                    var d = new Date(value.x)
                    text += "\n" + "磁盘写吞吐量: " + value.y.toFixed(4)
                }

                if (service_rtSeries.count > 0) {
                    var value = chart.mapToValue(p, service_rtSeries)
                    var d = new Date(value.x)
                    text += "\n" + "服务器响应时间: " + value.y.toFixed(4)
                }

                if (m_qpsSeries.count > 0) {
                    var value = chart.mapToValue(p, m_qpsSeries)
                    var d = new Date(value.x)
                    text += "\n" + "服务器QPS: " + value.y.toFixed(4)
                }

                if (text === "")
                    return

                var result =
                    (d.getMonth() + 1) + "-" +
                    d.getDate() + " " +
                    String(d.getHours()).padStart(2, "0") + ":" +
                    String(d.getMinutes()).padStart(2, "0")
                var time = "时间: " + result + "\n"

                tooltip.text =  time + text
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