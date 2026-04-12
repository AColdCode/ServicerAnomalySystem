import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "multiDetect"

ScrollView {
    id: singleDetect
    anchors.fill: parent

    property int index: -1

    contentItem: Flickable {
        id: mainInterface
        contentWidth: parent.width
        contentHeight: 800

        ColumnLayout {
            anchors.fill: parent

            MultiTop {
                Layout.fillWidth: true
                Layout.preferredHeight: 100
            }

            SeletcMetric {
                id: selectMetric
                Layout.fillWidth: true
                Layout.preferredHeight: 100
                Layout.leftMargin: 20
                Layout.rightMargin: 20
            }

            MultiShow {
                id: singleShow
                Layout.fillWidth: true
                Layout.preferredHeight: 600
                Layout.leftMargin: 20
                Layout.rightMargin: 20
            }

            Item {
                Layout.fillHeight: true
            }
        }
    }
}
