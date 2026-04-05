import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "charts"
import "components"
import "login"
import "header"
import "menu"

// ApplicationWindow {
//
//     id: root
//
//     visible: true
//     width: 1600
//     height: 900
//
//     title: "Server Situation Monitoring System"
//
//     color: "#1e1e1e"
//
//     RowLayout {
//
//         anchors.fill: parent
//
//         // ===============================
//         // 左侧导航
//         // ===============================
//
//         SideBar{
//             id: sideBar
//             Layout.preferredWidth: 220
//             Layout.fillHeight: true
//         }
//
//
//         // ===============================
//         // 主区域
//         // ===============================
//
//         ColumnLayout {
//
//             Layout.fillWidth: true
//             Layout.fillHeight: true
//
//             // ===============================
//             // 顶部栏
//             // ===============================
//             TopBar {
//                 id: topBar
//                 Layout.fillWidth: true
//                 Layout.preferredHeight: 60
//             }
//
//             // ===============================
//             // 页面区域
//             // ===============================
//
//             StackLayout {
//
//                 id: pageStack
//
//                 Layout.fillWidth: true
//                 Layout.fillHeight: true
//
//                 currentIndex: sideBar.currentIndex
//
//                 SingleMetricChart{
//                     id: singleMetricChart
//                 }
//
//                 MultiMetricChart{
//                     id: multiMetricChart
//                 }
//
//                 SinglePredictChart {
//                     id: singlePredictChart
//                 }
//
//                 MultiPredictChart {
//                     id: multiPredictChart
//                 }
//             }
//         }
//     }
// }

ApplicationWindow {
    id: root

    visible: true

    width: isLogin ? 1920 : 600
    height: isLogin ? 1080 : 500
    minimumWidth: 600
    minimumHeight: 500

    property bool isLogin: false
    property string username: ""
    property string role: ""

    title: "Server Situation Monitoring System"

    color: "#F9FAFB"

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


    LogAndReg {
        id: log_reg
        visible: !isLogin
        anchors.fill: parent
    }

    Connections {
        target: DataManager

        function onLoginSuccess(username, role) {
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
        }
    }
}