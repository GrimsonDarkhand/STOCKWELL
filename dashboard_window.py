
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QListWidget, QFrame, QScrollArea, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class DashboardWindow(QWidget):
    def __init__(self, controller, current_user):
        super().__init__()
        self.controller = controller
        self.current_user = current_user
        self.init_ui()
        self.load_dashboard_data()

    def init_ui(self):
        self.setWindowTitle(f'StokWELL - Dashboard for {self.current_user}')
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
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
                padding: 15px;
                margin: 5px;
            }
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
                padding: 10px;
            }
        """)

        main_layout = QVBoxLayout()

        # Header
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        welcome_label = QLabel(f'Welcome, {self.current_user}!')
        welcome_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #4CAF50;")
        header_layout.addWidget(welcome_label)
        
        header_layout.addStretch()
        
        self.logout_button = QPushButton('Logout')
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.logout_button.clicked.connect(self.logout)
        header_layout.addWidget(self.logout_button)
        
        main_layout.addWidget(header_frame)

        # Content area
        content_layout = QHBoxLayout()

        # Left column - Balance and Actions
        left_column = QVBoxLayout()
        
        # Balance card
        balance_frame = QFrame()
        balance_layout = QVBoxLayout(balance_frame)
        balance_title = QLabel('Account Balance')
        balance_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        balance_layout.addWidget(balance_title)
        
        self.balance_label = QLabel('R0.00')
        self.balance_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50;")
        balance_layout.addWidget(self.balance_label)
        left_column.addWidget(balance_frame)

        # Action buttons
        actions_frame = QFrame()
        actions_layout = QVBoxLayout(actions_frame)
        actions_title = QLabel('Quick Actions')
        actions_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        actions_layout.addWidget(actions_title)

        self.create_stokvel_button = QPushButton('Create New Stokvel')
        self.create_stokvel_button.clicked.connect(self.create_stokvel)
        actions_layout.addWidget(self.create_stokvel_button)

        self.contribute_button = QPushButton('Contribute to Stokvel')
        self.contribute_button.clicked.connect(self.contribute)
        actions_layout.addWidget(self.contribute_button)

        left_column.addWidget(actions_frame)
        left_column.addStretch()

        # Right column - Transactions and Stokvels
        right_column = QVBoxLayout()

        # Transactions
        transactions_frame = QFrame()
        transactions_layout = QVBoxLayout(transactions_frame)
        transactions_title = QLabel('Recent Transactions')
        transactions_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        transactions_layout.addWidget(transactions_title)

        self.transactions_list = QListWidget()
        self.transactions_list.setMaximumHeight(200)
        transactions_layout.addWidget(self.transactions_list)
        right_column.addWidget(transactions_frame)

        # Stokvels
        stokvels_frame = QFrame()
        stokvels_layout = QVBoxLayout(stokvels_frame)
        stokvels_title = QLabel('Your Stokvels')
        stokvels_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        stokvels_layout.addWidget(stokvels_title)

        self.stokvels_list = QListWidget()
        stokvels_layout.addWidget(self.stokvels_list)
        right_column.addWidget(stokvels_frame)

        # Add columns to content layout
        content_layout.addLayout(left_column, 1)
        content_layout.addLayout(right_column, 2)
        
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def load_dashboard_data(self):
        data = self.controller.get_data()
        user_data = data['users'][self.current_user]

        self.balance_label.setText(f"Balance: R{user_data['balance']:.2f}")

        self.transactions_list.clear()
        self.transactions_list.addItem('--- Transactions ---')
        for tx in user_data['transactions']:
            self.transactions_list.addItem(tx)

        self.stokvels_list.clear()
        self.stokvels_list.addItem('--- Your Stokvels ---')
        for s_name in user_data['stokvels']:
            stokvel = data['stokvels'][s_name]
            self.stokvels_list.addItem(f"* {s_name} - Balance: R{stokvel['balance']:.2f} - Members: {', '.join(stokvel['members'])}")

    def create_stokvel(self):
        self.controller.show_create_stokvel_dialog()
        self.load_dashboard_data() # Refresh dashboard after creating stokvel

    def contribute(self):
        self.controller.show_contribute_dialog()
        self.load_dashboard_data() # Refresh dashboard after contributing

    def logout(self):
        self.controller.logout_user()
        self.close()


