# views/login_view.py
from PyQt6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)
from PyQt6.QtCore import pyqtSlot


class LoginView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reagent Management System")
        self.setGeometry(100, 100, 800, 600)

        # Will be set through setup method
        self.login_viewmodel = None
        self.home_viewmodel = None

        # Create a stacked widget to manage different views
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create the login widget
        self.login_widget = QWidget()
        self._setup_login_ui()

        # Add login widget to stacked widget
        self.stacked_widget.addWidget(self.login_widget)

        # Initialize other widgets as None
        self.register_widget = None
        self.home_widget = None

    def setup_viewmodels(
        self, login_viewmodel, register_viewmodel=None, home_viewmodel=None
    ):
        """Connect to the viewmodels"""
        self.login_viewmodel = login_viewmodel
        self.register_viewmodel = register_viewmodel
        self.home_viewmodel = home_viewmodel

        # Connect signals from viewmodels
        if self.login_viewmodel:
            self.login_viewmodel.login_succeeded.connect(self.on_login_success)
            self.login_viewmodel.login_failed.connect(self.on_login_failed)

    def _setup_login_ui(self):
        """Set up the UI components for the login page"""
        layout = QVBoxLayout(self.login_widget)

        title_label = QLabel("Login to Reagent Management System")
        layout.addWidget(title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self._login)
        layout.addWidget(login_button)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self._show_register)
        layout.addWidget(register_button)

        # Add some spacing before the exit button
        layout.addSpacing(20)

        # Add exit button at the bottom
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)

        # Use a horizontal layout to position the exit button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(exit_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

    def _login(self):
        """Handle login button click"""
        if not self.login_viewmodel:
            QMessageBox.critical(self, "Error", "ViewModel not initialized")
            return

        username = self.username_input.text()
        password = self.password_input.text()

        # Use the ViewModel to authenticate
        self.login_viewmodel.authenticate(username, password)

    @pyqtSlot()
    def on_login_success(self):
        """Handle successful login"""
        try:
            # Switch to home view
            if self.home_viewmodel and self.home_viewmodel.create_home_view(self):
                # Set window title and size appropriate for main application
                self.setWindowTitle("Sistem Manajemen Reagen")
                self.setGeometry(100, 100, 800, 600)
            else:
                QMessageBox.warning(self, "Error", "Could not open home view")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open home view: {str(e)}")

    @pyqtSlot(str)
    def on_login_failed(self, message):
        """Handle failed login"""
        QMessageBox.warning(self, "Login Failed", message)

    def _show_register(self):
        """Show the register widget"""
        if self.register_viewmodel:
            self.register_viewmodel.show_register_view(self)

    def show_login(self):
        """Switch back to the login widget"""
        # Reset window title and size for login view
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 250)

        # Clear sensitive data
        self.username_input.clear()
        self.password_input.clear()

        # Switch to login widget
        self.stacked_widget.setCurrentWidget(self.login_widget)
