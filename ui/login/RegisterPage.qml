// 注册
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: registerPage
    width: 400
    height: 300
    color: "#F9FAFB"

    property bool nameTrue: false
    property bool passwordTrue: false

    ColumnLayout {
        spacing: 10
        anchors.fill: parent

        ColumnLayout {
            spacing: 10
            Layout.fillWidth: true

            Text {
                Layout.fillWidth: true
                text: "用户名"
            }

            TextField {
                id: usernameField
                placeholderText: "字母、数字或下划线"
                placeholderTextColor: registerPage.nameTrue ? "#409eff" : usernameField.activeFocus ? "red" : "#999"
                Layout.fillWidth: true
                Layout.preferredHeight: 60

                onTextChanged: {
                    registerPage.nameTrue = DataManager.isLegalUsername(usernameField.text)
                }

                onAccepted: {
                    passwordField.focus = true
                }

                background: Rectangle {
                    radius: 8
                    border.width: 1
                    border.color: registerPage.nameTrue ? "#409eff" : usernameField.activeFocus ? "red" : "grey"
                }
            }
        }

        ColumnLayout {
            spacing: 10
            Layout.fillWidth: true

            Text {
                text: "密码"
            }

            TextField {
                id: passwordField
                placeholderText: "至少六位"
                placeholderTextColor: registerPage.passwordTrue ? "#409eff" : passwordField.activeFocus ? "red" : "#999"
                echoMode: TextInput.Password
                Layout.fillWidth: true
                Layout.preferredHeight: 60

                onTextChanged: {
                    registerPage.passwordTrue = DataManager.isLegalPassword(passwordField.text)
                }

                onAccepted: {
                    registerBtn.click()
                }

                background: Rectangle {
                    radius: 8
                    border.width: 1
                    border.color: registerPage.passwordTrue ? "#409eff" : passwordField.activeFocus ? "red" : "grey"
                }
            }
        }


        Button {
            id: registerBtn
            text: "注册"
            Layout.fillWidth: true
            enabled: registerPage.nameTrue && registerPage.passwordTrue
            background: Rectangle {
                color: "#409EFF"
                radius: 12
            }

            onClicked: {
                let result = DataManager.register(usernameField.text, passwordField.text)

                if (result) {
                    usernameField.clear()
                    passwordField.clear()
                }
            }
        }

        Text {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter
            horizontalAlignment: Text.AlignHCenter
            font.pixelSize: 16
            color: "grey"
            text: "第一个注册的用户将自动成为管理员"
        }
    }
}