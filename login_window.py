
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

class LoginWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('StokWELL - Login/Register')
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #333;
                font-size: 14px;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin: 5px 0;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                margin: 5px 0;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Title
        title_label = QLabel('StokWELL')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50; margin-bottom: 20px;")
        main_layout.addWidget(title_label)

        subtitle_label = QLabel('Manage Your Stokvel')
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 14px; color: #666; margin-bottom: 30px;")
        main_layout.addWidget(subtitle_label)

        # Form container
        form_frame = QFrame()
        form_frame.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 20px; }")
        form_layout = QVBoxLayout(form_frame)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        form_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password_input)

        # Button layout
        button_layout = QHBoxLayout()
        
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)
        button_layout.addWidget(self.login_button)

        self.register_button = QPushButton('Register')
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        self.register_button.clicked.connect(self.register)
        button_layout.addWidget(self.register_button)

        form_layout.addLayout(button_layout)
        main_layout.addWidget(form_frame)

        self.setLayout(main_layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        success, message = self.controller.login_user(username, password)
        if success:
            QMessageBox.information(self, 'Login Success', message)
            self.controller.show_dashboard()
            self.close()
        else:
            QMessageBox.warning(self, 'Login Failed', message)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        success, message = self.controller.register_user(username, password)
        if success:
            QMessageBox.information(self, 'Registration Success', message)
        else:
            QMessageBox.warning(self, 'Registration Failed', message)


