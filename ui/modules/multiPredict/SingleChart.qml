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

    property double lastTs: 0
    property var qmlPoints: []
    property var qmlPrePoints: []


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

                onPointChanged: {
                    if (qmlPoints.length === 0) return

                    let now = Date.now()
                    if (now - lastTs < 16) return

                    singleShow.lastTs = now

                    chart.handleHover()
                }
            }

            function handleHover() {
                let p = hover.point.position

                let value = chart.mapToValue(p, historSeries)

                let vals = getY(value.x)
                let val = vals[0], risk = vals[1]

                let d = new Date(value.x)

                let result =
                    (d.getMonth() + 1) + "-" +
                    d.getDate() + " " +
                    String(d.getHours()).padStart(2, "0") + ":" +
                    String(d.getMinutes()).padStart(2, "0")
                let txt = "时间: " + result + "\n" + singleShow.metricName + ": " + val.toFixed(4)
                if (risk !== 0) {
                    txt += "\n风险值: " + risk.toFixed(4)
                }
                tooltip.text = txt
                tooltip.x = p.x - tooltip.width / 2
                tooltip.y = p.y + 10
            }

            function getY(x) {
                let arr = singleShow.qmlPoints
                let flag = 0
                if (arr[arr.length - 1].x < x) {
                    arr = singleShow.qmlPrePoints
                    flag = 1
                }
                let l = 0, r = arr.length - 1

                while (l <= r) {
                    let m = (l + r) >> 1
                    if (arr[m].x === x) return arr[m].y
                    if (arr[m].x < x) l = m + 1
                    else r = m - 1
                }

                let val = 0, risk = 0
                let i = Math.max(1, l)
                i = Math.min(i, arr.length - 1)
                let p1 = arr[i - 1]
                let p2 = arr[i]
                let k = (p2.y - p1.y) / (p2.x - p1.x)
                val = p1.y + k * (x - p1.x)

                // if (flag) {
                //     let r1 = singleShow.risk_series[i - 1]
                //     let r2 = singleShow.risk_series[i]
                //     let k1 = (r2 - r1) / (p2.x - p1.x)
                //     risk = r1 + k1 * (x - p1.x)
                // }

                return [val, risk]
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
