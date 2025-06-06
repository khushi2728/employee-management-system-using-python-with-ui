from PyQt5 import QtWidgets, uic
import pymysql
from PyQt5.QtGui import QIcon


class ViewEmpWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("search_em.ui", self)
        self.setWindowTitle("Employee Management System")
        self.setWindowIcon(QIcon("logo.png"))

        self.tableWidget = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        self.txtName = self.findChild(QtWidgets.QLineEdit, "txtName")
        self.txtEmail = self.findChild(QtWidgets.QLineEdit, "txtEmail")
        self.txtMobileno = self.findChild(QtWidgets.QLineEdit, "txtMobileno")
        self.txtPost = self.findChild(QtWidgets.QLineEdit, "txtPost")
        self.btnSearch = self.findChild(QtWidgets.QPushButton, "btnSearch")

        self.btnSearch.clicked.connect(self.search_employee)
        self.load_data()

        self.btnToggleTable = self.findChild(QtWidgets.QPushButton, "btnToggleTable")

        if self.btnToggleTable:
            self.btnToggleTable.clicked.connect(self.toggle_table_visibility)
            self.tableWidget.setVisible(False)  # or False if you want to hide initially
            self.btnToggleTable.setText("Show Table")  # or "Show Table" if hidden initially



    def load_data(self):
        self.populate_table("SELECT name, email, phone, gender, dob, address, post, salary FROM employees")

    def search_employee(self):
        name = self.txtName.text().strip()
        email = self.txtEmail.text().strip()
        phone = self.txtMobileno.text().strip()
        post = self.txtPost.text().strip()

        query = "SELECT name, email, phone, gender, dob, address, post, salary FROM employees WHERE 1=1"
        params = []

        if name:
            query += " AND name LIKE %s"
            params.append(f"%{name}%")
        if email:
            query += " AND email LIKE %s"
            params.append(f"%{email}%")
        if phone:
            query += " AND phone LIKE %s"
            params.append(f"%{phone}%")
        if post:
            query += " AND post LIKE %s"
            params.append(f"%{post}%")

        self.populate_table(query, params)

    def populate_table(self, query, params=None):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Email", "Phone", "Gender", "DOB", "Address", "Post", "Salary"])

        try:
            conn = pymysql.connect(host="localhost", user="root", password="", db="employees12")
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            for row_idx, row in enumerate(cursor.fetchall()):
                self.tableWidget.insertRow(row_idx)
                for col_idx, item in enumerate(row):
                    self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(item)))

            conn.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

    def toggle_table_visibility(self):
        if self.tableWidget and self.btnToggleTable:
            is_visible = self.tableWidget.isVisible()
            self.tableWidget.setVisible(not is_visible)
            self.btnToggleTable.setText("Show Table" if not is_visible else "Hide Table")
