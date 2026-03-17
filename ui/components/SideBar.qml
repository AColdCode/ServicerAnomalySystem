import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {

    id: root

    color: "#252526"

    property int currentIndex: 0

    ColumnLayout {

        anchors.fill: parent

        spacing: 10

        Rectangle {

            Layout.fillWidth: true
            height: 70
            color: "#333"

            Text {
                anchors.centerIn: parent
                text: "SERVER\nMONITOR"
                color: "white"
                horizontalAlignment: Text.AlignHCenter
            }
        }

        // ===============================
        // 按钮
        // ===============================

        Repeater {

            model: [
                "单指标异常检测",
                "多指标异常检测",
                "单指标预测",
                "多指标预测"
            ]

            delegate: Button {

                Layout.fillWidth: true
                height: 50

                text: modelData

                onClicked: {

                    root.currentIndex = index
                }
            }
        }

        Item {
            Layout.fillHeight: true
        }
    }
}
