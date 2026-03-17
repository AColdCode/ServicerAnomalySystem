import QtQuick 6.0
import QtCharts 6.0
import QtQuick.Controls 6.0
import QtQuick.Layouts

Rectangle {

    id: root

    color: "#2d2d30"

    radius: 5

    property string title: "Multi Metric Predict"

    property int sampleIntervalMs: 5 * 60 * 1000   // 5分钟
    property bool autoScroll: true                  // 自动滚动
    property int visiblePoints: 10                 // 屏幕显示点数（≈2小时）
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
                    tickCount: 10

                    min: 0
                    max: 10
                }

                // =========================
                // CPU
                // =========================

                LineSeries {

                    id: cpuReal

                    name: "CPU Real"

                    axisX: axisX
                    axisY: axisY
                }

                LineSeries {

                    id: cpuPred

                    name: "CPU Pred"

                    color: "orange"

                    axisX: axisX
                    axisY: axisY
                }

                // =========================
                // Memory
                // =========================

                LineSeries {

                    id: memReal

                    name: "Memory Real"

                    axisX: axisX
                    axisY: axisY
                }

                LineSeries {

                    id: memPred

                    name: "Memory Pred"

                    color: "yellow"

                    axisX: axisX
                    axisY: axisY
                }

                // =========================
                // Response Time
                // =========================

                LineSeries {

                    id: rtReal

                    name: "RT Real"

                    axisX: axisX
                    axisY: axisY
                }

                LineSeries {

                    id: rtPred

                    name: "RT Pred"

                    color: "cyan"

                    axisX: axisX
                    axisY: axisY
                }

            }
        }
    }

    Connections {

        target: DataManager

        function onDataLoaded() {
            root.allData = DataManager.getMulti("predict")

            cpuReal.clear()
            cpuPred.clear()

            memReal.clear()
            memPred.clear()

            rtReal.clear()
            rtPred.clear()

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
        if(root.currentIndex >= root.allData.length){
            streamTimer.stop()
            return
        }

        var p = root.allData[root.currentIndex++]

        var ts = p.ts

        if (cpuReal.count > maxPoints)
            cpuReal.remove(0)
        cpuReal.append(ts, p.real_cpu)

        if (cpuPred.count > maxPoints)
            cpuPred.remove(0)
        cpuPred.append(ts, p.pred_cpu)

        if (memReal.count > maxPoints)
            memReal.remove(0)
        memReal.append(ts, p.real_mem)

        if (memPred.count > maxPoints)
            memPred.remove(0)
        memPred.append(ts, p.pred_mem)

        if (rtReal.count > maxPoints)
            rtReal.remove(0)
        rtReal.append(ts, p.real_resp)

        if (rtPred.count > maxPoints)
            rtPred.remove(0)
        rtPred.append(ts, p.pred_resp)

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
