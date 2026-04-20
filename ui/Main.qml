import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "charts"
import "components"
import "login"
import "header"
import "menu"
import "modules"


ApplicationWindow {
    id: root

    visible: true

    width: isLogin ? Screen.width : 600
    height: isLogin ? Screen.height : 500
    minimumWidth: 600
    minimumHeight: 500

    property bool isLogin: false
    property string username: ""
    property string role: ""
    property string m_color: "#F9FAFB"

    title: "Server Situation Monitoring System"

    color: m_color

    header: Top {
        id: top
        visible: isLogin
        height: 50

        onMenu_openedChanged: {
            drawer.open()
        }
    }

    // 左侧弹出菜单
    LeftDrawer {
        id: drawer
        width: 300
        height: parent.height
    }

    // 主区域
    MainControl {
        id: mainControl
        visible: isLogin && drawer.currentMenu === index
        anchors.fill: parent
        index: 1
    }

    SingleDetect {
        id: singleDetect
        visible: isLogin && drawer.currentMenu === index
        anchors.fill: parent
        index: 2
    }

    MultiDetect {
        id: multiDetext
        visible: isLogin && drawer.currentMenu === index
        anchors.fill: parent
        index: 3
    }

    SinglePredict {
        id: singlePredict
        visible: isLogin && drawer.currentMenu === index
        anchors.fill: parent
        index: 4
    }

    DataManage {
        id: dataManage
        visible: isLogin && drawer.currentMenu === index
        anchors.fill: parent
        index: 6
    }

    SystemManage {
        id: systemManage
        visible: isLogin && drawer.currentMenu === index
        anchors.fill: parent
        index: 7
    }

    // 登录注册页面
    LogAndReg {
        id: log_reg
        visible: !isLogin
        anchors.fill: parent
    }

    Connections {
        target: DataManager

        function onLoginSuccess(username, role) {
            if (role === "admin") {
                DataManager.refreshUsers()
            }
            root.isLogin = true
            root.username = username
            root.role = role
            root.x = -5
            root.y = 25
        }
    }

    Connections {
        target: DataManager

        function onLogoutSignal() {
            root.isLogin = false
            root.username = ""
            root.role = ""
            root.x = 432
            root.y = 162
            drawer.currentMenu = 1
        }
    }
}