import QtQuick 6.0
import QtCharts 6.0
import QtQuick.Controls 6.0
import QtQuick.Layouts

Rectangle {

    id: root

    color: "#2d2d30"

    radius: 5

    property string title: "CPU Usage Anomaly Detection"

    property int sampleIntervalMs: 5 * 60 * 1000   // 5分钟
    property bool autoScroll: true                  // 自动滚动
    property int visiblePoints: 10                  // 屏幕显示点数（≈2小时）
    property int maxPoints: 2000                    // 最大缓存
    property var allData: []
    property int currentIndex: 0

    ColumnLayout {

        anchors.fill: parent
        anchors.margins: 10

        spacing: 10

        Text {

            text: root.title

            color: "white"

            font.pixelSize: 18
        }

        Rectangle {

            Layout.fillWidth: true
            Layout.fillHeight: true

            color: "#1e1e1e"

            ChartView {

                anchors.fill: parent

                antialiasing: true

                legend.visible: true

                animationOptions: ChartView.NoAnimation

                DateTimeAxis {
                    id: axisX
                    format: "MM-dd hh:mm"
                    tickCount: visiblePoints

                    property int windowMs: sampleIntervalMs * visiblePoints
                    min: new Date(Date.now() - windowMs)
                    max: new Date(Date.now())
                }

                ValueAxis {

                    id: axisY
                    min: 0
                    max: 0.05
                    tickCount: 6
                }

                LineSeries {

                    id: cpuSeries

                    name: "CPU Usage"

                    axisX: axisX
                    axisY: axisY
                    width: 2
                }

                ScatterSeries {

                    id: anomalySeries

                    name: "Detected Anomaly"

                    color: "red"

                    markerSize: 8

                    axisX: axisX
                    axisY: axisY
                }

            }
        }
    }

    Connections {

        target: DataManager

        function onDataLoaded() {
            root.allData = DataManager.getSingle("detect")
            cpuSeries.clear()
            anomalySeries.clear()
            streamTimer.start()
        }
    }

    Timer {
        id: streamTimer
        interval: 500
        repeat: true
        running: false

        onTriggered: addNextPoint()
    }

    function addNextPoint() {
        if (root.currentIndex >= root.allData.length) {
            streamTimer.stop()
            return
        }

        var p = root.allData[root.currentIndex++]

        var ts = p.ts

        if (cpuSeries.count > maxPoints)
            cpuSeries.remove(0)
        cpuSeries.append(ts, p.cpu)


        if (p.detect === 1) {
            if (anomalySeries.count > maxPoints)
                anomalySeries.remove(0)
            anomalySeries.append(ts, p.cpu)
        }

        if (autoScroll) {
            let windowMs = sampleIntervalMs * visiblePoints
            axisX.max = new Date(ts)
            axisX.min = new Date(ts - windowMs)
        }
        // adjustTickDensity()
    }

    function adjustTickDensity() {
        let span = axisX.max.getTime() - axisX.min.getTime()

        if (span <= 30 * 60 * 1000) {              // ≤30分钟
            axisX.format = "hh:mm:ss"
            axisX.tickCount = 7
        }
        else if (span <= 6 * 60 * 60 * 1000) {     // ≤6小时
            axisX.format = "MM-dd hh:mm"
            axisX.tickCount = 8
        }
        else if (span <= 3 * 24 * 60 * 60 * 1000) {
            axisX.format = "MM-dd\nhh:mm"
            axisX.tickCount = 9
        }
        else {
            axisX.format = "yyyy-MM-dd"
            axisX.tickCount = 6
        }
    }
}
