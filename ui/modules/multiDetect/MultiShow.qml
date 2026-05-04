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

    property double lastTs: 0

    property var cpuPoints: []
    property var rtPoints: []
    property var memPoints: []
    property var diskPoints: []
    property var readPoints: []
    property var writePoints: []
    property var srtPoints: []
    property var qpsPoints: []


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
                name: "CPU使用率(%)"
                id: m_cpuSeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            LineSeries {
                name: "CPU响应时间(秒)"
                id: responseSeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            LineSeries {
                name: "内存使用率(%)"
                id: memorySeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            LineSeries {
                name: "磁盘使用率(%)"
                id: m_diskSeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            LineSeries {
                name: "磁盘读吞吐量(MB/s)"
                id: io_readSeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            LineSeries {
                name: "磁盘写吞吐量(MB/s)"
                id: io_writeSeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            LineSeries {
                name: "服务器响应时间(秒)"
                id: service_rtSeries
                axisX: metricAxisX
                axisY: metricAxisY
            }

            LineSeries {
                name: "服务器QPS(次/秒)"
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

                onPointChanged: {
                    let now = Date.now()
                    if (now - lastTs < 16) return

                    multiShow.lastTs = now

                    chart.handleHover()
                }
            }

            function handleHover() {
                let p = hover.point.position
                let value = chart.mapToValue(p, m_cpuSeries)
                let x = value.x
                let index = getIndex(x)
                let d = new Date(value.x)

                let text = ""

                if (m_cpuSeries.count > 0) {
                    let p1 = multiShow.cpuPoints[index - 1]
                    let p2 = multiShow.cpuPoints[index]
                    let k = (p2.y - p1.y) / (p2.x - p1.x)
                    let val = p1.y + k * (x - p1.x)
                    text += "\n" + "CPU使用率: " + val.toFixed(4) + "%"
                }

                if (responseSeries.count > 0) {
                    let p1 = multiShow.rtPoints[index - 1]
                    let p2 = multiShow.rtPoints[index]
                    let k = (p2.y - p1.y) / (p2.x - p1.x)
                    let val = p1.y + k * (x - p1.x)
                    text += "\n" + "CPU响应时间: " + val.toFixed(4) + "秒"
                }

                if (memorySeries.count > 0) {
                    let p1 = multiShow.memPoints[index - 1]
                    let p2 = multiShow.memPoints[index]
                    let k = (p2.y - p1.y) / (p2.x - p1.x)
                    let val = p1.y + k * (x - p1.x)
                    text += "\n" + "内存使用率: " + val.toFixed(4) + "%"
                }

                if (m_diskSeries.count > 0) {
                    let p1 = multiShow.diskPoints[index - 1]
                    let p2 = multiShow.diskPoints[index]
                    let k = (p2.y - p1.y) / (p2.x - p1.x)
                    let val = p1.y + k * (x - p1.x)
                    text += "\n" + "磁盘使用率: " + val.toFixed(4) + "%"
                }

                if (io_readSeries.count > 0) {
                    let p1 = multiShow.readPoints[index - 1]
                    let p2 = multiShow.readPoints[index]
                    let k = (p2.y - p1.y) / (p2.x - p1.x)
                    let val = p1.y + k * (x - p1.x)
                    text += "\n" + "磁盘读吞吐量: " + val.toFixed(4) + "MB/s"
                }

                if (io_writeSeries.count > 0) {
                    let p1 = multiShow.writePoints[index - 1]
                    let p2 = multiShow.writePoints[index]
                    let k = (p2.y - p1.y) / (p2.x - p1.x)
                    let val = p1.y + k * (x - p1.x)
                    text += "\n" + "磁盘写吞吐量: " + val.toFixed(4) + "MB/s"
                }

                if (service_rtSeries.count > 0) {
                    let p1 = multiShow.srtPoints[index - 1]
                    let p2 = multiShow.srtPoints[index]
                    let k = (p2.y - p1.y) / (p2.x - p1.x)
                    let val = p1.y + k * (x - p1.x)
                    text += "\n" + "服务器响应时间: " + val.toFixed(4) + "秒"
                }

                if (m_qpsSeries.count > 0) {
                    let p1 = multiShow.qpsPoints[index - 1]
                    let p2 = multiShow.qpsPoints[index]
                    let k = (p2.y - p1.y) / (p2.x - p1.x)
                    let val = p1.y + k * (x - p1.x)
                    text += "\n" + "服务器QPS: " + val.toFixed(4) + "次/秒"
                }

                if (text === "")
                    return

                let result =
                    (d.getMonth() + 1) + "-" +
                    d.getDate() + " " +
                    String(d.getHours()).padStart(2, "0") + ":" +
                    String(d.getMinutes()).padStart(2, "0")
                let time = "时间: " + result + "\n"

                tooltip.text =  time + text
                tooltip.x = p.x - tooltip.width / 2
                tooltip.y = p.y + 10
            }

            function getIndex(x) {
                let arr = multiShow.cpuPoints
                if (arr.length === 0) arr = multiShow.rtPoints
                if (arr.length === 0) arr = multiShow.memPoints
                if (arr.length === 0) arr = multiShow.diskPoints
                if (arr.length === 0) arr = multiShow.readPoints
                if (arr.length === 0) arr = multiShow.writePoints
                if (arr.length === 0) arr = multiShow.srtPoints
                if (arr.length === 0) arr = multiShow.qpsPoints

                let l = 0, r = arr.length - 1

                while (l <= r) {
                    let m = (l + r) >> 1
                    if (arr[m].x === x) return arr[m].y
                    if (arr[m].x < x) l = m + 1
                    else r = m - 1
                }

                let i = Math.max(1, l)

                return Math.min(i, arr.length - 1)
            }

            Rectangle {
                id: tooltip
                visible: hover.hovered
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