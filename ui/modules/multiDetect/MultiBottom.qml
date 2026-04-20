import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

Rectangle {
    id: anomalyList
    radius: 10
    width: parent.width

    property real acc: 0.0
    property int num: 0

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        // ================= 标题栏 =================
        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            Layout.topMargin: 10

            Text {
                Layout.leftMargin: 20
                text: "异常事件数量：" + anomalyList.num
                font.pixelSize: 20
                color: "black"
            }

            Item { Layout.fillWidth: true }

            Text {
                text: "异常检测准确率：" + anomalyList.acc + "%"
                font.pixelSize: 20
                color: "black"
            }

            Item { Layout.fillWidth: true }

            Rectangle {
                id: refreshBtn
                Layout.preferredWidth: 30
                Layout.preferredHeight: 30
                Layout.rightMargin: 20
                radius: 5
                color: refresh_hover.hovered ? "#D4E0ED" : anomalyList.color

                Image {
                    anchors.fill: parent
                    source: "../../../images/refresh.svg"
                    fillMode: Image.PreserveAspectFit
                }

                HoverHandler { id: refresh_hover }

                TapHandler {
                    onTapped: {
                        DataManager.refreshAnomalyData()
                    }
                }
            }
        }

        // ================= 表头 =================
        RowLayout {
            id: tableHeader
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            Layout.leftMargin: 20

            property string topColor: "#6588BC"

            Text { text: "时间"; Layout.preferredWidth: 170; color: tableHeader.topColor }
            Text { text: "异常评分"; Layout.preferredWidth: 100; color: tableHeader.topColor }
            Text { text: "状态"; Layout.preferredWidth: 80; color: tableHeader.topColor }
            Text { text: "处理"; Layout.preferredWidth: 60; color: tableHeader.topColor }
            Text { text: "异常原因"; Layout.preferredWidth: 120; color: tableHeader.topColor }

            Item { Layout.fillWidth: true }

            Text {
                text: "操作"
                Layout.rightMargin: 50
                color: tableHeader.topColor
            }
        }

        // ================= 列表 =================
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 500
            Layout.leftMargin: 10
            Layout.rightMargin: 10
            radius: 5
            color: anomalyList.color

            ListView {
                id: listView
                anchors.fill: parent
                clip: true

                model: DataManager.anomalyModel

                property real savedContentY: 0

                ScrollBar.vertical: ScrollBar {}

                delegate: Rectangle {
                    id: itemRet
                    width: listView.width
                    height: 40

                    property int timestamp: model.timestamp

                    color: model.is_anomaly === 1
                           ? (model.is_handled === 0 ? "#FFECEC" : "#F2F2F2")
                           : "white"

                    RowLayout {
                        anchors.fill: parent
                        spacing: 20

                        // 时间
                        Text {
                            Layout.leftMargin: 10
                            Layout.preferredWidth: 150
                            text: model.time
                        }

                        // score
                        Text {
                            Layout.preferredWidth: 80
                            text: Number(model.score).toFixed(2)
                            color: model.score > 70 ? "red" : "black"
                        }

                        // 是否异常
                        Rectangle {
                            Layout.preferredWidth: 60
                            Layout.preferredHeight: 25
                            radius: 5
                            color: model.is_anomaly === 1 ? "#FF6B6B" : "#E2EBF3"

                            Text {
                                anchors.centerIn: parent
                                text: model.is_anomaly === 1 ? "异常" : "正常"
                                color: model.is_anomaly === 1 ? "white" : "black"
                                font.pixelSize: 13
                            }
                        }

                        // 是否处理
                        Rectangle {
                            Layout.preferredWidth: 60
                            Layout.preferredHeight: 25
                            radius: 5
                            color: model.is_handled === 1 ? "#4CAF50" : "#FFC107"

                            Text {
                                anchors.centerIn: parent
                                text: model.is_handled === 1 ? "已处理" : "未处理"
                                color: "white"
                                font.pixelSize: 13
                            }
                        }

                        // 异常原因
                        Text {
                            Layout.preferredWidth: 120
                            text: model.top_metric ? model.top_metric : "-"
                        }

                        Item { Layout.fillWidth: true }

                        // ===== 操作按钮 =====
                        Rectangle {
                            visible: model.is_anomaly === 1 && model.is_handled === 0
                            Layout.preferredWidth: 60
                            Layout.preferredHeight: 25
                            Layout.rightMargin: 30
                            radius: 5
                            color: handle_hover.hovered ? "#81C784" : "#A5D6A7"

                            Text {
                                anchors.centerIn: parent
                                text: "处理"
                                font.pixelSize: 13
                            }

                            HoverHandler { id: handle_hover }

                            TapHandler {
                                onTapped: {
                                    DataManager.markAnomalyHandled(itemRet.timestamp)
                                    listView.savePosition()
                                    DataManager.refreshAnomalyData()
                                }
                            }
                        }
                    }

                    HoverHandler { id: row_hover }

                    Rectangle {
                        anchors.bottom: parent.bottom
                        width: parent.width
                        height: 1
                        color: "#DDDDDD"
                    }
                }

                function savePosition() {
                    savedContentY = contentY
                }

                function restorePosition() {
                    contentY = savedContentY
                }

                Connections {
                    target: DataManager
                    function onAnomalyModelChanged() {
                        listView.restorePosition()
                    }
                }

                Connections {
                    target: DataManager
                    function onAnomalyTopChanged(acc, num) {
                        anomalyList.acc = acc
                        anomalyList.num = num
                    }
                }
            }

            Component.onCompleted: {
                DataManager.refreshAnomalyData()
            }
        }
    }
}