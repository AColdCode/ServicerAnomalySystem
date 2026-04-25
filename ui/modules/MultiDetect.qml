import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "multiDetect"

ScrollView {
    id: multiDetect
    anchors.fill: parent

    property int index: -1

    contentItem: Flickable {
        id: mainInterface
        contentWidth: parent.width
        contentHeight: 1600

        ColumnLayout {
            anchors.fill: parent

            MultiTop {
                Layout.fillWidth: true
                Layout.preferredHeight: 100
            }

            SeletcMetric {
                id: selectMetric
                Layout.fillWidth: true
                Layout.preferredHeight: 150
                Layout.leftMargin: 20
                Layout.rightMargin: 20

                onClearAnomaly: {
                    multiShow.multiAnomaly.clear()
                    multiShow.cpuSeries.clear()
                    multiShow.rtSeries.clear()
                    multiShow.memSeries.clear()
                    multiShow.diskSeries.clear()
                    multiShow.readSeries.clear()
                    multiShow.writeSeries.clear()
                    multiShow.srtSeries.clear()
                    multiShow.qpsSeries.clear()

                    multiShow.cpuPoints = []
                    multiShow.rtPoints = []
                    multiShow.memPoints = []
                    multiShow.diskPoints = []
                    multiShow.readPoints = []
                    multiShow.writePoints = []
                    multiShow.srtPoints = []
                    multiShow.qpsPoints = []
                }
            }

            MultiShow {
                id: multiShow
                Layout.fillWidth: true
                Layout.preferredHeight: 600
                Layout.topMargin: 20
                Layout.leftMargin: 20
                Layout.rightMargin: 20
            }

            MultiBottom {
                id: multiBottom
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.topMargin: 20
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

        function onMultiDetectUpdated(index, ts, vs, as) {
            if (index === 0) {
                if (as[0] === 1) {
                    multiShow.multiAnomaly.append(ts[0] * 1000, vs[0])
                }
                multiShow.cpuSeries.append(ts[0] * 1000, vs[0])
                multiShow.cpuPoints.push(Qt.point(ts[0] * 1000, vs[0]))
                for (let i = 1; i < ts.length; i++) {
                    let v = vs[i]
                    let t = ts[i] * 1000
                    let a = as[i]
                    if (a === 1) {
                        multiShow.multiAnomaly.append(t, v)
                    }
                    multiShow.cpuSeries.append(t, v)
                    multiShow.cpuPoints.push(Qt.point(t, v))
                }
            } else if (index === 1) {
                if (as[0] === 1) {
                    multiShow.multiAnomaly.append(ts[0] * 1000, vs[0])
                }
                multiShow.rtSeries.append(ts[0] * 1000, vs[0])
                multiShow.rtPoints.push(Qt.point(ts[0] * 1000, vs[0]))
                for (let i = 1; i < ts.length; i++) {
                    let v = vs[i]
                    let t = ts[i] * 1000
                    let a = as[i]
                    if (a === 1) {
                        multiShow.multiAnomaly.append(t, v)
                    }
                    multiShow.rtSeries.append(t, v)
                    multiShow.rtPoints.push(Qt.point(t, v))
                }
            } else if (index === 2) {
                if (as[0] === 1) {
                    multiShow.anomaly.append(ts[0] * 1000, vs[0])
                }
                multiShow.memSeries.append(ts[0] * 1000, vs[0])
                multiShow.memPoints.push(Qt.point(ts[0] * 1000, vs[0]))
                for (let i = 1; i < ts.length; i++) {
                    let v = vs[i]
                    let t = ts[i] * 1000
                    let a = as[i]
                    if (a === 1) {
                        multiShow.multiAnomaly.append(t, v)
                    }
                    multiShow.memSeries.append(t, v)
                    multiShow.memPoints.push(Qt.point(t, v))
                }
            } else if (index === 3) {
                if (as[0] === 1) {
                    multiShow.multiAnomaly.append(ts[0] * 1000, vs[0])
                }
                multiShow.diskSeries.append(ts[0] * 1000, vs[0])
                multiShow.diskPoints.push(Qt.point(ts[0] * 1000, vs[0]))
                for (let i = 1; i < ts.length; i++) {
                    let v = vs[i]
                    let t = ts[i] * 1000
                    let a = as[i]
                    if (a === 1) {
                        multiShow.multiAnomaly.append(t, v)
                    }
                    multiShow.diskSeries.append(t, v)
                    multiShow.diskPoints.push(Qt.point(t, v))
                }
            } else if (index === 4) {
                if (as[0] === 1) {
                    multiShow.multiAnomaly.append(ts[0] * 1000, vs[0])
                }
                multiShow.readSeries.append(ts[0] * 1000, vs[0])
                multiShow.readPoints.push(Qt.point(ts[0] * 1000, vs[0]))
                for (let i = 1; i < ts.length; i++) {
                    let v = vs[i]
                    let t = ts[i] * 1000
                    let a = as[i]
                    if (a === 1) {
                        multiShow.multiAnomaly.append(t, v)
                    }
                    multiShow.readSeries.append(t, v)
                    multiShow.readPoints.push(Qt.point(t, v))
                }
            } else if (index === 5) {
                if (as[0] === 1) {
                    multiShow.multiAnomaly.append(ts[0] * 1000, vs[0])
                }
                multiShow.writeSeries.append(ts[0] * 1000, vs[0])
                multiShow.writePoints.push(Qt.point(ts[0] * 1000, vs[0]))
                for (let i = 1; i < ts.length; i++) {
                    let v = vs[i]
                    let t = ts[i] * 1000
                    let a = as[i]
                    if (a === 1) {
                        multiShow.multiAnomaly.append(t, v)
                    }
                    multiShow.writeSeries.append(t, v)
                    multiShow.writePoints.push(Qt.point(t, v))
                }
            } else if (index === 6) {
                if (as[0] === 1) {
                    multiShow.multiAnomaly.append(ts[0] * 1000, vs[0])
                }
                multiShow.srtSeries.append(ts[0] * 1000, vs[0])
                multiShow.srtPoints.push(Qt.point(ts[0] * 1000, vs[0]))
                for (let i = 1; i < ts.length; i++) {
                    let v = vs[i]
                    let t = ts[i] * 1000
                    let a = as[i]
                    if (a === 1) {
                        multiShow.multiAnomaly.append(t, v)
                    }
                    multiShow.srtSeries.append(t, v)
                    multiShow.srtPoints.push(Qt.point(t, v))
                }
            } else if (index === 7) {
                if (as[0] === 1) {
                    multiShow.multiAnomaly.append(ts[0] * 1000, vs[0])
                }
                multiShow.qpsSeries.append(ts[0] * 1000, vs[0])
                multiShow.qpsPoints.push(Qt.point(ts[0] * 1000, vs[0]))
                for (let i = 1; i < ts.length; i++) {
                    let v = vs[i]
                    let t = ts[i] * 1000
                    let a = as[i]
                    if (a === 1) {
                        multiShow.qpsSeries.append(t, v)
                    }
                    multiShow.srtSeries.append(t, v)
                    multiShow.srtPoints.push(Qt.point(t, v))
                }
            }

            multiShow.minX = new Date(ts[0] * 1000)
            multiShow.maxX = new Date(ts[ts.length - 1] * 1000)
        }
    }

    Connections {
        target: DataManager

        function onUpdateMaxMin(minVal, maxVal) {
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }

            let padding = (maxVal - minVal) * 0.1

            multiShow.minY = minVal - padding
            multiShow.maxY = maxVal + padding
        }
    }
}
