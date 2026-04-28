import QtQuick
import QtQuick.Controls

Popup {
    id: markedPopup
    width: 200
    height: 100
    modal: false
    focus: true
    closePolicy: Popup.NoAutoClose

    parent: Overlay.overlay

    x: (parent.width - width) / 2
    y: 30

    property alias text: markedText.text

    background: Rectangle {
        radius: 10
        color: "#333"
        opacity: 0.9
    }

    Text {
        id: markedText
        anchors.centerIn: parent
        color: "white"
    }

    Timer {
        interval: 1500
        running: markedPopup.visible
        repeat: false
        onTriggered: markedPopup.close()
    }
}