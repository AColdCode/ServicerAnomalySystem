import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

Rectangle {
    id: userList

    radius: 10
    width: parent.width

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            Layout.topMargin: 10
            spacing: 10

            Text {
                Layout.leftMargin: 10
                text: "用户列表"
                font.pixelSize: 20
                color: "black"
            }

            Item {
                Layout.fillWidth: true
            }

            Rectangle {
                id: refreshBtn
                Layout.preferredWidth: 30
                Layout.preferredHeight: 30
                Layout.rightMargin: 10
                color: refresh_hover.hovered ? "#D4E0ED" : userList.color
                radius: 5

                Image {
                    anchors.fill: parent
                    fillMode: Image.PreserveAspectFit
                    source: RESOURCE_PATH + "images/refresh.svg"
                }

                HoverHandler {
                    id: refresh_hover
                    cursorShape: Qt.PointingHandCursor
                }

                TapHandler {
                    id: refresh_tap
                    onTapped: {
                        DataManager.refreshUsers()
                    }
                }

                // 阴影效果
                layer.enabled: true
                layer.effect: MultiEffect {
                    shadowEnabled: refresh_hover.hovered
                    shadowBlur: 0.8
                    shadowColor: "#80000000"
                    shadowVerticalOffset: 4
                }
            }
        }

        RowLayout {
            id: listTop
            Layout.fillWidth: true
            Layout.preferredHeight: 40

            property string topColor: "#6588BC"

            Text {
                Layout.leftMargin: 10
                Layout.preferredWidth: 130
                text: "用户名"
                font.pixelSize: userListview.textFont
                color: listTop.topColor
            }

            Text {
                Layout.leftMargin: 10
                Layout.preferredWidth: 80
                text: "角色"
                font.pixelSize: userListview.textFont
                color: listTop.topColor
            }

            Text {
                Layout.leftMargin: 10
                Layout.preferredWidth: 150
                text: "上级管理员"
                font.pixelSize: userListview.textFont
                color: listTop.topColor
            }

            Text {
                Layout.leftMargin: 10
                Layout.preferredWidth: 100
                text: "状态"
                font.pixelSize: userListview.textFont
                color: listTop.topColor
            }

            Text {
                Layout.leftMargin: 10
                Layout.preferredWidth: 150
                text: "创建时间"
                font.pixelSize: userListview.textFont
                color: listTop.topColor
            }

            Item {
                Layout.fillWidth: true
            }

            Text {
                Layout.rightMargin: 30
                text: "操作"
                font.pixelSize: userListview.textFont
                color: listTop.topColor
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 500
            Layout.leftMargin: 10
            Layout.rightMargin: 10

            color: userList.color
            radius: 5

            ListView {
                id: userListview
                flickDeceleration: 100000
                maximumFlickVelocity: 0
                boundsBehavior: Flickable.StopAtBounds
                anchors.fill: parent

                model: DataManager.userModel

                property int textFont: 15
                property real savedContentY: 0
                property string currentUser: ""

                clip: true

                ScrollBar.vertical: ScrollBar {
                    policy: ScrollBar.AsNeeded
                }

                delegate: Rectangle {
                    width: userListview.width
                    height: 40
                    color: row_hover.hovered ? "#F7F9FB" : "white"

                    property bool isCurrentUser: userListview.currentUser === nameText.m_name

                    RowLayout {
                        spacing: 20
                        anchors.fill: parent

                        Text {
                            id: nameText
                            Layout.leftMargin: 10
                            Layout.preferredWidth: 100
                            property string m_name: model.username
                            text: model.username
                            font.pixelSize: userListview.textFont
                            color: "black"
                        }

                        Rectangle {
                            id: roleRt
                            Layout.preferredWidth: 80
                            Layout.preferredHeight: 30
                            radius: 5
                            property string m_role: model.role

                            color: m_role === "admin" ? "#3C83F6" : "#E2EBF3"

                            Text {
                                anchors.centerIn: parent
                                text: roleRt.m_role === "admin" ? "管理员" : "普通用户"
                                font.pixelSize: userListview.textFont
                                color: roleRt.m_role === "admin" ? "white" : "black"
                            }
                        }

                        Text {
                            id: parentAdminText
                            Layout.leftMargin: 10
                            Layout.preferredWidth: 100
                            property string m_name: model.parent_admin
                            text: m_name
                            font.pixelSize: userListview.textFont
                            color: "black"
                        }

                        Item {
                            Layout.preferredWidth: 20
                        }

                        Rectangle {
                            id: activeRt
                            Layout.preferredWidth: 50
                            Layout.preferredHeight: 30
                            radius: 5
                            color: m_active === 1 ? "#E2EBF3" : "red"

                            property int m_active: model.is_active

                            Text {
                                anchors.centerIn: parent
                                text: activeRt.m_active === 1 ? "启用" : "禁用"
                                font.pixelSize: userListview.textFont
                                color: activeRt.m_active === 1 ? "black" : "white"
                            }
                        }

                        Item {
                            Layout.preferredWidth: 20
                        }

                        Text {
                            Layout.preferredWidth: 150
                            text: model.created_at
                            font.pixelSize: userListview.textFont
                            color: "black"
                        }

                        Item {
                            Layout.fillWidth: true
                        }

                        ComboBox {
                            id: roleCB
                            visible: !isCurrentUser
                            Layout.preferredWidth: 120
                            Layout.preferredHeight: 34

                            property bool ignore: true
                            model: ["管理员", "普通用户"]

                            currentIndex: roleRt.m_role === "admin" ? 0 : 1

                            onCurrentIndexChanged: {
                                if (ignore) {
                                    ignore = false
                                    return
                                }

                                let result = DataManager.changeUserRole(nameText.m_name, currentIndex === 0 ? "admin" : "user")
                                if (result) {
                                    roleRt.m_role = currentIndex === 0 ? "admin" : "user"
                                    userListview.savePosition()
                                    DataManager.refreshUsers()
                                } else {
                                    roleCB.currentIndex = currentIndex === 0 ? 1 : 0
                                    console.log("权限不足，修改用户角色失败")
                                    ignore = true
                                }
                            }
                        }

                        Rectangle {
                            id: enableBtn
                            visible: !isCurrentUser
                            Layout.preferredWidth: 30
                            Layout.preferredHeight: 30
                            color: enable_hover.hovered ? "#D4E0ED" : "#F9FAFB"
                            radius: 5

                            Image {
                                anchors.fill: parent
                                fillMode: Image.PreserveAspectFit
                                source: activeRt.m_active === 0 ? RESOURCE_PATH + "images/usable.svg" : RESOURCE_PATH + "images/disabled.svg"
                            }

                            HoverHandler {
                                id: enable_hover
                                cursorShape: Qt.PointingHandCursor
                            }

                            TapHandler {
                                id: enable_tap
                                onTapped: {
                                    confirmDialog.actionType = "toggleActive"
                                    confirmDialog.targetUser = nameText.m_name
                                    confirmDialog.newState = activeRt.m_active === 0 ? 1 : 0
                                    confirmDialog.open()
                                }
                            }
                        }

                        Rectangle {
                            id: deleteBtn
                            visible: !isCurrentUser
                            Layout.preferredWidth: 20
                            Layout.preferredHeight: 20
                            Layout.rightMargin: 20
                            color: del_hover.hovered ? "#D4E0ED" : "#F9FAFB"
                            radius: 5

                            Image {
                                anchors.fill: parent
                                fillMode: Image.PreserveAspectFit
                                source: RESOURCE_PATH + "images/delete.svg"
                            }

                            HoverHandler {
                                id: del_hover
                                cursorShape: Qt.PointingHandCursor
                            }

                            TapHandler {
                                id: del_tap
                                onTapped: {
                                    confirmDialog.actionType = "delete"
                                    confirmDialog.targetUser = nameText.m_name
                                    confirmDialog.open()
                                }
                            }
                        }

                        Rectangle {
                            visible: isCurrentUser
                            Layout.preferredWidth: 80
                            Layout.preferredHeight: 20
                            Layout.rightMargin: 50
                            radius: 5
                            border.color: "grey"
                            border.width: 1

                            Text {
                                anchors.centerIn: parent
                                color: "black"
                                text: "当前用户"
                                font.pixelSize: 12
                            }
                        }
                    }

                    HoverHandler {
                        id: row_hover
                    }

                    Rectangle {
                        anchors.bottom: parent.bottom
                        width: parent.width
                        height: 1
                        color: "grey"
                    }
                }

                Connections {
                    target: DataManager

                    function onUserModelChanged() {
                        userListview.restorePosition()
                    }
                }

                Connections {
                    target: DataManager

                    function onLoginSuccess(username, role) {
                        userListview.currentUser = username
                    }
                }

                function savePosition() {
                    savedContentY = contentY
                }

                function restorePosition() {
                    contentY = savedContentY
                }
            }

            Component.onCompleted: {
                DataManager.refreshUsers()
            }

            Dialog {
                id: confirmDialog
                anchors.centerIn: parent
                width: 320
                modal: true
                title: "确认操作"

                property string actionType: ""
                property string targetUser: ""
                property int newState: -1

                standardButtons: Dialog.Ok | Dialog.Cancel

                onAccepted: {
                    userListview.savePosition()

                    if (actionType === "delete") {
                        let result = DataManager.deleteUser(targetUser)
                        if (!result)
                            console.log("权限不足，删除用户失败")
                    }

                    else if (actionType === "toggleActive") {
                        let result = DataManager.changeUserActive(targetUser, newState)
                        if (!result)
                            console.log("权限不足，修改用户状态失败")
                    }

                    DataManager.refreshUsers()
                }

                contentItem: Column {
                    width: parent.width
                    spacing: 10

                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        text: {
                            if (confirmDialog.actionType === "delete")
                                return "确定要删除该用户吗？该操作不可恢复！"

                            if (confirmDialog.actionType === "toggleActive")
                                return confirmDialog.newState === 1
                                    ? "确定要启用该用户吗？"
                                    : "确定要禁用该用户吗？"

                            return ""
                        }

                        color: confirmDialog.actionType === "delete" ? "red" : "black"
                    }
                }
            }
        }
    }
}