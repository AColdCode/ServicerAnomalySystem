import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "mainControl"

ScrollView {
    id: mainControl
    anchors.fill: parent

    property int index: -1

    contentItem: Flickable {
        id: mainInterface
        contentWidth: parent.width
        contentHeight: 1200

        ColumnLayout {
            anchors.fill: parent

            TopControl {
                Layout.fillWidth: true
                Layout.preferredHeight: 100
            }

            GlobalState {
                Layout.fillWidth: true
                Layout.preferredHeight: 120
                Layout.leftMargin: 20
                Layout.rightMargin: 20
            }

            VarsIndicators {
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

            Item {
                Layout.fillHeight: true
            }
        }
    }
}
