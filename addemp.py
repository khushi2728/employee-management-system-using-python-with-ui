from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate
import pymysql
import sys

from PyQt5.QtGui import QIcon


class AddEmpWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("add_em.ui", self)
        self.setWindowTitle("Employee Management System")
        self.setWindowIcon(QIcon("logo.png"))

        # Finding UI elements
        self.txtName = self.findChild(QtWidgets.QLineEdit, "txtName")
        self.txtEmail = self.findChild(QtWidgets.QLineEdit, "txtEmail")
        self.txtMobileno = self.findChild(QtWidgets.QLineEdit, "txtMobileno")
        self.txtCombobox = self.findChild(QtWidgets.QComboBox, "txtCombobox")
        self.txtDate = self.findChild(QtWidgets.QDateEdit, "txtDate")
        self.txtAddress = self.findChild(QtWidgets.QTextEdit, "txtAddress")
        self.txtPost = self.findChild(QtWidgets.QLineEdit, "txtPost")
        self.txtSalary = self.findChild(QtWidgets.QLineEdit, "txtSalary")
        self.btnAdd = self.findChild(QtWidgets.QPushButton, "btnAdd")
        self.tableWidget = self.findChild(QtWidgets.QTableWidget, "tableWidget")


        # Setup
        self.txtDate.setCalendarPopup(True)
        self.txtDate.setDate(QDate.currentDate())
        self.txtCombobox.setCurrentIndex(0)

        self.btnAdd.clicked.connect(self.add_employee)

        self.load_data()

        self.btnToggleTable = self.findChild(QtWidgets.QPushButton, "btnToggleTable")

        if self.btnToggleTable:
            self.btnToggleTable.clicked.connect(self.toggle_table_visibility)
            self.tableWidget.setVisible(False)  # or False if you want to hide initially
            self.btnToggleTable.setText("Show Table")  # or "Show Table" if hidden initially


    def add_employee(self):
        data = (
            self.txtName.text().strip(),
            self.txtEmail.text().strip(),
            self.txtMobileno.text().strip(),
            self.txtCombobox.currentText(),
            self.txtDate.date().toString("yyyy-MM-dd"),
            self.txtAddress.toPlainText().strip(),
            self.txtPost.text().strip(),
            self.txtSalary.text().strip()
        )

        if "" in data or data[3] == "Select Gender":
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return

        try:
            conn = pymysql.connect(host="localhost", user="root", password="", db="employees12")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO employees (name, email, phone, gender, dob, address, post, salary)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, data)
            conn.commit()
            conn.close()
            QtWidgets.QMessageBox.information(self, "Success", "Employee added successfully!")
            self.clear_inputs()
            self.load_data()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

    def load_data(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Name", "Email", "Phone", "Gender", "DOB", "Address", "Post", "Salary"]
        )

        try:
            conn = pymysql.connect(host="localhost", user="root", password="", db="employees12")
            cursor = conn.cursor()
            cursor.execute("SELECT name, email, phone, gender, dob, address, post, salary FROM employees")
            for row_idx, row in enumerate(cursor.fetchall()):
                self.tableWidget.insertRow(row_idx)
                for col_idx, item in enumerate(row):
                    self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(item)))
            conn.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Load Error", str(e))

    def clear_inputs(self):
        self.txtName.clear()
        self.txtEmail.clear()
        self.txtMobileno.clear()
        self.txtCombobox.setCurrentIndex(0)
        self.txtDate.setDate(QDate.currentDate())
        self.txtAddress.clear()
        self.txtPost.clear()
        self.txtSalary.clear()

    def toggle_table_visibility(self):
        if self.tableWidget and self.btnToggleTable:
            is_visible = self.tableWidget.isVisible()
            self.tableWidget.setVisible(not is_visible)
            self.btnToggleTable.setText("Show Table" if not is_visible else "Hide Table")
