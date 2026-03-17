import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "charts"
import "components"

ApplicationWindow {

    id: root

    visible: true
    width: 1600
    height: 900

    title: "Server Situation Monitoring System"

    color: "#1e1e1e"

    RowLayout {

        anchors.fill: parent

        // ===============================
        // 左侧导航
        // ===============================

        SideBar{
            id: sideBar
            Layout.preferredWidth: 220
            Layout.fillHeight: true
        }


        // ===============================
        // 主区域
        // ===============================

        ColumnLayout {

            Layout.fillWidth: true
            Layout.fillHeight: true

            // ===============================
            // 顶部栏
            // ===============================
            TopBar {
                id: topBar
                Layout.fillWidth: true
                Layout.preferredHeight: 60
            }

            // ===============================
            // 页面区域
            // ===============================

            StackLayout {

                id: pageStack

                Layout.fillWidth: true
                Layout.fillHeight: true

                currentIndex: sideBar.currentIndex

                SingleMetricChart{
                    id: singleMetricChart
                }

                MultiMetricChart{
                    id: multiMetricChart
                }

                SinglePredictChart {
                    id: singlePredictChart
                }

                MultiPredictChart {
                    id: multiPredictChart
                }
            }
        }
    }
}