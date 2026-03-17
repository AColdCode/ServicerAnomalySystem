import QtQuick 6.0
import QtQuick.Controls 6.0
import QtCharts 6.0

ApplicationWindow {
    id: root
    width: 1200
    height: 600
    visible: true
    title: "Anomaly Detection"

    // ===== 采样参数 =====
    property int sampleIntervalMs: 5 * 60 * 1000   // 5分钟
    property int visiblePoints: 24                  // 屏幕显示点数（≈2小时）
    property bool autoScroll: true                  // 自动滚动
    property int maxPoints: 2000                    // 最大缓存

    // =========================
    // 图表
    // =========================
    ChartView {
        id: chartView
        anchors.fill: parent
        antialiasing: true
        // animationOptions: ChartView.NoAnimation
        legend.visible: true

        // ===== 时间轴 =====
        DateTimeAxis {
            id: axisX_
            format: "MM-dd hh:mm"
            tickCount: 7

            // 初始窗口（非常重要）
            property int windowMs: sampleIntervalMs * visiblePoints
            min: new Date(Date.now() - windowMs)
            max: new Date(Date.now())
        }

        // ===== Y轴 =====
        ValueAxis {
            id: axisY_
            min: 0
            max: 0.0002
            tickCount: 7
        }

        // ===== 主曲线 =====
        LineSeries {
            id: metricLine
            name: "Cpu Usage"
            axisX: axisX_
            axisY: axisY_
            width: 2
        }

        // ===== 异常点 =====
        ScatterSeries {
            id: anomalyPoints
            name: "Detected Anomaly"
            axisX: axisX_
            axisY: axisY_
            markerSize: 8
        }
    }

    // =========================
    // 数据接收
    // =========================
    Connections {
        target: dataBridge

        function onNewPoint(ts, value, isAnomaly) {

            // ===== 加点 =====
            metricLine.append(ts, value)

            if (isAnomaly === 1) {
                anomalyPoints.append(ts, value)
            }

            // ===== 自动滚动窗口（核心）=====
            if (autoScroll) {
                let windowMs = sampleIntervalMs * visiblePoints
                axisX_.max = new Date(ts)
                axisX_.min = new Date(ts - windowMs)
            }

            // ===== 内存保护 =====
            if (metricLine.count > maxPoints) {
                metricLine.remove(0)
            }
            if (anomalyPoints.count > maxPoints) {
                anomalyPoints.remove(0)
            }

            // ===== 动态刻度 =====
            adjustTickDensity()
        }
    }

    // =========================
    // 自适应刻度（监控级）
    // =========================
    function adjustTickDensity() {
        let span = axisX_.max.getTime() - axisX_.min.getTime()

        if (span <= 30 * 60 * 1000) {              // ≤30分钟
            axisX_.format = "hh:mm:ss"
            axisX_.tickCount = 6
        }
        else if (span <= 6 * 60 * 60 * 1000) {     // ≤6小时
            axisX_.format = "MM-dd hh:mm"
            axisX_.tickCount = 7
        }
        else if (span <= 3 * 24 * 60 * 60 * 1000) {
            axisX_.format = "MM-dd\nhh:mm"
            axisX_.tickCount = 8
        }
        else {
            axisX_.format = "yyyy-MM-dd"
            axisX_.tickCount = 6
        }
    }
}