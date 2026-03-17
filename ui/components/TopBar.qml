import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {

    color: "#333"

    RowLayout {

        anchors.fill: parent
        anchors.margins: 10

        spacing: 20

        Text {

            text: "Server Situation Monitoring System"

            font.pixelSize: 20

            color: "white"
        }

        Item {
            Layout.fillWidth: true
        }

        Text {

            id: timeText

            color: "lightgray"

            font.pixelSize: 16
        }

        Timer {

            interval: 1000
            running: true
            repeat: true

            onTriggered: {

                var d = new Date()

                timeText.text = d.toLocaleString()
            }
        }
    }
}