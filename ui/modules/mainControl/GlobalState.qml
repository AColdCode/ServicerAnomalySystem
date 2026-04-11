import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: globalState
    width: parent.width
    height: 80
    border.color: "grey"
    border.width: 1
    radius: 10

    property int serverCount: 0
    property int warningCount: 0
    property int normalCount: 0
    property int abnormalCount: 0

    ColumnLayout {
        anchors.fill: parent

        Text {
            text: "集群整体运行状态"
            font.pixelSize: 20
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
            Layout.leftMargin: 20
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.leftMargin: 20

            ColumnLayout {
                Layout.fillHeight: true

                Text {
                    id: serverCountTxt
                    text: globalState.serverCount
                    font.pixelSize: 30
                    font.bold: true
                    color: "black"
                }

                Text {
                    text: "服务器总数"
                    font.pixelSize: 15
                    color: "black"
                }
            }

            Item {
                Layout.fillWidth: true
            }

            ColumnLayout {
                Layout.fillHeight: true

                Text {
                    id: warningCountTxt
                    text: globalState.warningCount
                    font.pixelSize: 30
                    font.bold: true
                    color: "red"
                }

                Text {
                    text: "警告数量"
                    font.pixelSize: 15
                    color: "black"
                }
            }

            Item {
                Layout.fillWidth: true
            }

            ColumnLayout {
                Layout.fillHeight: true

                Text {
                    id: normalCountTxt
                    text: globalState.normalCount
                    font.pixelSize: 30
                    font.bold: true
                    color: "black"
                }

                Text {
                    text: "正常指标数"
                    font.pixelSize: 15
                    color: "black"
                }
            }

            Item {
                Layout.fillWidth: true
            }

            ColumnLayout {
                Layout.fillHeight: true

                Text {
                    id: abnormalCountTxt
                    text: globalState.abnormalCount
                    font.pixelSize: 30
                    font.bold: true
                    color: "red"
                }

                Text {
                    text: "异常指标数"
                    font.pixelSize: 15
                    color: "black"
                }
            }

            Item {
                Layout.fillWidth: true
            }
        }
    }

    Connections {
        target: DataManager

        function onDataGenerated(server_count, total_rows, start, end) {
            globalState.serverCount = server_count
        }
    }

    Connections {
        target: DataManager

        function onAnomalyNumChanged(anomalyNum) {
            globalState.warningCount = anomalyNum
        }
    }

    Connections {
        target: DataManager

        function onNormalNumChanged(normalNum) {
            globalState.normalCount = normalNum
            globalState.abnormalCount = 8 - normalNum
        }
    }
}