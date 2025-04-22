# views/login_window.py
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
from views.register_window import RegisterWindow
from views.home_window import HomeWindow


class LoginWindow(QMainWindow):
    def __init__(self, user_model=None):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 200)
        self.user_model = user_model or {}  # Use empty dict if no model provided
        self.record_model = None
        self.register_window = None
        self.home_window = None

        # Placeholder users for testing
        self.test_users = {
            "admin": {
                "username": "admin",
                "password_hash": "hashed_admin123",
                "email": "admin@example.com",
                "is_active": True,
            },
            "user1": {
                "username": "user1",
                "password_hash": "hashed_password123",
                "email": "user1@example.com",
                "is_active": True,
            },
            "inactive": {
                "username": "inactive",
                "password_hash": "hashed_test",
                "email": "inactive@example.com",
                "is_active": False,
            },
        }

        self._setup_ui()

    def setup_models(self, record_model, user_model=None):
        """Store the models for use when opening windows"""
        self.record_model = record_model
        if user_model:
            self.user_model = user_model

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self._login)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self._open_register)

        layout.addWidget(QLabel("Login to Reagent Management System"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(register_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Use placeholder authentication instead of database
        user = self.test_users.get(username)

        if not user or user["password_hash"] != f"hashed_{password}":
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
            return

        if not user["is_active"]:
            QMessageBox.warning(self, "Inactive", "User account is deactivated.")
            return

        # On success, open HomeWindow
        QMessageBox.information(self, "Success", f"Welcome, {username}!")

        try:
            self.home_window = HomeWindow()
            self.home_window.setup_models(self.record_model, self.user_model)
            self.home_window.show()
            self.close()
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Could not open home window: {str(e)}\n\nThis is expected if HomeWindow is not yet implemented.",
            )

    def _open_register(self):
        self.register_window = RegisterWindow(parent=self)
        self.register_window.show()
        self.hide()

    def add_user(self, username, email, password_hash):
        """Add a user to the test users dictionary"""
        if username in self.test_users:
            return False

        self.test_users[username] = {
            "username": username,
            "password_hash": password_hash,
            "email": email,
            "is_active": True,
        }
        return True
