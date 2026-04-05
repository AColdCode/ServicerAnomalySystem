import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    anchors.fill: parent
    id: login_register

    property bool loginShow: true

    ColumnLayout  {
        anchors.centerIn: parent
        spacing: 10

        Text {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter
            horizontalAlignment: Text.AlignHCenter
            font.pixelSize: 24
            text: "态势预测与异常检测系统"
        }

        Text {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter
            horizontalAlignment: Text.AlignHCenter
            font.pixelSize: 16
            color: "grey"
            text: "智能运维平台"
        }

        RowLayout {
            spacing: 10
            Layout.fillWidth: true

            Button {
                text: "登录"
                Layout.fillWidth: true
                onClicked: {
                    login_register.loginShow = true
                }
            }

            Button {
                text: "注册"
                Layout.fillWidth: true
                onClicked: {
                    login_register.loginShow = false
                }
            }
        }

        LoginPage {
            visible: login_register.loginShow
            Layout.fillWidth: true
        }

        RegisterPage {
            visible: !login_register.loginShow
            Layout.fillWidth: true
        }
    }
}