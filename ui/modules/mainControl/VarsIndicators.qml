import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: varsIndicators
    width: parent.width
    height: 800

    ColumnLayout {
        anchors.fill: parent

        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 100
            Layout.leftMargin: 20
            Layout.rightMargin: 20
            Layout.topMargin: 20
            spacing: 20

            Indicator {
                id: cpuUsage
                Layout.fillWidth: true
                Layout.fillHeight: true
                name: "CPU使用率"
                unit: "%"
            }

            Indicator {
                id: responseTime
                Layout.fillWidth: true
                Layout.fillHeight: true
                name: "响应时间"
                unit: "秒"
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 100
            Layout.leftMargin: 20
            Layout.rightMargin: 20
            spacing: 20

            Indicator {
                id: memoryUsage
                Layout.fillWidth: true
                Layout.fillHeight: true
                name: "内存使用率"
                unit: "%"
            }

            Indicator {
                id: diskUsage
                Layout.fillWidth: true
                Layout.fillHeight: true
                name: "磁盘使用率"
                unit: "%"
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 100
            Layout.leftMargin: 20
            Layout.rightMargin: 20
            spacing: 20

            Indicator {
                id: diskRead
                Layout.fillWidth: true
                Layout.fillHeight: true
                name: "磁盘读吞吐量"
                unit: "MB/s"
            }

            Indicator {
                id: diskWrite
                Layout.fillWidth: true
                Layout.fillHeight: true
                name: "磁盘写吞吐量"
                unit: "MB/s"
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 100
            Layout.leftMargin: 20
            Layout.rightMargin: 20
            spacing: 20

            Indicator {
                id: serverResponseTime
                Layout.fillWidth: true
                Layout.fillHeight: true
                name: "服务响应时间"
                unit: "秒"
            }

            Indicator {
                id: serverQPS
                Layout.fillWidth: true
                Layout.fillHeight: true
                name: "服务QPS"
                unit: "次/秒"
            }
        }
    }

    Connections {
        target: DataManager

        function onTrendUpdated(index, trend, isAnomaly, value) {
            if (index === 0) {
                cpuUsage.series.clear()
                cpuUsage.isNormal = !isAnomaly
                cpuUsage.value = value
                if (trend.length > 0) {
                    var minVal = trend[0]
                    var maxVal = trend[0]
                    cpuUsage.series.append(0, trend[0])
                    for (var i = 1; i < trend.length; i++) {
                        var v = trend[i]
                        cpuUsage.series.append(i, v)
                        if (v < minVal) minVal = v
                        if (v > maxVal) maxVal = v
                    }

                    // 防止 max=min 导致图表崩
                    if (minVal === maxVal) {
                        minVal -= 1
                        maxVal += 1
                    }

                    // 加一点 padding（非常关键，不然贴边）
                    var padding = (maxVal - minVal) * 0.1

                    cpuUsage.minY = minVal - padding
                    cpuUsage.maxY = maxVal + padding
                }
            } else if (index === 1) {
                responseTime.series.clear()
                responseTime.isNormal = !isAnomaly
                responseTime.value = value
                if (trend.length > 0) {
                    var minVal = trend[0]
                    var maxVal = trend[0]
                    responseTime.series.append(0, trend[0])
                    for (var i = 1; i < trend.length; i++) {
                        var v = trend[i]
                        responseTime.series.append(i, v)
                        if (v < minVal) minVal = v
                        if (v > maxVal) maxVal = v
                    }

                    // 防止 max=min 导致图表崩
                    if (minVal === maxVal) {
                        minVal -= 1
                        maxVal += 1
                    }

                    // 加一点 padding（非常关键，不然贴边）
                    var padding = (maxVal - minVal) * 0.1

                    responseTime.minY = minVal - padding
                    responseTime.maxY = maxVal + padding
                }
            } else if (index === 2) {
                memoryUsage.series.clear()
                memoryUsage.isNormal = !isAnomaly
                memoryUsage.value = value
                if (trend.length > 0) {
                    var minVal = trend[0]
                    var maxVal = trend[0]
                    memoryUsage.series.append(0, trend[0])
                    for (var i = 1; i < trend.length; i++) {
                        var v = trend[i]
                        memoryUsage.series.append(i, v)
                        if (v < minVal) minVal = v
                        if (v > maxVal) maxVal = v
                    }

                    // 防止 max=min 导致图表崩
                    if (minVal === maxVal) {
                        minVal -= 1
                        maxVal += 1
                    }

                    // 加一点 padding（非常关键，不然贴边）
                    var padding = (maxVal - minVal) * 0.1

                    memoryUsage.minY = minVal - padding
                    memoryUsage.maxY = maxVal + padding
                }
            } else if (index === 3) {
                diskUsage.series.clear()
                diskUsage.isNormal = !isAnomaly
                diskUsage.value = value
                if (trend.length > 0) {
                    var minVal = trend[0]
                    var maxVal = trend[0]
                    diskUsage.series.append(0, trend[0])
                    for (var i = 1; i < trend.length; i++) {
                        var v = trend[i]
                        diskUsage.series.append(i, v)
                        if (v < minVal) minVal = v
                        if (v > maxVal) maxVal = v
                    }

                    // 防止 max=min 导致图表崩
                    if (minVal === maxVal) {
                        minVal -= 1
                        maxVal += 1
                    }

                    // 加一点 padding（非常关键，不然贴边）
                    var padding = (maxVal - minVal) * 0.1

                    diskUsage.minY = minVal - padding
                    diskUsage.maxY = maxVal + padding
                }
            } else if (index === 4) {
                diskRead.series.clear()
                diskRead.isNormal = !isAnomaly
                diskRead.value = value
                if (trend.length > 0) {
                    var minVal = trend[0]
                    var maxVal = trend[0]
                    diskRead.series.append(0, trend[0])
                    for (var i = 1; i < trend.length; i++) {
                        var v = trend[i]
                        diskRead.series.append(i, v)
                        if (v < minVal) minVal = v
                        if (v > maxVal) maxVal = v
                    }

                    // 防止 max=min 导致图表崩
                    if (minVal === maxVal) {
                        minVal -= 1
                        maxVal += 1
                    }

                    // 加一点 padding（非常关键，不然贴边）
                    var padding = (maxVal - minVal) * 0.1

                    diskRead.minY = minVal - padding
                    diskRead.maxY = maxVal + padding
                }
            } else if (index === 5) {
                diskWrite.series.clear()
                diskWrite.isNormal = !isAnomaly
                diskWrite.value = value
                if (trend.length > 0) {
                    var minVal = trend[0]
                    var maxVal = trend[0]
                    diskWrite.series.append(0, trend[0])
                    for (var i = 1; i < trend.length; i++) {
                        var v = trend[i]
                        diskWrite.series.append(i, v)
                        if (v < minVal) minVal = v
                        if (v > maxVal) maxVal = v
                    }

                    // 防止 max=min 导致图表崩
                    if (minVal === maxVal) {
                        minVal -= 1
                        maxVal += 1
                    }

                    // 加一点 padding（非常关键，不然贴边）
                    var padding = (maxVal - minVal) * 0.1

                    diskWrite.minY = minVal - padding
                    diskWrite.maxY = maxVal + padding
                }
            } else if (index === 6) {
                serverResponseTime.series.clear()
                serverResponseTime.isNormal = !isAnomaly
                serverResponseTime.value = value
                if (trend.length > 0) {
                    var minVal = trend[0]
                    var maxVal = trend[0]
                    serverResponseTime.series.append(0, trend[0])
                    for (var i = 1; i < trend.length; i++) {
                        var v = trend[i]
                        serverResponseTime.series.append(i, v)
                        if (v < minVal) minVal = v
                        if (v > maxVal) maxVal = v
                    }

                    // 防止 max=min 导致图表崩
                    if (minVal === maxVal) {
                        minVal -= 1
                        maxVal += 1
                    }

                    // 加一点 padding（非常关键，不然贴边）
                    var padding = (maxVal - minVal) * 0.1

                    serverResponseTime.minY = minVal - padding
                    serverResponseTime.maxY = maxVal + padding
                }
            } else if (index === 7) {
                serverQPS.series.clear()
                serverQPS.isNormal = !isAnomaly
                serverQPS.value = value
                if (trend.length > 0) {
                    var minVal = trend[0]
                    var maxVal = trend[0]
                    serverQPS.series.append(0, trend[0])
                    for (var i = 1; i < trend.length; i++) {
                        var v = trend[i]
                        serverQPS.series.append(i, v)
                        if (v < minVal) minVal = v
                        if (v > maxVal) maxVal = v
                    }

                    // 防止 max=min 导致图表崩
                    if (minVal === maxVal) {
                        minVal -= 1
                        maxVal += 1
                    }

                    // 加一点 padding（非常关键，不然贴边）
                    var padding = (maxVal - minVal) * 0.1

                    serverQPS.minY = minVal - padding
                    serverQPS.maxY = maxVal + padding
                }
            }
        }
    }
}