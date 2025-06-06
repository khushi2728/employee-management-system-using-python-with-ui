import sqlite3

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import sys
from PyQt5 import QtCore

class ToDoWindow(QWidget):
    def __init__(self):
        super(ToDoWindow, self).__init__()
        loadUi("to-dosave.ui", self)
        self.setWindowTitle("Employee Management System")
        self.setWindowIcon(QIcon("logo.png"))

        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.btnSaveChanges.clicked.connect(self.saveChanges)


        self.calendarDateChanged()

    def calendarDateChanged(self):
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        self.updateTaskList(dateSelected)

    def updateTaskList(self, date):
        self.listWidget.clear()

        db = sqlite3.connect("base.db")
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
        db = sqlite3.connect("base.db")
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