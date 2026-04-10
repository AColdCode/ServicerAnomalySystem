import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: dataClear
    width: parent.width
    height: 80
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
            text: "数据清理"
            font.pixelSize: 20
            color: "black"
        }

        Text {
            Layout.leftMargin: 20
            Layout.bottomMargin: 10
            Layout.alignment: Qt.AlignLeft
            text: "清空指定时间范围内的历史监控数据和异常告警记录"
            font.pixelSize: 15
            color: "grey"
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
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        Rectangle {
            id: dataClearBtn
            Layout.preferredWidth: 120
            Layout.preferredHeight: 50
            Layout.leftMargin: 20
            radius: 10
            color: dataClearHover.hovered ? "#F05656" : "#EF4343"

            property bool isClearing: false

            RowLayout {
                anchors.fill: parent
                spacing: 10

                Image {
                    id: dataClearIcon
                    visible: !dataClearBtn.isClearing
                    source: "../../../images/dataDelete.svg"
                    Layout.preferredWidth: 24
                    Layout.preferredHeight: 24
                    Layout.leftMargin: 10
                    fillMode: Image.PreserveAspectFit
                }

                AnimatedImage {
                    visible: dataClearBtn.isClearing
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
                    text: dataClearBtn.isClearing ? "正在清空..." : "清空数据"
                    font.pixelSize: 15
                    color: "white"
                }
            }

            HoverHandler {
                id: dataClearHover
                cursorShape: Qt.PointingHandCursor
            }

            TapHandler {
                id: dataClearTap
                onTapped: {
                    DataManager.deleteDataset(startTextField.text, endTextField.text)
                    dataClearBtn.isClearing = true
                }
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    MyCalendar {
        id: dateTimeDialog
        x: parent.width / 2 - width / 2
        y: -height
    }

    Connections {
        target: DataManager

        function onDataDeleted() {
            dataClearBtn.isClearing = false
        }
    }
}