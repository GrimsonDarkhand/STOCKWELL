
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel, QFrame
from PyQt5.QtCore import Qt

class CreateStokvelDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Create New Stokvel")
        self.setFixedSize(350, 200)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
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
                padding: 12px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)

        main_layout = QVBoxLayout()
        
        # Content frame
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)

        title_label = QLabel("Create New Stokvel")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #4CAF50; margin-bottom: 15px;")
        title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title_label)

        self.stokvel_name_input = QLineEdit()
        self.stokvel_name_input.setPlaceholderText("Enter Stokvel Name")
        content_layout.addWidget(self.stokvel_name_input)

        # Button layout
        button_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #757575;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.create_stokvel)
        button_layout.addWidget(self.create_button)

        content_layout.addLayout(button_layout)
        main_layout.addWidget(content_frame)
        self.setLayout(main_layout)

    def create_stokvel(self):
        stokvel_name = self.stokvel_name_input.text()
        if not stokvel_name:
            QMessageBox.warning(self, "Input Error", "Stokvel name cannot be empty.")
            return

        success, message = self.controller.create_stokvel(stokvel_name)
        if success:
            QMessageBox.information(self, "Success", message)
            self.accept() # Close dialog
        else:
            QMessageBox.warning(self, "Error", message)


