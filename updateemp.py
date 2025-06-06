from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate
import pymysql
from PyQt5.QtGui import QIcon


class UpdateEmpWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("update_em.ui", self)
        self.setWindowTitle("Employee Management System")
        self.setWindowIcon(QIcon("logo.png"))

        # Widgets
        self.txtName = self.findChild(QtWidgets.QLineEdit, "txtName")
        self.txtEmail = self.findChild(QtWidgets.QLineEdit, "txtEmail")
        self.txtMobileno = self.findChild(QtWidgets.QLineEdit, "txtMobileno")
        self.txtCombobox = self.findChild(QtWidgets.QComboBox, "txtCombobox")
        self.txtDate = self.findChild(QtWidgets.QDateEdit, "txtDate")
        self.txtAddress = self.findChild(QtWidgets.QTextEdit, "txtAddress")
        self.txtPost = self.findChild(QtWidgets.QLineEdit, "txtPost")
        self.txtSalary = self.findChild(QtWidgets.QLineEdit, "txtSalary")
        self.btnUpdate = self.findChild(QtWidgets.QPushButton, "btnUpdate")
        self.tableWidget = self.findChild(QtWidgets.QTableWidget, "tableWidget")

        self.txtEmail.setReadOnly(True)
        self.txtDate.setCalendarPopup(True)
        self.txtDate.setDate(QDate.currentDate())

        self.load_data()
        self.btnUpdate.clicked.connect(self.update_employee)
        self.tableWidget.cellClicked.connect(self.load_row_data)

        self.btnToggleTable = self.findChild(QtWidgets.QPushButton, "btnToggleTable")

        if self.btnToggleTable:
            self.btnToggleTable.clicked.connect(self.toggle_table_visibility)
            self.tableWidget.setVisible(False)  # or False if you want to hide initially
            self.btnToggleTable.setText("Show Table")  # or "Show Table" if hidden initially

    def load_row_data(self, row, _):
        self.txtName.setText(self.tableWidget.item(row, 0).text())
        self.txtEmail.setText(self.tableWidget.item(row, 1).text())
        self.txtMobileno.setText(self.tableWidget.item(row, 2).text())
        self.txtCombobox.setCurrentText(self.tableWidget.item(row, 3).text())
        dob = self.tableWidget.item(row, 4).text()
        self.txtDate.setDate(QDate.fromString(dob, "yyyy-MM-dd"))
        self.txtAddress.setText(self.tableWidget.item(row, 5).text())
        self.txtPost.setText(self.tableWidget.item(row, 6).text())
        self.txtSalary.setText(self.tableWidget.item(row, 7).text())

    def update_employee(self):
        data = (
            self.txtName.text().strip(),
            self.txtMobileno.text().strip(),
            self.txtCombobox.currentText(),
            self.txtDate.date().toString("yyyy-MM-dd"),
            self.txtAddress.toPlainText().strip(),
            self.txtPost.text().strip(),
            self.txtSalary.text().strip(),
            self.txtEmail.text().strip()
        )

        if "" in data or data[2] == "Select Gender":
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return

        try:
            conn = pymysql.connect(host="localhost", user="root", password="", db="employees12")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE employees
                SET name=%s, phone=%s, gender=%s, dob=%s, address=%s, post=%s, salary=%s
                WHERE email=%s
            """, data)
            conn.commit()
            conn.close()
            QtWidgets.QMessageBox.information(self, "Success", "Employee updated successfully!")
            self.load_data()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

    def load_data(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Email", "Phone", "Gender", "DOB", "Address", "Post", "Salary"])

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

    def toggle_table_visibility(self):
        if self.tableWidget and self.btnToggleTable:
            is_visible = self.tableWidget.isVisible()
            self.tableWidget.setVisible(not is_visible)
            self.btnToggleTable.setText("Hide Table" if not is_visible else "Show Table")
