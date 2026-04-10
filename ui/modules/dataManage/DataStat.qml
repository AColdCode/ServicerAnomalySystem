import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: dataStat
    width: parent.width
    height: 100
    border.color: "grey"
    border.width: 1
    radius: 10

    property int serverNum: 0
    property int recordNum: 0
    property int alarmNum: 0
    property string startTime: ""
    property string endTime: ""

    ColumnLayout {
        anchors.fill: parent
        spacing: 5

        Text {
            Layout.leftMargin: 20
            Layout.topMargin: 20
            Layout.alignment: Qt.AlignLeft
            text: "数据统计"
            font.pixelSize: 20
            color: "black"
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.leftMargin: 20
            Layout.rightMargin: 20
            spacing: 10

            ColumnLayout {
                Layout.fillHeight: true

                Text {
                    Layout.alignment: Qt.AlignLeft
                    text: "服务器总数"
                    font.pixelSize: 15
                    color: "#65779A"
                }

                Text {
                    Layout.alignment: Qt.AlignLeft
                    text: serverNum
                    font.pixelSize: 30
                    color: "black"
                }
            }

            Item {
                Layout.fillWidth: true
            }

            ColumnLayout {
                Layout.fillHeight: true

                Text {
                    Layout.alignment: Qt.AlignLeft
                    text: "监控记录数"
                    font.pixelSize: 15
                    color: "#65779A"
                }

                Text {
                    Layout.alignment: Qt.AlignLeft
                    text: recordNum
                    font.pixelSize: 30
                    color: "black"
                }
            }

            Item {
                Layout.fillWidth: true
            }

            ColumnLayout {
                Layout.fillHeight: true

                Text {
                    Layout.alignment: Qt.AlignLeft
                    text: "异常告警数"
                    font.pixelSize: 15
                    color: "#65779A"
                }

                Text {
                    Layout.alignment: Qt.AlignLeft
                    text: alarmNum
                    font.pixelSize: 30
                    color: "black"
                }
            }

            Item {
                Layout.fillWidth: true
            }
        }

        Rectangle {
            Layout.preferredHeight: 1
            Layout.fillWidth: true
            Layout.leftMargin: 20
            Layout.rightMargin: 20
            color: "grey"
        }

        Text {
            Layout.alignment: Qt.AlignLeft
            Layout.leftMargin: 20
            Layout.bottomMargin: 20
            text: "数据时间范围: " + dataStat.startTime + " 至 " + dataStat.endTime
            font.pixelSize: 12
            color: "grey"
        }
    }

    Component.onCompleted: {
        DataManager.genFinished()
    }

    Connections {
        target: DataManager

        function onDataGenerated(server_count, total_rows, start, end) {
            dataStat.serverNum = server_count
            dataStat.recordNum = total_rows
            dataStat.startTime = start
            dataStat.endTime = end
        }
    }

    Connections {
        target: DataManager

        function onDataDeleted(server_count, total_rows, start, end) {
            dataStat.serverNum = server_count
            dataStat.recordNum = total_rows
            dataStat.startTime = start
            dataStat.endTime = end
        }
    }
}