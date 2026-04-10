import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: dataStat
    width: parent.width
    height: 500
    border.color: "grey"
    border.width: 1
    radius: 10

    ColumnLayout {
        anchors.fill: parent
        spacing: 5

        Text {
            Layout.leftMargin: 20
            Layout.topMargin: 20
            Layout.alignment: Qt.AlignLeft
            text: "监控数据生成"
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
                    text: "开始时间"
                    font.pixelSize: 15
                    color: "#65779A"
                }

                TextField {
                    id: startTextField
                    Layout.fillWidth: true
                    text: "2026/01/01 00:00"
                    readOnly: true
                    rightPadding: 40

                    Image {
                        id: startCalendarIcon
                        source: "../../../images/calendar.svg"
                        anchors.right: parent.right
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.rightMargin: 20
                        width: 24
                        height: 24

                        TapHandler {
                            id: startCalendarTapHandler
                            onTapped: {
                                dateTimeDialog.targetTextField = startTextField
                                dateTimeDialog.open()
                            }
                        }
                    }
                }
            }

            Item {
                Layout.fillWidth: true
            }

            ColumnLayout {
                Layout.fillHeight: true

                Text {
                    Layout.alignment: Qt.AlignLeft
                    text: "结束时间"
                    font.pixelSize: 15
                    color: "#65779A"
                }

                TextField {
                    id: endTextField
                    Layout.fillWidth: true
                    text: "2026/01/01 00:00"
                    readOnly: true
                    rightPadding: 40

                    Image {
                        id: endCalendarIcon
                        source: "../../../images/calendar.svg"
                        anchors.right: parent.right
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.rightMargin: 20
                        width: 24
                        height: 24

                        TapHandler {
                            id: endCalendarTapHandler
                            onTapped: {
                                dateTimeDialog.targetTextField = endTextField
                                dateTimeDialog.open()
                            }
                        }
                    }
                }
            }

            Item {
                Layout.fillWidth: true
            }
        }

        Item {
            Layout.fillHeight: true
        }

        ColumnLayout {
            id: server
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            Layout.topMargin: 20
            property int serverNum: 1
            property int minServerNum: 1
            property int maxServerNum: 20
            spacing: -5

            Text {
                Layout.leftMargin: 20
                text: "服务器数量: " + server.serverNum + "台"
                font.pixelSize: 15
                color: "black"
            }

            Slider {
                id: serverNumSlider
                Layout.fillWidth: true
                Layout.preferredHeight: 50
                Layout.leftMargin: 10
                from: server.minServerNum
                to: server.maxServerNum
                stepSize: 1
                snapMode: Slider.SnapAlways
                focus: true
                value: 1
                onValueChanged: {
                    server.serverNum = value
                }
            }

            Text {
                Layout.leftMargin: 20
                text: "范围: " + server.minServerNum + "-" + server.maxServerNum + " 台"
                font.pixelSize: 15
                color: "grey"
            }
        }

        ColumnLayout {
            id: interval
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            Layout.topMargin: 20
            property int intervalCount: 1
            property int minIntervalCount: 1
            property int maxIntervalCount: 10
            spacing: -5

            Text {
                Layout.leftMargin: 20
                text: "数据采样间隔: " + interval.intervalCount + "分钟"
                font.pixelSize: 15
                color: "black"
            }

            Slider {
                id: intervalCountSlider
                Layout.fillWidth: true
                Layout.preferredHeight: 50
                Layout.leftMargin: 10
                from: interval.minIntervalCount
                to: interval.maxIntervalCount
                stepSize: 1
                snapMode: Slider.SnapAlways
                focus: true
                value: 1
                onValueChanged: {
                    interval.intervalCount = value
                }
            }

            Text {
                Layout.leftMargin: 20
                text: "范围: " + interval.minIntervalCount + "-" + interval.maxIntervalCount + " 分钟"
                font.pixelSize: 15
                color: "grey"
            }
        }

        ColumnLayout {
            id: anomaly
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            Layout.topMargin: 20
            property int anomalyRatio: 1
            property int minAnomalyRatio: 1
            property int maxAnomalyRatio: 10
            spacing: -5

            Text {
                Layout.leftMargin: 20
                text: "异常注入比例:  " + anomaly.anomalyRatio + "%"
                font.pixelSize: 15
                color: "black"
            }

            Slider {
                id: anomalyRatioSlider
                Layout.fillWidth: true
                Layout.preferredHeight: 50
                Layout.leftMargin: 10
                from: anomaly.minAnomalyRatio
                to: anomaly.maxAnomalyRatio
                stepSize: 1
                snapMode: Slider.SnapAlways
                focus: true
                value: 1

                onValueChanged: {
                    anomaly.anomalyRatio = value
                }
            }

            Text {
                Layout.leftMargin: 20
                text: "范围: " + anomaly.minAnomalyRatio + "-" + anomaly.maxAnomalyRatio + " %"
                font.pixelSize: 15
                color: "grey"
            }
        }

        Item {
            Layout.fillHeight: true
        }

        Rectangle {
            id: dataGenBtn
            Layout.preferredWidth: 120
            Layout.preferredHeight: 50
            Layout.leftMargin: 20
            radius: 10
            color: isGening ? "#9DC1FA" : dataGenHover.hovered ? "#4F8FF6" : "#3C83F6"

            property bool isGening: false

            RowLayout {
                anchors.fill: parent
                spacing: 10

                Image {
                    id: dataGenIcon
                    visible: !dataGenBtn.isGening
                    source: "../../../images/dataGen.svg"
                    Layout.preferredWidth: 24
                    Layout.preferredHeight: 24
                    Layout.leftMargin: 10
                    fillMode: Image.PreserveAspectFit
                }

                AnimatedImage {
                    visible: dataGenBtn.isGening
                    source: "../../../images/loading.gif"
                    Layout.preferredWidth: 30
                    Layout.preferredHeight: 30
                    Layout.leftMargin: 10

                    playing: true
                    paused: false
                    fillMode: Image.PreserveAspectFit
                }

                Item {
                    Layout.fillWidth: true
                }

                Text {
                    Layout.rightMargin: 10
                    text: dataGenBtn.isGening ? "生成中..." : "生成数据"
                    font.pixelSize: 15
                    color: "white"
                }
            }

            HoverHandler {
                id: dataGenHover
                cursorShape: Qt.PointingHandCursor
            }

            TapHandler {
                id: dataGenTap
                onTapped: {
                    DataManager.genData(server.serverNum, interval.intervalCount, anomaly.anomalyRatio, startTextField.text, endTextField.text)
                    dataGenBtn.isGening = true
                }
            }
        }

        Item {
            Layout.fillHeight: true
        }
    }

    MyCalendar {
        id: dateTimeDialog
        x: parent.width / 2 - width / 2
    }

    Connections {
        target: DataManager

        function onDataGenerated() {
            dataGenBtn.isGening = false
        }
    }
}