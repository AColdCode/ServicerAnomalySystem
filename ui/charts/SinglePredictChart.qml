import QtQuick 6.0
import QtCharts 6.0
import QtQuick.Controls 6.0
import QtQuick.Layouts

Rectangle {

    id: root

    color: "#2d2d30"

    radius: 5

    property string title: "CPU Usage Predict"

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
                animationOptions: ChartView.NoAnimation

                legend.visible: true

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
                    tickCount: 6

                    min: 0
                    max: 0.05
                }

                // =========================
                // 实际值
                // =========================

                LineSeries {

                    id: realSeries

                    name: "Real CPU"

                    axisX: axisX
                    axisY: axisY
                }

                // =========================
                // 预测值
                // =========================

                LineSeries {

                    id: predSeries

                    name: "Predicted CPU"

                    color: "orange"

                    axisX: axisX
                    axisY: axisY
                }
            }
        }
    }

    Connections {

        target: DataManager

        function onDataLoaded() {
            root.allData = DataManager.getSingle("predict")
            realSeries.clear()
            predSeries.clear()
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
        if (currentIndex >= allData.length) {
            streamTimer.stop()
            return
        }

        var p = root.allData[root.currentIndex++]

        var ts = p.ts

        if (realSeries.count > maxPoints)
            realSeries.remove(0)
        realSeries.append(ts, p.real)

        if (predSeries.count > maxPoints)
            predSeries.remove(0)
        predSeries.append(ts, p.pred)

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
