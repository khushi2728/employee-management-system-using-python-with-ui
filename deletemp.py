from PyQt5 import QtWidgets, uic
import pymysql
from PyQt5.QtGui import QIcon


class DeleteEmpWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("delete_em.ui", self)
        self.setWindowTitle("Employee Management System")
        self.setWindowIcon(QIcon("logo.png"))

        self.tableWidget = self.findChild(QtWidgets.QTableWidget, "tableWidget_2")
        self.btnDelete = self.findChild(QtWidgets.QPushButton, "btnDelete")

        self.btnDelete.clicked.connect(self.delete_employee)
        self.tableWidget.cellClicked.connect(self.select_row)

        self.selected_email = None
        self.load_data()

        self.btnToggleTable = self.findChild(QtWidgets.QPushButton, "btnToggleTable")

        if self.btnToggleTable:
            self.btnToggleTable.clicked.connect(self.toggle_table_visibility)
            self.tableWidget.setVisible(False)  # or False if you want it hidden initially
            self.btnToggleTable.setText("Show Table")  # or "Show Table" if hidden initially



    def select_row(self, row, _):
        self.selected_email = self.tableWidget.item(row, 1).text()  # email is column 1

    def delete_employee(self):
        if not self.selected_email:
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select a record first.")
            return

        confirm = QtWidgets.QMessageBox.question(self, "Confirm", "Are you sure to delete this employee?")
        if confirm != QtWidgets.QMessageBox.Yes:
            return

        try:
            conn = pymysql.connect(host="localhost", user="root", password="", db="employees12")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees WHERE email=%s", (self.selected_email,))
            conn.commit()
            conn.close()
            QtWidgets.QMessageBox.information(self, "Success", "Employee deleted.")
            self.selected_email = None
            self.load_data()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Delete Error", str(e))

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
            self.btnToggleTable.setText("Show Table" if not is_visible else "Hide Table")



