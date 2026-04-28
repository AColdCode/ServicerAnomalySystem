import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: selectMetric
    color: "white"

    ColumnLayout {
        anchors.fill: parent

        Label {
            Layout.fillWidth: true
            Layout.leftMargin: 10
            Layout.topMargin: 10
            text: "选择监控指标"
            font.pixelSize: 20
            color: "black"
            Layout.alignment: Qt.AlignHCenter
        }

        GridLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            columns: 4

            CheckBox {
                text: "CPU使用率"
                Layout.fillWidth: true
                checked: true

                onCheckedChanged: {
                    if (!checked) {
                        DataManager.cancelMDetectMetric(0)
                    } else {
                        DataManager.setMDetectMetric(0)
                    }
                }
            }
            CheckBox {
                text: "CPU响应时间"
                Layout.fillWidth: true

                onCheckedChanged: {
                    if (!checked) {
                        DataManager.cancelMDetectMetric(1)
                    } else {
                        DataManager.setMDetectMetric(1)
                    }
                }
            }
            CheckBox {
                text: "内存使用率"
                Layout.fillWidth: true

                onCheckedChanged: {
                    if (!checked) {
                        DataManager.cancelMDetectMetric(2)
                    } else {
                        DataManager.setMDetectMetric(2)
                    }
                }
            }
            CheckBox {
                text: "磁盘使用率"
                Layout.fillWidth: true

                onCheckedChanged: {
                    if (!checked) {
                        DataManager.cancelMDetectMetric(3)
                    } else {
                        DataManager.setMDetectMetric(3)
                    }
                }
            }

            CheckBox {
                text: "磁盘读吞吐量"
                Layout.fillWidth: true

                onCheckedChanged: {
                    if (!checked) {
                        DataManager.cancelMDetectMetric(4)
                    } else {
                        DataManager.setMDetectMetric(4)
                    }
                }
            }
            CheckBox {
                text: "磁盘写吞吐量"
                Layout.fillWidth: true

                onCheckedChanged: {
                    if (!checked) {
                        DataManager.cancelMDetectMetric(5)
                    } else {
                        DataManager.setMDetectMetric(5)
                    }
                }
            }
            CheckBox {
                text: "服务响应时间"
                Layout.fillWidth: true

                onCheckedChanged: {
                    if (!checked) {
                        DataManager.cancelMDetectMetric(6)
                    } else {
                        DataManager.setMDetectMetric(6)
                    }
                }
            }
            CheckBox {
                text: "服务QPS"
                Layout.fillWidth: true

                onCheckedChanged: {
                    if (!checked) {
                        DataManager.cancelMDetectMetric(7)
                    } else {
                        DataManager.setMDetectMetric(7)
                    }
                }
            }
        }
    }
}