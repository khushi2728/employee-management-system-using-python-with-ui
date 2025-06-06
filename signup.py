# signup.py
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon

from db_connection import get_connection

class SignupWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("signup.ui", self)
        self.setWindowTitle("Employee Management System")
        self.setWindowIcon(QIcon("logo.png"))

        self.signupButton = self.findChild(QtWidgets.QPushButton, "btnSignup")
        self.usernameInput = self.findChild(QtWidgets.QLineEdit, "txtUsername")
        self.passwordInput = self.findChild(QtWidgets.QLineEdit, "txtPassword")
        self.txtConfirmPassword = self.findChild(QtWidgets.QLineEdit, "txtConfirmPass")

        self.signupButton.clicked.connect(self.signup)
        self.gotoLoginButton = self.findChild(QtWidgets.QPushButton, "btnLogin")
        self.gotoLoginButton.clicked.connect(self.open_login)

    def open_login(self):
        from login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.exec_()


    def signup(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        conn = get_connection()
        print("con liya")
        cursor = conn.cursor()
        print("cursor bana")
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            QtWidgets.QMessageBox.warning(self, "Error", "User already exists.")
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            QtWidgets.QMessageBox.information(self, "Success", "Signup successful!")
            self.accept()
        conn.close()