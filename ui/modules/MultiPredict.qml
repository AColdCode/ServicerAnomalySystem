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
            evaluates.risk_intensity = scores[1]
            evaluates.risk_peak = scores[2]
            evaluates.risk_ratio = scores[3]
            evaluates.correlation_change = scores[4]

            multiShow.cpuChart.hSeries.clear()
            multiShow.cpuChart.pSeries.clear()
            multiShow.cpuChart.qmlPoints = []
            multiShow.cpuChart.qmlPrePoints = []
            let minVal = hVs[0][0]
            let maxVal = hVs[0][0]
            multiShow.cpuChart.pSeries.append(hTs[hTs.length - 1] * 1000, hVs[0][hVs[0].length - 1])
            multiShow.cpuChart.qmlPrePoints.push(Qt.point(hTs[hTs.length - 1] * 1000, hVs[0][hVs[0].length - 1]))
            for (let i = 0; i < hTs.length - 1; i++) {
                let hV = hVs[0][i]
                let pV = pVs[0][i]
                let ht = hTs[i] * 1000
                let pt = pTs[i] * 1000
                multiShow.cpuChart.hSeries.append(ht, hV)
                multiShow.cpuChart.pSeries.append(pt, pV)
                multiShow.cpuChart.qmlPoints.push(Qt.point(ht, hV))
                multiShow.cpuChart.qmlPrePoints.push(Qt.point(pt, pV))
                if (hV < minVal) minVal = hV
                if (hV > maxVal) maxVal = hV
                if (pV < minVal) minVal = pV
                if (pV > maxVal) maxVal = pV
            }
            multiShow.cpuChart.hSeries.append(hTs[hTs.length - 1] * 1000, hVs[0][hVs[0].length - 1])
            multiShow.cpuChart.qmlPoints.push(Qt.point(hTs[hTs.length - 1] * 1000, hVs[0][hVs[0].length - 1]))
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }
            let padding = (maxVal - minVal) * 0.1
            multiShow.cpuChart.minY = minVal - padding
            multiShow.cpuChart.maxY = maxVal + padding
            multiShow.cpuChart.minX = new Date(hTs[0] * 1000)
            multiShow.cpuChart.maxX = new Date(pTs[pTs.length - 1] * 1000)
            
            multiShow.rtChart.hSeries.clear()
            multiShow.rtChart.pSeries.clear()
            multiShow.rtChart.qmlPoints = []
            multiShow.rtChart.qmlPrePoints = []
            minVal = hVs[1][0]
            maxVal = hVs[1][0]
            multiShow.rtChart.pSeries.append(hTs[hTs.length - 1] * 1000, hVs[1][hVs[1].length - 1])
            multiShow.rtChart.qmlPrePoints.push(Qt.point(hTs[hTs.length - 1] * 1000, hVs[1][hVs[1].length - 1]))
            for (let i = 0; i < hTs.length - 1; i++) {
                let hV = hVs[1][i]
                let pV = pVs[1][i]
                let ht = hTs[i] * 1000
                let pt = pTs[i] * 1000
                multiShow.rtChart.hSeries.append(ht, hV)
                multiShow.rtChart.pSeries.append(pt, pV)
                multiShow.rtChart.qmlPoints.push(Qt.point(ht, hV))
                multiShow.rtChart.qmlPrePoints.push(Qt.point(pt, pV))
                if (hV < minVal) minVal = hV
                if (hV > maxVal) maxVal = hV
                if (pV < minVal) minVal = pV
                if (pV > maxVal) maxVal = pV
            }
            multiShow.rtChart.hSeries.append(hTs[hTs.length - 1] * 1000, hVs[1][hVs[1].length - 1])
            multiShow.rtChart.qmlPoints.push(Qt.point(hTs[hTs.length - 1] * 1000, hVs[1][hVs[1].length - 1]))
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }
            padding = (maxVal - minVal) * 0.1
            multiShow.rtChart.minY = minVal - padding
            multiShow.rtChart.maxY = maxVal + padding
            multiShow.rtChart.minX = new Date(hTs[0] * 1000)
            multiShow.rtChart.maxX = new Date(pTs[pTs.length - 1] * 1000)
            
            multiShow.memChart.hSeries.clear()
            multiShow.memChart.pSeries.clear()
            multiShow.memChart.qmlPoints = []
            multiShow.memChart.qmlPrePoints = []
            minVal = hVs[2][0]
            maxVal = hVs[2][0]
            multiShow.memChart.pSeries.append(hTs[hTs.length - 1] * 1000, hVs[2][hVs[2].length - 1])
            multiShow.memChart.qmlPrePoints.push(Qt.point(hTs[hTs.length - 1] * 1000, hVs[2][hVs[2].length - 1]))
            for (let i = 0; i < hTs.length - 1; i++) {
                let hV = hVs[2][i]
                let pV = pVs[2][i]
                let ht = hTs[i] * 1000
                let pt = pTs[i] * 1000
                multiShow.memChart.hSeries.append(ht, hV)
                multiShow.memChart.pSeries.append(pt, pV)
                multiShow.memChart.qmlPoints.push(Qt.point(ht, hV))
                multiShow.memChart.qmlPrePoints.push(Qt.point(pt, pV))
                if (hV < minVal) minVal = hV
                if (hV > maxVal) maxVal = hV
                if (pV < minVal) minVal = pV
                if (pV > maxVal) maxVal = pV
            }
            multiShow.memChart.hSeries.append(hTs[hTs.length - 1] * 1000, hVs[2][hVs[2].length - 1])
            multiShow.memChart.qmlPoints.push(Qt.point(hTs[hTs.length - 1] * 1000, hVs[2][hVs[2].length - 1]))
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }
            padding = (maxVal - minVal) * 0.1
            multiShow.memChart.minY = minVal - padding
            multiShow.memChart.maxY = maxVal + padding
            multiShow.memChart.minX = new Date(hTs[0] * 1000)
            multiShow.memChart.maxX = new Date(pTs[pTs.length - 1] * 1000)
            
            multiShow.diskChart.hSeries.clear()
            multiShow.diskChart.pSeries.clear()
            multiShow.diskChart.qmlPoints = []
            multiShow.diskChart.qmlPrePoints = []
            minVal = hVs[3][0]
            maxVal = hVs[3][0]
            multiShow.diskChart.pSeries.append(hTs[hTs.length - 1] * 1000, hVs[3][hVs[3].length - 1])
            multiShow.diskChart.qmlPrePoints.push(Qt.point(hTs[hTs.length - 1] * 1000, hVs[3][hVs[3].length - 1]))
            for (let i = 0; i < hTs.length - 1; i++) {
                let hV = hVs[3][i]
                let pV = pVs[3][i]
                let ht = hTs[i] * 1000
                let pt = pTs[i] * 1000
                multiShow.diskChart.hSeries.append(ht, hV)
                multiShow.diskChart.pSeries.append(pt, pV)
                multiShow.diskChart.qmlPoints.push(Qt.point(ht, hV))
                multiShow.diskChart.qmlPrePoints.push(Qt.point(pt, pV))
                if (hV < minVal) minVal = hV
                if (hV > maxVal) maxVal = hV
                if (pV < minVal) minVal = pV
                if (pV > maxVal) maxVal = pV
            }
            multiShow.diskChart.hSeries.append(hTs[hTs.length - 1] * 1000, hVs[3][hVs[3].length - 1])
            multiShow.diskChart.qmlPoints.push(Qt.point(hTs[hTs.length - 1] * 1000, hVs[3][hVs[3].length - 1]))
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }
            padding = (maxVal - minVal) * 0.1
            multiShow.diskChart.minY = minVal - padding
            multiShow.diskChart.maxY = maxVal + padding
            multiShow.diskChart.minX = new Date(hTs[0] * 1000)
            multiShow.diskChart.maxX = new Date(pTs[pTs.length - 1] * 1000)
            
            multiShow.readChart.hSeries.clear()
            multiShow.readChart.pSeries.clear()
            multiShow.readChart.qmlPoints = []
            multiShow.readChart.qmlPrePoints = []
            minVal = hVs[4][0]
            maxVal = hVs[4][0]
            multiShow.readChart.pSeries.append(hTs[hTs.length - 1] * 1000, hVs[4][hVs[4].length - 1])
            multiShow.readChart.qmlPrePoints.push(Qt.point(hTs[hTs.length - 1] * 1000, hVs[4][hVs[4].length - 1]))
            for (let i = 0; i < hTs.length - 1; i++) {
                let hV = hVs[4][i]
                let pV = pVs[4][i]
                let ht = hTs[i] * 1000
                let pt = pTs[i] * 1000
                multiShow.readChart.hSeries.append(ht, hV)
                multiShow.readChart.pSeries.append(pt, pV)
                multiShow.readChart.qmlPoints.push(Qt.point(ht, hV))
                multiShow.readChart.qmlPrePoints.push(Qt.point(pt, pV))
                if (hV < minVal) minVal = hV
                if (hV > maxVal) maxVal = hV
                if (pV < minVal) minVal = pV
                if (pV > maxVal) maxVal = pV
            }
            multiShow.readChart.hSeries.append(hTs[hTs.length - 1] * 1000, hVs[4][hVs[4].length - 1])
            multiShow.readChart.qmlPoints.push(Qt.point(hTs[hTs.length - 1] * 1000, hVs[4][hVs[4].length - 1]))
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }
            padding = (maxVal - minVal) * 0.1
            multiShow.readChart.minY = minVal - padding
            multiShow.readChart.maxY = maxVal + padding
            multiShow.readChart.minX = new Date(hTs[0] * 1000)
            multiShow.readChart.maxX = new Date(pTs[pTs.length - 1] * 1000)
            
            multiShow.writeChart.hSeries.clear()
            multiShow.writeChart.pSeries.clear()
            multiShow.writeChart.qmlPoints = []
            multiShow.writeChart.qmlPrePoints = []
            minVal = hVs[5][0]
            maxVal = hVs[5][0]
            multiShow.writeChart.pSeries.append(hTs[hTs.length - 1] * 1000, hVs[5][hVs[5].length - 1])
            multiShow.writeChart.qmlPrePoints.push(Qt.point(hTs[hTs.length - 1] * 1000, hVs[5][hVs[5].length - 1]))
            for (let i = 0; i < hTs.length - 1; i++) {
                let hV = hVs[5][i]
                let pV = pVs[5][i]
                let ht = hTs[i] * 1000
                let pt = pTs[i] * 1000
                multiShow.writeChart.hSeries.append(ht, hV)
                multiShow.writeChart.pSeries.append(pt, pV)
                multiShow.writeChart.qmlPoints.push(Qt.point(ht, hV))
                multiShow.writeChart.qmlPrePoints.push(Qt.point(pt, pV))
                if (hV < minVal) minVal = hV
                if (hV > maxVal) maxVal = hV
                if (pV < minVal) minVal = pV
                if (pV > maxVal) maxVal = pV
            }
            multiShow.writeChart.hSeries.append(hTs[hTs.length - 1] * 1000, hVs[5][hVs[5].length - 1])
            multiShow.writeChart.qmlPoints.push(Qt.point(hTs[hTs.length - 1] * 1000, hVs[5][hVs[5].length - 1]))
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }
            padding = (maxVal - minVal) * 0.1
            multiShow.writeChart.minY = minVal - padding
            multiShow.writeChart.maxY = maxVal + padding
            multiShow.writeChart.minX = new Date(hTs[0] * 1000)
            multiShow.writeChart.maxX = new Date(pTs[pTs.length - 1] * 1000)
            
            multiShow.srtChart.hSeries.clear()
            multiShow.srtChart.pSeries.clear()
            multiShow.srtChart.qmlPoints = []
            multiShow.srtChart.qmlPrePoints = []
            minVal = hVs[6][0]
            maxVal = hVs[6][0]
            multiShow.srtChart.pSeries.append(hTs[hTs.length - 1] * 1000, hVs[6][hVs[6].length - 1])
            multiShow.srtChart.qmlPrePoints.push(Qt.point(hTs[hTs.length - 1] * 1000, hVs[6][hVs[6].length - 1]))
            for (let i = 0; i < hTs.length - 1; i++) {
                let hV = hVs[6][i]
                let pV = pVs[6][i]
                let ht = hTs[i] * 1000
                let pt = pTs[i] * 1000
                multiShow.srtChart.hSeries.append(ht, hV)
                multiShow.srtChart.pSeries.append(pt, pV)
                multiShow.srtChart.qmlPoints.push(Qt.point(ht, hV))
                multiShow.srtChart.qmlPrePoints.push(Qt.point(pt, pV))
                if (hV < minVal) minVal = hV
                if (hV > maxVal) maxVal = hV
                if (pV < minVal) minVal = pV
                if (pV > maxVal) maxVal = pV
            }
            multiShow.srtChart.hSeries.append(hTs[hTs.length - 1] * 1000, hVs[6][hVs[6].length - 1])
            multiShow.srtChart.qmlPoints.push(Qt.point(hTs[hTs.length - 1] * 1000, hVs[6][hVs[6].length - 1]))
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }
            padding = (maxVal - minVal) * 0.1
            multiShow.srtChart.minY = minVal - padding
            multiShow.srtChart.maxY = maxVal + padding
            multiShow.srtChart.minX = new Date(hTs[0] * 1000)
            multiShow.srtChart.maxX = new Date(pTs[pTs.length - 1] * 1000)
            
            multiShow.qpsChart.hSeries.clear()
            multiShow.qpsChart.pSeries.clear()
            multiShow.qpsChart.qmlPoints = []
            multiShow.qpsChart.qmlPrePoints = []
            minVal = hVs[7][0]
            maxVal = hVs[7][0]
            multiShow.qpsChart.pSeries.append(hTs[hTs.length - 1] * 1000, hVs[7][hVs[7].length - 1])
            multiShow.qpsChart.qmlPrePoints.push(Qt.point(hTs[hTs.length - 1] * 1000, hVs[7][hVs[7].length - 1]))
            for (let i = 0; i < hTs.length - 1; i++) {
                let hV = hVs[7][i]
                let pV = pVs[7][i]
                let ht = hTs[i] * 1000
                let pt = pTs[i] * 1000
                multiShow.qpsChart.hSeries.append(ht, hV)
                multiShow.qpsChart.pSeries.append(pt, pV)
                multiShow.qpsChart.qmlPoints.push(Qt.point(ht, hV))
                multiShow.qpsChart.qmlPrePoints.push(Qt.point(pt, pV))
                if (hV < minVal) minVal = hV
                if (hV > maxVal) maxVal = hV
                if (pV < minVal) minVal = pV
                if (pV > maxVal) maxVal = pV
            }
            multiShow.qpsChart.hSeries.append(hTs[hTs.length - 1] * 1000, hVs[7][hVs[7].length - 1])
            multiShow.qpsChart.qmlPoints.push(Qt.point(hTs[hTs.length - 1] * 1000, hVs[7][hVs[7].length - 1]))
            if (minVal === maxVal) {
                minVal -= 1
                maxVal += 1
            }
            padding = (maxVal - minVal) * 0.1
            multiShow.qpsChart.minY = minVal - padding
            multiShow.qpsChart.maxY = maxVal + padding
            multiShow.qpsChart.minX = new Date(hTs[0] * 1000)
            multiShow.qpsChart.maxX = new Date(pTs[pTs.length - 1] * 1000)
        }
    }
}
