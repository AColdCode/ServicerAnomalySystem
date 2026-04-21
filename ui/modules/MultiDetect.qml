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
                multiShow.cpuSeries.clear()

                if (as[0] === 1) {
                    multiShow.multiAnomaly.append(ts[0] * 1000, vs[0])
                }
                multiShow.cpuSeries.append(ts[0], vs[0])
                for (var i = 1; i < ts.length; i++) {
                    var v = vs[i]
                    var t = ts[i] * 1000
                    var a = as[i]
                    if (a === 1) {
                        multiShow.multiAnomaly.append(t, v)
                    }
                    multiShow.cpuSeries.append(t, v)
                }
            } else if (index === 1) {
                multiShow.rtSeries.clear()

                if (as[0] === 1) {
                    multiShow.multiAnomaly.append(ts[0] * 1000, vs[0])
                }
                multiShow.rtSeries.append(ts[0], vs[0])
                for (var i = 1; i < ts.length; i++) {
                    var v = vs[i]
                    var t = ts[i] * 1000
                    var a = as[i]
                    if (a === 1) {
                        multiShow.multiAnomaly.append(t, v)
                    }
                    multiShow.rtSeries.append(t, v)
                }
            } else if (index === 2) {
                multiShow.memSeries.clear()

                if (as[0] === 1) {
                    multiShow.anomaly.append(ts[0] * 1000, vs[0])
                }
                multiShow.memSeries.append(ts[0], vs[0])
                for (var i = 1; i < ts.length; i++) {
                    var v = vs[i]
                    var t = ts[i] * 1000
                    var a = as[i]
                    if (a === 1) {
                        multiShow.multiAnomaly.append(t, v)
                    }
                    multiShow.memSeries.append(t, v)
                }
            } else if (index === 3) {
                multiShow.diskSeries.clear()

                if (as[0] === 1) {
                    multiShow.multiAnomaly.append(ts[0] * 1000, vs[0])
                }
                multiShow.diskSeries.append(ts[0], vs[0])
                for (var i = 1; i < ts.length; i++) {
                    var v = vs[i]
                    var t = ts[i] * 1000
                    var a = as[i]
                    if (a === 1) {
                        multiShow.multiAnomaly.append(t, v)
                    }
                    multiShow.diskSeries.append(t, v)
                }
            } else if (index === 4) {
                multiShow.readSeries.clear()

                if (as[0] === 1) {
                    multiShow.multiAnomaly.append(ts[0] * 1000, vs[0])
                }
                multiShow.readSeries.append(ts[0], vs[0])
                for (var i = 1; i < ts.length; i++) {
                    var v = vs[i]
                    var t = ts[i] * 1000
                    var a = as[i]
                    if (a === 1) {
                        multiShow.multiAnomaly.append(t, v)
                    }
                    multiShow.readSeries.append(t, v)
                }
            } else if (index === 5) {
                multiShow.writeSeries.clear()

                if (as[0] === 1) {
                    multiShow.multiAnomaly.append(ts[0] * 1000, vs[0])
                }
                multiShow.writeSeries.append(ts[0], vs[0])
                for (var i = 1; i < ts.length; i++) {
                    var v = vs[i]
                    var t = ts[i] * 1000
                    var a = as[i]
                    if (a === 1) {
                        multiShow.multiAnomaly.append(t, v)
                    }
                    multiShow.writeSeries.append(t, v)
                }
            } else if (index === 6) {
                multiShow.srtSeries.clear()

                if (as[0] === 1) {
                    multiShow.multiAnomaly.append(ts[0] * 1000, vs[0])
                }
                multiShow.srtSeries.append(ts[0], vs[0])
                for (var i = 1; i < ts.length; i++) {
                    var v = vs[i]
                    var t = ts[i] * 1000
                    var a = as[i]
                    if (a === 1) {
                        multiShow.multiAnomaly.append(t, v)
                    }
                    multiShow.srtSeries.append(t, v)
                }
            } else if (index === 7) {
                multiShow.qpsSeries.clear()

                if (as[0] === 1) {
                    multiShow.multiAnomaly.append(ts[0] * 1000, vs[0])
                }
                multiShow.qpsSeries.append(ts[0], vs[0])
                for (var i = 1; i < ts.length; i++) {
                    var v = vs[i]
                    var t = ts[i] * 1000
                    var a = as[i]
                    if (a === 1) {
                        multiShow.qpsSeries.append(t, v)
                    }
                    multiShow.srtSeries.append(t, v)
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

            var padding = (maxVal - minVal) * 0.1

            multiShow.minY = minVal - padding
            multiShow.maxY = maxVal + padding
        }
    }
}
