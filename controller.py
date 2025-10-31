
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from ui.login_window import LoginWindow
from ui.dashboard_window import DashboardWindow
from ui.create_stokvel_dialog import CreateStokvelDialog
from ui.contribute_dialog import ContributeDialog
from data_manager import load_data, save_data
from user_manager import register_user, login_user
from stokvel_manager import create_stokvel, contribute

class Controller:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = QMainWindow()
        self.stacked_widget = QStackedWidget()
        self.main_window.setCentralWidget(self.stacked_widget)

        self.data = load_data()
        self.current_user = None

        self.login_window = LoginWindow(self)
        self.stacked_widget.addWidget(self.login_window)

        self.dashboard_window = None # Will be initialized after successful login

    def run(self):
        self.main_window.show()
        sys.exit(self.app.exec_())

    def get_data(self):
        return self.data

    def register_user(self, username, password):
        success, message = register_user(self.data, username, password)
        return success, message

    def login_user(self, username, password):
        success, message = login_user(self.data, username, password)
        if success:
            self.current_user = username
        return success, message

    def logout_user(self):
        self.current_user = None
        self.stacked_widget.setCurrentWidget(self.login_window)

    def show_dashboard(self):
        if self.current_user:
            self.dashboard_window = DashboardWindow(self, self.current_user)
            self.stacked_widget.addWidget(self.dashboard_window)
            self.stacked_widget.setCurrentWidget(self.dashboard_window)

    def create_stokvel(self, stokvel_name):
        success, message = create_stokvel(self.data, stokvel_name, self.current_user)
        return success, message

    def contribute(self, stokvel_name, amount):
        success, message = contribute(self.data, stokvel_name, amount, self.current_user)
        return success, message

    def show_create_stokvel_dialog(self):
        dialog = CreateStokvelDialog(self)
        dialog.exec_()

    def show_contribute_dialog(self):
        dialog = ContributeDialog(self)
        dialog.exec_()

if __name__ == '__main__':
    controller = Controller()
    controller.run()


