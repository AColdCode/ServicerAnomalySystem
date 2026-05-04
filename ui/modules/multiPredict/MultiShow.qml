import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtCharts

Rectangle {
    id: multiShow
    width: parent.width
    height: 800
    color: "white"

    property var cpuChart: m_cpuChart
    property var rtChart: responseChart
    property var memChart: memoryChart
    property var diskChart: m_diskChart
    property var readChart: io_readChart
    property var writeChart: io_writeChart
    property var srtChart: service_rtChart
    property var qpsChart: m_qpsChart


    GridLayout {
        anchors.fill: parent
        columns: 2

        SingleChart {
            id: m_cpuChart
            Layout.fillWidth: true
            Layout.fillHeight: true

            metricName: "CPU使用率(%)"
        }
        SingleChart {
            id: responseChart
            Layout.fillWidth: true
            Layout.fillHeight: true

            metricName: "CPU响应时间(秒)"
        }
        SingleChart {
            id: memoryChart
            Layout.fillWidth: true
            Layout.fillHeight: true

            metricName: "内存使用率(%)"
        }
        SingleChart {
            id: m_diskChart
            Layout.fillWidth: true
            Layout.fillHeight: true

            metricName: "磁盘使用率(%)"
        }

        SingleChart {
            id: io_readChart
            Layout.fillWidth: true
            Layout.fillHeight: true

            metricName: "磁盘读吞吐量(MB/s)"
        }
        SingleChart {
            id: io_writeChart
            Layout.fillWidth: true
            Layout.fillHeight: true

            metricName: "磁盘写吞吐量(MB/s)"
        }
        SingleChart {
            id: service_rtChart
            Layout.fillWidth: true
            Layout.fillHeight: true

            metricName: "服务器响应时间(秒)"
        }
        SingleChart {
            id: m_qpsChart
            Layout.fillWidth: true
            Layout.fillHeight: true

            metricName: "服务器QPS(次/秒)"
        }
    }
}