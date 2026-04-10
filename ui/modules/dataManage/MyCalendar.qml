import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: dateTimeDialog
    modal: true
    title: "选择时间"
    standardButtons: Dialog.Ok | Dialog.Cancel
    width: 360
    height: 420

    property date selectedDate: new Date()
    property date currentMonth: new Date()
    property var targetTextField: null

    contentItem: ColumnLayout {
        spacing: 10

        // ===== 月份控制 =====
        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: 50
            Layout.fillWidth: true

            Item {
                Layout.fillWidth: true
            }

            Button {
                Layout.preferredWidth: 50
                Layout.preferredHeight: 50
                text: "<"
                onClicked: {
                    dateTimeDialog.currentMonth = new Date(
                        dateTimeDialog.currentMonth.getFullYear(),
                        dateTimeDialog.currentMonth.getMonth() - 1,
                        1
                    )
                }
            }

            Item {
                Layout.fillWidth: true
            }

            Text {
                text: Qt.formatDate(dateTimeDialog.currentMonth, "yyyy年 MM月")
                font.pixelSize: 16
            }

            Item {
                Layout.fillWidth: true
            }

            Button {
                Layout.preferredWidth: 50
                Layout.preferredHeight: 50
                text: ">"
                onClicked: {
                    dateTimeDialog.currentMonth = new Date(
                        dateTimeDialog.currentMonth.getFullYear(),
                        dateTimeDialog.currentMonth.getMonth() + 1,
                        1
                    )
                }
            }

            Item {
                Layout.fillWidth: true
            }
        }

        // ===== 日历 =====
        MonthGrid {
            id: calendar
            Layout.fillWidth: true
            Layout.fillHeight: true

            month: dateTimeDialog.currentMonth.getMonth()
            year: dateTimeDialog.currentMonth.getFullYear()

            delegate: Rectangle {
                width: 40
                height: 40
                radius: 20

                property bool isSelected:
                    model.date.getFullYear() === dateTimeDialog.selectedDate.getFullYear() &&
                    model.date.getMonth() === dateTimeDialog.selectedDate.getMonth() &&
                    model.date.getDate() === dateTimeDialog.selectedDate.getDate()

                color: isSelected ? "#409EFF" : "transparent"

                Text {
                    anchors.centerIn: parent
                    text: model.day
                    color: isSelected ? "white" : "black"
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        dateTimeDialog.selectedDate = model.date
                    }
                }
            }
        }

        // ===== 时间选择 =====
        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: 10

            SpinBox {
                id: hourSpin
                from: 0
                to: 23
            }

            Text { text: ":" }

            SpinBox {
                id: minuteSpin
                from: 0
                to: 59
            }
        }
    }

    // ===== 确认 =====
    onAccepted: {
        if (targetTextField) {
            var d = dateTimeDialog.selectedDate

            var finalDate = new Date(
                d.getFullYear(),
                d.getMonth(),
                d.getDate(),
                hourSpin.value,
                minuteSpin.value
            )

            targetTextField.text =
                Qt.formatDateTime(finalDate, "yyyy/MM/dd HH:mm")
        }
    }

    // ===== 打开时回显 =====
    onOpened: {
        if (targetTextField && targetTextField.text !== "") {

            var parts = targetTextField.text.split(" ")
            if (parts.length === 2) {
                var datePart = parts[0].split("/")
                var timePart = parts[1].split(":")

                if (datePart.length === 3 && timePart.length === 2) {
                    var d = new Date(
                        parseInt(datePart[0]),
                        parseInt(datePart[1]) - 1,
                        parseInt(datePart[2]),
                        parseInt(timePart[0]),
                        parseInt(timePart[1])
                    )

                    dateTimeDialog.selectedDate = d
                    dateTimeDialog.currentMonth = d
                    hourSpin.value = d.getHours()
                    minuteSpin.value = d.getMinutes()
                }
            }
        }
    }
}