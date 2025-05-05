
import sqlite3
from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import sys
from PyQt5 import QtCore

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("mainui.ui", self)

        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.pushButton_1.clicked.connect(self.saveChanges)
        self.pushButton_2.clicked.connect(self.addNewTask)
        self.pushButton_3.clicked.connect(self.deleteTask)  # 🆕 Delete button

        self.calendarDateChanged()

    def calendarDateChanged(self):
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        self.updateTaskList(dateSelected)

    def updateTaskList(self, date):
        self.listWidget.clear()

        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        query = "SELECT task, completed FROM tasks WHERE date = ?"
        row = (date.isoformat(),)
        results = cursor.execute(query, row).fetchall()

        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if result[1] == "Yes":
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            self.listWidget.addItem(item)

        db.close()

    def saveChanges(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate().isoformat()

        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            task = item.text()

            if item.checkState() == QtCore.Qt.Checked:
                query = "UPDATE tasks SET completed = 'Yes' WHERE task = ? AND date = ?"
            else:
                query = "UPDATE tasks SET completed = 'No' WHERE task = ? AND date = ?"

            row = (task, date)
            cursor.execute(query, row)

        db.commit()
        db.close()

        messageBox = QMessageBox()
        messageBox.setText("Changes saved.")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()

    def addNewTask(self):
        try:
            db = sqlite3.connect("data.db")
            cursor = db.cursor()

            newTask = str(self.lineEdit.text())
            if not newTask:
                QMessageBox.warning(self, "Warning", "Task cannot be empty.")
                return

            date = self.calendarWidget.selectedDate().toPyDate().isoformat()
            query = "INSERT INTO tasks(task,completed,date) VALUES(?,?,?)"
            row = (newTask, "No", date)

            cursor.execute(query, row)
            db.commit()
            db.close()

            self.updateTaskList(self.calendarWidget.selectedDate().toPyDate())
            self.lineEdit.clear()

            msg = QMessageBox()
            msg.setText("Task added.")
            msg.exec()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")

    def deleteTask(self):
        selectedItems = self.listWidget.selectedItems()
        if not selectedItems:
            QMessageBox.warning(self, "Warning", "Please select a task to delete.")
            return
        print("hii")
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        print("jj")
        date = self.calendarWidget.selectedDate().toPyDate().isoformat()

        for item in selectedItems:
            task = item.text()
            query = "DELETE FROM tasks WHERE task = ? AND date = ?"
            print("hua delete")
            row = (task, date)
            cursor.execute(query, row)
            print("delete ")

        db.commit()
        db.close()
        print("kiya")

        self.updateTaskList(self.calendarWidget.selectedDate().toPyDate())
        print("kiya update")

        msg = QMessageBox()
        msg.setText("Task(s) deleted.")
        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

