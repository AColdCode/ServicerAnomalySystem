import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "multiPredict"

ScrollView {
    id: multiPredict
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

            Evaluates {
                id: evaluates
                Layout.fillWidth: true
                Layout.preferredHeight: 150
                Layout.leftMargin: 20
                Layout.rightMargin: 20
            }

            MultiShow {
                id: multiShow
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.topMargin: 20
                Layout.leftMargin: 20
                Layout.rightMargin: 20
                Layout.bottomMargin: 20
            }
        }
    }

    Connections {
        target: DataManager

        function onMultiPredictUpdated(hTs, hVs, pTs, pVs, scores, evaluate) {
            evaluates.evaluate = evaluate
            evaluates.final_score = scores[0]
            evaluates.volatility = scores[1]
            evaluates.smoothness = scores[2]
            evaluates.trend = scores[3]
            evaluates.anomaly_ratio = scores[4]
            evaluates.jump = scores[5]
            evaluates.monotonic = scores[6]
            evaluates.entropy = scores[7]

            multiShow.cpuChart.hSeries.clear()
            multiShow.cpuChart.pSeries.clear()
            var minVal = hVs[0][0]
            var maxVal = hVs[0][0]
            multiShow.cpuChart.pSeries.append(hTs[hTs.length - 1] * 1000, hVs[0][hVs[0].length - 1])
            for (var i = 0; i < hTs.length - 1; i++) {
                var hV = hVs[0][i]
                var pV = pVs[0][i]
                var ht = hTs[i] * 1000
                var pt = pTs[i] * 1000
                multiShow.cpuChart.hSeries.append(ht, hV)
                multiShow.cpuChart.pSeries.append(pt, pV)
                if (hV < minVal) minVal = hV
                if (hV > maxVal) maxVal = hV
                if (pV < minVal) minVal = pV
                if (pV > maxVal) maxVal = pV
            }
            multiShow.cpuChart.hSeries.append(hTs[hTs.length - 1] * 1000, hVs[0][hVs[0].length - 1])
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }
            var padding = (maxVal - minVal) * 0.1
            multiShow.cpuChart.minY = minVal - padding
            multiShow.cpuChart.maxY = maxVal + padding
            multiShow.cpuChart.minX = new Date(hTs[0] * 1000)
            multiShow.cpuChart.maxX = new Date(pTs[pTs.length - 1] * 1000)
            
            multiShow.rtChart.hSeries.clear()
            multiShow.rtChart.pSeries.clear()
            minVal = hVs[1][0]
            maxVal = hVs[1][0]
            multiShow.rtChart.pSeries.append(hTs[hTs.length - 1] * 1000, hVs[1][hVs[1].length - 1])
            for (var i = 0; i < hTs.length - 1; i++) {
                var hV = hVs[1][i]
                var pV = pVs[1][i]
                var ht = hTs[i] * 1000
                var pt = pTs[i] * 1000
                multiShow.rtChart.hSeries.append(ht, hV)
                multiShow.rtChart.pSeries.append(pt, pV)
                if (hV < minVal) minVal = hV
                if (hV > maxVal) maxVal = hV
                if (pV < minVal) minVal = pV
                if (pV > maxVal) maxVal = pV
            }
            multiShow.rtChart.hSeries.append(hTs[hTs.length - 1] * 1000, hVs[1][hVs[1].length - 1])
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }
            var padding = (maxVal - minVal) * 0.1
            multiShow.rtChart.minY = minVal - padding
            multiShow.rtChart.maxY = maxVal + padding
            multiShow.rtChart.minX = new Date(hTs[0] * 1000)
            multiShow.rtChart.maxX = new Date(pTs[pTs.length - 1] * 1000)
            
            multiShow.memChart.hSeries.clear()
            multiShow.memChart.pSeries.clear()
            minVal = hVs[2][0]
            maxVal = hVs[2][0]
            multiShow.memChart.pSeries.append(hTs[hTs.length - 1] * 1000, hVs[2][hVs[2].length - 1])
            for (var i = 0; i < hTs.length - 1; i++) {
                var hV = hVs[2][i]
                var pV = pVs[2][i]
                var ht = hTs[i] * 1000
                var pt = pTs[i] * 1000
                multiShow.memChart.hSeries.append(ht, hV)
                multiShow.memChart.pSeries.append(pt, pV)
                if (hV < minVal) minVal = hV
                if (hV > maxVal) maxVal = hV
                if (pV < minVal) minVal = pV
                if (pV > maxVal) maxVal = pV
            }
            multiShow.memChart.hSeries.append(hTs[hTs.length - 1] * 1000, hVs[2][hVs[2].length - 1])
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }
            var padding = (maxVal - minVal) * 0.1
            multiShow.memChart.minY = minVal - padding
            multiShow.memChart.maxY = maxVal + padding
            multiShow.memChart.minX = new Date(hTs[0] * 1000)
            multiShow.memChart.maxX = new Date(pTs[pTs.length - 1] * 1000)
            
            multiShow.diskChart.hSeries.clear()
            multiShow.diskChart.pSeries.clear()
            minVal = hVs[3][0]
            maxVal = hVs[3][0]
            multiShow.diskChart.pSeries.append(hTs[hTs.length - 1] * 1000, hVs[3][hVs[3].length - 1])
            for (var i = 0; i < hTs.length - 1; i++) {
                var hV = hVs[3][i]
                var pV = pVs[3][i]
                var ht = hTs[i] * 1000
                var pt = pTs[i] * 1000
                multiShow.diskChart.hSeries.append(ht, hV)
                multiShow.diskChart.pSeries.append(pt, pV)
                if (hV < minVal) minVal = hV
                if (hV > maxVal) maxVal = hV
                if (pV < minVal) minVal = pV
                if (pV > maxVal) maxVal = pV
            }
            multiShow.diskChart.hSeries.append(hTs[hTs.length - 1] * 1000, hVs[3][hVs[3].length - 1])
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }
            var padding = (maxVal - minVal) * 0.1
            multiShow.diskChart.minY = minVal - padding
            multiShow.diskChart.maxY = maxVal + padding
            multiShow.diskChart.minX = new Date(hTs[0] * 1000)
            multiShow.diskChart.maxX = new Date(pTs[pTs.length - 1] * 1000)
            
            multiShow.readChart.hSeries.clear()
            multiShow.readChart.pSeries.clear()
            minVal = hVs[4][0]
            maxVal = hVs[4][0]
            multiShow.readChart.pSeries.append(hTs[hTs.length - 1] * 1000, hVs[4][hVs[4].length - 1])
            for (var i = 0; i < hTs.length - 1; i++) {
                var hV = hVs[4][i]
                var pV = pVs[4][i]
                var ht = hTs[i] * 1000
                var pt = pTs[i] * 1000
                multiShow.readChart.hSeries.append(ht, hV)
                multiShow.readChart.pSeries.append(pt, pV)
                if (hV < minVal) minVal = hV
                if (hV > maxVal) maxVal = hV
                if (pV < minVal) minVal = pV
                if (pV > maxVal) maxVal = pV
            }
            multiShow.readChart.hSeries.append(hTs[hTs.length - 1] * 1000, hVs[4][hVs[4].length - 1])
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }
            var padding = (maxVal - minVal) * 0.1
            multiShow.readChart.minY = minVal - padding
            multiShow.readChart.maxY = maxVal + padding
            multiShow.readChart.minX = new Date(hTs[0] * 1000)
            multiShow.readChart.maxX = new Date(pTs[pTs.length - 1] * 1000)
            
            multiShow.writeChart.hSeries.clear()
            multiShow.writeChart.pSeries.clear()
            minVal = hVs[5][0]
            maxVal = hVs[5][0]
            multiShow.writeChart.pSeries.append(hTs[hTs.length - 1] * 1000, hVs[5][hVs[5].length - 1])
            for (var i = 0; i < hTs.length - 1; i++) {
                var hV = hVs[5][i]
                var pV = pVs[5][i]
                var ht = hTs[i] * 1000
                var pt = pTs[i] * 1000
                multiShow.writeChart.hSeries.append(ht, hV)
                multiShow.writeChart.pSeries.append(pt, pV)
                if (hV < minVal) minVal = hV
                if (hV > maxVal) maxVal = hV
                if (pV < minVal) minVal = pV
                if (pV > maxVal) maxVal = pV
            }
            multiShow.writeChart.hSeries.append(hTs[hTs.length - 1] * 1000, hVs[5][hVs[5].length - 1])
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }
            var padding = (maxVal - minVal) * 0.1
            multiShow.writeChart.minY = minVal - padding
            multiShow.writeChart.maxY = maxVal + padding
            multiShow.writeChart.minX = new Date(hTs[0] * 1000)
            multiShow.writeChart.maxX = new Date(pTs[pTs.length - 1] * 1000)
            
            multiShow.srtChart.hSeries.clear()
            multiShow.srtChart.pSeries.clear()
            minVal = hVs[6][0]
            maxVal = hVs[6][0]
            multiShow.srtChart.pSeries.append(hTs[hTs.length - 1] * 1000, hVs[6][hVs[6].length - 1])
            for (var i = 0; i < hTs.length - 1; i++) {
                var hV = hVs[6][i]
                var pV = pVs[6][i]
                var ht = hTs[i] * 1000
                var pt = pTs[i] * 1000
                multiShow.srtChart.hSeries.append(ht, hV)
                multiShow.srtChart.pSeries.append(pt, pV)
                if (hV < minVal) minVal = hV
                if (hV > maxVal) maxVal = hV
                if (pV < minVal) minVal = pV
                if (pV > maxVal) maxVal = pV
            }
            multiShow.srtChart.hSeries.append(hTs[hTs.length - 1] * 1000, hVs[6][hVs[6].length - 1])
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }
            var padding = (maxVal - minVal) * 0.1
            multiShow.srtChart.minY = minVal - padding
            multiShow.srtChart.maxY = maxVal + padding
            multiShow.srtChart.minX = new Date(hTs[0] * 1000)
            multiShow.srtChart.maxX = new Date(pTs[pTs.length - 1] * 1000)
            
            multiShow.qpsChart.hSeries.clear()
            multiShow.qpsChart.pSeries.clear()
            minVal = hVs[7][0]
            maxVal = hVs[7][0]
            multiShow.qpsChart.pSeries.append(hTs[hTs.length - 1] * 1000, hVs[7][hVs[7].length - 1])
            for (var i = 0; i < hTs.length - 1; i++) {
                var hV = hVs[7][i]
                var pV = pVs[7][i]
                var ht = hTs[i] * 1000
                var pt = pTs[i] * 1000
                multiShow.qpsChart.hSeries.append(ht, hV)
                multiShow.qpsChart.pSeries.append(pt, pV)
                if (hV < minVal) minVal = hV
                if (hV > maxVal) maxVal = hV
                if (pV < minVal) minVal = pV
                if (pV > maxVal) maxVal = pV
            }
            multiShow.qpsChart.hSeries.append(hTs[hTs.length - 1] * 1000, hVs[7][hVs[7].length - 1])
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }
            var padding = (maxVal - minVal) * 0.1
            multiShow.qpsChart.minY = minVal - padding
            multiShow.qpsChart.maxY = maxVal + padding
            multiShow.qpsChart.minX = new Date(hTs[0] * 1000)
            multiShow.qpsChart.maxX = new Date(pTs[pTs.length - 1] * 1000)
        }
    }
}
