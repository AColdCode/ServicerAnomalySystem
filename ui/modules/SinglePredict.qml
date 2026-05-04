import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "singlePredict"

ScrollView {
    id: singlePredict
    anchors.fill: parent

    property int index: -1

    contentItem: Flickable {
        id: mainInterface
        contentWidth: parent.width
        contentHeight: 900

        ColumnLayout {
            anchors.fill: parent

            SingleTop {
                Layout.fillWidth: true
                Layout.preferredHeight: 100
            }

            Evaluates {
                id: evaluates
                Layout.fillWidth: true
                Layout.preferredHeight: 150
                Layout.leftMargin: 20
                Layout.rightMargin: 20
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

        function onSinglePredictUpdated(index, ts, vs, preTs, preVs, status, final_score, risk_intensity, risk_peak, risk_ratio, risk_series) {
            evaluates.evaluate = status
            evaluates.final_score = final_score
            evaluates.risk_intensity = risk_intensity
            evaluates.risk_peak = risk_peak
            evaluates.risk_ratio = risk_ratio

            singleShow.risk_series = risk_series

            if (index === 0) {
                singleShow.metric = "CPU使用率(%)"
            } else if (index === 1) {
                singleShow.metric = "CPU响应时间(秒)"
            } else if (index === 2) {
                singleShow.metric = "内存使用率(%)"
            } else if (index === 3) {
                singleShow.metric = "磁盘使用率(%)"
            } else if (index === 4) {
                singleShow.metric = "磁盘读吞吐量(MB/s)"
            } else if (index === 5) {
                singleShow.metric = "磁盘写吞吐量(MB/s)"
            } else if (index === 6) {
                singleShow.metric = "服务响应时间(秒)"
            } else if (index === 7) {
                singleShow.metric = "服务QPS(次/秒)"
            }

            singleShow.hSeries.clear()
            singleShow.pSeries.clear()
            singleShow.qmlPoints = []
            singleShow.qmlPrePoints = []
            if (ts.length > 0) {
                var minVal = vs[0]
                var maxVal = vs[0]

                singleShow.qmlPoints.push(Qt.point(ts[0] * 1000, vs[0]))
                singleShow.hSeries.append(ts[0] * 1000, vs[0])
                for (var i = 1; i < ts.length; i++) {
                    var v = vs[i]
                    var t = ts[i] * 1000
                    singleShow.qmlPoints.push(Qt.point(t, v))
                    singleShow.hSeries.append(t, v)
                    if (v < minVal) minVal = v
                    if (v > maxVal) maxVal = v
                }

                singleShow.qmlPrePoints.push(Qt.point(ts[ts.length - 1] * 1000, vs[vs.length - 1]))
                singleShow.pSeries.append(ts[ts.length - 1] * 1000, vs[vs.length - 1])
                for (var j = 0; j < preTs.length; j++) {
                    var pv = preVs[j]
                    var pt = preTs[j] * 1000
                    singleShow.qmlPrePoints.push(Qt.point(pt, pv))
                    singleShow.pSeries.append(pt, pv)
                    if (pv < minVal) minVal = pv
                    if (pv > maxVal) maxVal = pv
                }

                if (minVal === maxVal) {
                    minVal -= 1
                    maxVal += 1
                }

                var padding = (maxVal - minVal) * 0.1

                singleShow.minY = minVal - padding
                singleShow.maxY = maxVal + padding
                singleShow.minX = new Date(ts[0] * 1000)
                singleShow.maxX = new Date(preTs[preTs.length - 1] * 1000)
            }
        }
    }
}
