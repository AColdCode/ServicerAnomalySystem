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
            Layout.fillWidth: true
            Layout.fillHeight: true

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
        }
    }
}