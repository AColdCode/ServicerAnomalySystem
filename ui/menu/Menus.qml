import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: menus
    width: parent.width
    height: 100
    color: "#F9FAFB"

    property int currentIndex: 1
    property bool isAdmin: false

    ColumnLayout {
        spacing: 10
        anchors.fill: parent

        MyMenuItem {
            Layout.fillWidth: true
            text: "主控台"
            icon: "../../images/main_interface.svg"
            index: 1
            color: menus.currentIndex === index ? "#2474F5" : hovered ? "#2196F3" : "#F9FAFB"

            onClicked: {
                menus.currentIndex = index
            }
        }

        MyMenuItem {
            Layout.fillWidth: true
            text: "单指标异常检测"
            icon: "../../images/detect_s.svg"
            index: 2
            color: menus.currentIndex === index ? "#2474F5" : hovered ? "#2196F3" : "#F9FAFB"

            onClicked: {
                menus.currentIndex = index
            }
        }

        MyMenuItem {
            Layout.fillWidth: true
            text: "多指标异常检测"
            icon: "../../images/detect_m.svg"
            index: 3
            color: menus.currentIndex === index ? "#2474F5" : hovered ? "#2196F3" : "#F9FAFB"

            onClicked: {
                menus.currentIndex = index
            }
        }

        MyMenuItem {
            Layout.fillWidth: true
            text: "单指标态势预测"
            icon: "../../images/forecast_s.svg"
            index: 4
            color: menus.currentIndex === index ? "#2474F5" : hovered ? "#2196F3" : "#F9FAFB"

            onClicked: {
                menus.currentIndex = index
            }
        }

        MyMenuItem {
            Layout.fillWidth: true
            text: "多指标态势预测"
            icon: "../../images/forecast_m.svg"
            index: 5
            color: menus.currentIndex === index ? "#2474F5" : hovered ? "#2196F3" : "#F9FAFB"

            onClicked: {
                menus.currentIndex = index
            }
        }

        MyMenuItem {
            visible: menus.isAdmin
            Layout.fillWidth: true
            text: "数据管理"
            icon: "../../images/data.svg"
            index: 6
            color: menus.currentIndex === index ? "#2474F5" : hovered ? "#2196F3" : "#F9FAFB"

            onClicked: {
                menus.currentIndex = index
            }
        }

        MyMenuItem {
            visible: menus.isAdmin
            Layout.fillWidth: true
            text: "系统管理"
            icon: "../../images/user.svg"
            index: 7
            color: menus.currentIndex === index ? "#2474F5" : hovered ? "#2196F3" : "#F9FAFB"

            onClicked: {
                menus.currentIndex = index
            }
        }
    }

    Connections {
        target: DataManager

        function onLoginSuccess(username, role) {
            menus.isAdmin = role === "admin";
        }
    }
}