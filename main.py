import pymysql
from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtGui import QIcon
from hrwork import HrWindow
from setup_database import init_db
from setupdb import init_db1
from signup import SignupWindow
from login import LoginWindow
from addemp import AddEmpWindow
from to_do import ToDoWindow
from updateemp import UpdateEmpWindow
from deletemp import DeleteEmpWindow
from viewemp import ViewEmpWindow
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("MainWindow2ui.ui", self)
        self.setWindowTitle("Employee Management System")
        self.setWindowIcon(QIcon("logo.png"))


        self.btnDashboard = self.findChild(QtWidgets.QPushButton, "btnDashboard")
        self.btnManage = self.findChild(QtWidgets.QPushButton, "btnManageemp")
        self.btnAttendance = self.findChild(QtWidgets.QPushButton, "btnAttendance")
        self.btnSalary = self.findChild(QtWidgets.QPushButton, "btnSalary")
        self.stackedWidget = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")

        self.btnDashboard.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btnManage.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btnAttendance.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.btnSalary.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))

        self.frameAdd = self.findChild(QtWidgets.QFrame, "frameAdd")
        self.frameUpdate = self.findChild(QtWidgets.QFrame, "frameUpdate")
        self.frameDelete = self.findChild(QtWidgets.QFrame, "frameDelete")
        self.frameView = self.findChild(QtWidgets.QFrame, "frameView")
        self.frameHrWorks = self.findChild(QtWidgets.QFrame, "frameHrWorks")
        self.frameTodo = self.findChild(QtWidgets.QFrame, "frameTodo")

        # Connect clicks
        if self.frameAdd: self.frameAdd.mousePressEvent = self.open_add
        if self.frameUpdate: self.frameUpdate.mousePressEvent = self.open_update
        if self.frameDelete: self.frameDelete.mousePressEvent = self.open_delete
        if self.frameView: self.frameView.mousePressEvent = self.open_view
        if self.frameHrWorks: self.frameHrWorks.mousePressEvent = self.open_hr
        if self.frameTodo: self.frameTodo.mousePressEvent = self.open_todo

        # Search
        self.txtSearchName = self.findChild(QtWidgets.QLineEdit, "txtName")
        self.tableWidgetSearch = self.findChild(QtWidgets.QTableWidget, "tableWidget")

        #ToggleTable(Salary)
        self.btnShowTable = self.findChild(QtWidgets.QPushButton, "btnShowTable")
        if self.tableWidgetSearch:
            self.tableWidgetSearch.setVisible(False)  # Hide initially
        if self.btnShowTable:
            self.btnShowTable.clicked.connect(self.toggle_table_visibility)

        if self.txtSearchName:
            self.txtSearchName.textChanged.connect(self.search_employee_by_name)

        # Attendance Submit
        self.cmbEmployeeName = self.findChild(QtWidgets.QComboBox, "cmbEmployeeName")
        self.load_employee_names()  # call the function to load employee names into dropdown
        self.inDatetime = self.findChild(QtWidgets.QDateTimeEdit, "inDatetime")
        self.outDatetime = self.findChild(QtWidgets.QDateTimeEdit, "outDatetime")
        self.btnSubmit = self.findChild(QtWidgets.QPushButton, "btnSubmit")

        if self.btnSubmit:
            self.btnSubmit.clicked.connect(self.submit_attendance)

        # Labels for employee count and avg attendance
        self.showEmployee = self.findChild(QtWidgets.QLabel, "showEmployee")
        self.avgAttendance = self.findChild(QtWidgets.QLabel, "avgAttendance")

        self.update_employee_count()
        self.update_average_attendance()
        self.show_dashboard()

    def load_employee_names(self):
        try:
            conn = pymysql.connect(host="localhost", user="root", password="", db="employees12")
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM employees")
            employee_names = cursor.fetchall()
            self.cmbEmployeeName.clear()
            for name in employee_names:
                self.cmbEmployeeName.addItem(name[0])
            cursor.close()
            conn.close()
        except Exception as e:
            print("Error loading employee names:", e)


    def toggle_table_visibility(self):
        if self.tableWidgetSearch and self.btnShowTable:
            is_visible = self.tableWidgetSearch.isVisible()
            self.tableWidgetSearch.setVisible(not is_visible)
            self.btnShowTable.setText("Hide Table" if not is_visible else "Show Table")


    def show_dashboard(self):
        self.stackedWidget.setCurrentIndex(0)
        self.update_employee_count()
        self.update_average_attendance()

    def update_employee_count(self):
        try:
            conn = pymysql.connect(host="localhost", user="root", password="", db="employees12")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM employees")
            count = cursor.fetchone()[0]
            self.showEmployee.setText(str(count))
            cursor.close()
            conn.close()
        except Exception as e:
            self.showEmployee.setText("Error")
            print("Error fetching employee count:", e)

    def update_average_attendance(self):
        try:
            conn = pymysql.connect(host="127.0.0.1", user="root", password="", db="myapp")
            cursor = conn.cursor()
            # Distinct usernames present today in attendance table
            cursor.execute("SELECT COUNT(DISTINCT username) FROM attendance WHERE date = CURDATE()")
            attendance_count = cursor.fetchone()[0]
            self.avgAttendance.setText(str(attendance_count))
            cursor.close()
            conn.close()
        except Exception as e:
            self.avgAttendance.setText("Error")
            print("Error fetching average attendance:", e)


    def open_add(self, event):
        self.add_window = AddEmpWindow()
        self.add_window.show()

    def open_update(self, event):
        self.update_window = UpdateEmpWindow()
        self.update_window.show()

    def open_delete(self, event):
        self.delete_window = DeleteEmpWindow()
        self.delete_window.show()

    def open_view(self, event):
        self.view_window = ViewEmpWindow()
        self.view_window.show()

    def open_hr(self, event):
        print("HR Frame Clicked")
        try:
            self.hr_window = HrWindow()
            self.hr_window.show()
            print("HR Window loaded successfully")
        except Exception as e:
            print("Failed to load HR Window:", str(e))

    def open_todo(self, event):
        print("ToDo Frame Clicked")
        self.todo_window = ToDoWindow()
        self.todo_window.show()

    def search_employee_by_name(self):
        name = self.txtSearchName.text().strip()
        try:
            conn = pymysql.connect(host="localhost", user="root", password="", db="employees12")
            cursor = conn.cursor()
            query = "SELECT name, email, post, salary FROM employees WHERE name LIKE %s"
            cursor.execute(query, ('%' + name + '%',))
            results = cursor.fetchall()

            self.tableWidgetSearch.setRowCount(0)
            self.tableWidgetSearch.setColumnCount(4)
            self.tableWidgetSearch.setHorizontalHeaderLabels(["Name", "Email", "Post", "Salary"])

            for row_num, row_data in enumerate(results):
                self.tableWidgetSearch.insertRow(row_num)
                for col_num, data in enumerate(row_data):
                    self.tableWidgetSearch.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(data)))

            cursor.close()
            conn.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

    def submit_attendance(self):
        employee_name = self.cmbEmployeeName.currentText().strip()
        in_time = self.inDatetime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        out_time = self.outDatetime.dateTime().toString("yyyy-MM-dd HH:mm:ss")

        if not employee_name:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select an employee name.")
            return

        try:
            conn = pymysql.connect(host="localhost", user="root", password="", db="employees12")
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    employee_name VARCHAR(100),
                    in_time DATETIME,
                    out_time DATETIME,
                    date DATE
                )
            """)

            cursor.execute(
                "INSERT INTO attendance (employee_name, in_time, out_time, date) VALUES (%s, %s, %s, CURDATE())",
                (employee_name, in_time, out_time)
            )

            conn.commit()
            cursor.close()
            conn.close()

            QtWidgets.QMessageBox.information(self, "Success", "Attendance submitted successfully.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))



class WelcomeWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("window.ui", self)
        self.setWindowTitle("Employee Management System")
        self.setWindowIcon(QIcon("logo.png"))
        self.loginButton = self.findChild(QtWidgets.QPushButton, "btnLogin")
        self.signupButton = self.findChild(QtWidgets.QPushButton, "btnSignup")
        self.loginButton.clicked.connect(self.open_login)
        self.signupButton.clicked.connect(self.open_signup)

    def open_login(self):
        login = LoginWindow()
        if login.exec_() == QtWidgets.QDialog.Accepted:
            self.accept()

    def open_signup(self):
        signup = SignupWindow()
        signup.exec_()


if __name__ == "__main__":
    init_db()
    init_db1()
    app = QtWidgets.QApplication(sys.argv)
    Welcome = WelcomeWindow()
    if Welcome.exec_() == QtWidgets.QDialog.Accepted:
        main = MainWindow()
        main.show()
    sys.exit(app.exec_())