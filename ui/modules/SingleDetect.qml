import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "singleDetect"

ScrollView {
    id: singleDetect
    anchors.fill: parent

    property int index: -1

    contentItem: Flickable {
        id: mainInterface
        contentWidth: parent.width
        contentHeight: 800

        ColumnLayout {
            anchors.fill: parent

            SingleTop {
                Layout.fillWidth: true
                Layout.preferredHeight: 100
            }

            SingleShow {
                id: singleShow
                Layout.fillWidth: true
                Layout.preferredHeight: 600
                Layout.leftMargin: 20
                Layout.rightMargin: 20
            }

            Item {
                Layout.fillHeight: true
            }
        }
    }

    Connections {
        target: DataManager

        function onSingleDetectUpdated(index, ts, vs, as, acc) {
            if (index === 0) {
                singleShow.text = "CPU使用率(%)"
            } else if (index === 1) {
                singleShow.text = "CPU响应时间(秒)"
            } else if (index === 2) {
                singleShow.text = "内存使用率(%)"
            } else if (index === 3) {
                singleShow.text = "磁盘使用率(%)"
            } else if (index === 4) {
                singleShow.text = "磁盘读吞吐量(MB/s)"
            } else if (index === 5) {
                singleShow.text = "磁盘写吞吐量(MB/s)"
            } else if (index === 6) {
                singleShow.text = "服务响应时间(秒)"
            } else if (index === 7) {
                singleShow.text = "服务QPS(次/秒)"
            }

            singleShow.acc = acc
            singleShow.series.clear()
            singleShow.anomaly.clear()
            singleShow.qmlPoints = []
            if (ts.length > 0) {
                var minVal = vs[0]
                var maxVal = vs[0]
                if (as[0] === 1) {
                    singleShow.anomaly.append(ts[0] * 1000, vs[0])
                }
                singleShow.series.append(ts[0] * 1000, vs[0])
                singleShow.qmlPoints.push(Qt.point(ts[0] * 1000, vs[0]))
                for (var i = 1; i < ts.length; i++) {
                    var v = vs[i]
                    var t = ts[i] * 1000
                    var a = as[i]
                    if (a === 1) {
                        singleShow.anomaly.append(t, v)
                    }
                    singleShow.series.append(t, v)
                    singleShow.qmlPoints.push(Qt.point(t, v))
                    if (v < minVal) minVal = v
                    if (v > maxVal) maxVal = v
                }

                if (minVal === maxVal) {
                    minVal -= 1
                    maxVal += 1
                }

                var padding = (maxVal - minVal) * 0.1

                singleShow.minY = minVal - padding
                singleShow.maxY = maxVal + padding
                singleShow.minX = new Date(ts[0] * 1000)
                singleShow.maxX = new Date(ts[ts.length - 1] * 1000)
            }
        }
    }
}
