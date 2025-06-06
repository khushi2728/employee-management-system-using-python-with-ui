# login.py
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon

from db_connection import get_connection

class LoginWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("loginui.ui", self)
        self.setWindowTitle("Employee Management System")
        self.setWindowIcon(QIcon("logo.png"))

        self.loginButton = self.findChild(QtWidgets.QPushButton, "btnLogin")
        self.usernameInput = self.findChild(QtWidgets.QLineEdit, "txtUsername")
        self.passwordInput = self.findChild(QtWidgets.QLineEdit, "txtPassword")
        self.loginButton.clicked.connect(self.login)
        self.gotoSignupButton = self.findChild(QtWidgets.QPushButton, "btnSignup")
        self.gotoSignupButton.clicked.connect(self.open_signup)

    def open_signup(self):
        from signup import SignupWindow
        self.signup_window = SignupWindow()
        self.signup_window.exec_()


    def login(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        if cursor.fetchone():
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Failed", "Invalid Credentials")
        conn.close()