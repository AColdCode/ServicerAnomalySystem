// 登录
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: loginPage
    width: 400
    height: 300
    color: "#F9FAFB"

    property bool nameTrue: false
    property bool passwordTrue: false

    ColumnLayout{
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
                placeholderText: "请输入用户名"
                placeholderTextColor: loginPage.nameTrue ? "#409eff" : usernameField.activeFocus ? "red" : "#999"
                Layout.fillWidth: true
                Layout.preferredHeight: 60

                onTextChanged: {
                    loginPage.nameTrue = DataManager.isLegalUsername(usernameField.text)
                }

                onAccepted: {
                    passwordField.focus = true
                }

                background: Rectangle {
                    radius: 8
                    border.width: 1
                    border.color: loginPage.nameTrue ? "#409eff" : usernameField.activeFocus ? "red" : "grey"
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
                placeholderText: "请输入密码"
                placeholderTextColor: loginPage.passwordTrue ? "#409eff" : passwordField.activeFocus ? "red" : "#999"
                echoMode: TextInput.Password
                Layout.fillWidth: true
                Layout.preferredHeight: 60

                onTextChanged: {
                    loginPage.passwordTrue = DataManager.isLegalPassword(passwordField.text)
                }

                onAccepted: {
                    loginBtn.click()
                }

                background: Rectangle {
                    radius: 8
                    border.width: 1
                    border.color: loginPage.passwordTrue ? "#409eff" : passwordField.activeFocus ? "red" : "grey"
                }
            }
        }


        Button {
            id: loginBtn
            text: "登录"
            Layout.fillWidth: true
            enabled: loginPage.nameTrue && loginPage.passwordTrue
            background: Rectangle {
                color: "#409EFF"
                radius: 12
            }

            onClicked: {
                let role = DataManager.login(usernameField.text, passwordField.text)

                if (role) {
                    usernameField.clear()
                    passwordField.clear()
                }
            }
        }
    }
}