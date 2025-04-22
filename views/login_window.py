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
    def __init__(self, user_model):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 200)
        self.user_model = user_model
        self.record_model = None  # Will be set through setup_models
        self.register_window = None
        self.home_window = None
        self._setup_ui()

    def setup_models(self, record_model, user_model):
        """Store the models for use when opening windows"""
        self.record_model = record_model
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

        # Use UserModel to authenticate
        try:
            user = self.user_model.get_by_username(username)

            if not user or user["password_hash"] != f"hashed_{password}":
                QMessageBox.warning(
                    self, "Login Failed", "Invalid username or password."
                )
                return

            if not user["is_active"]:
                QMessageBox.warning(self, "Inactive", "User account is deactivated.")
                return

            # On success, open HomeWindow with both models
            try:
                self.home_window = HomeWindow()
                self.home_window.setup_models(self.record_model, self.user_model)

                # Pass reference to login window for logout functionality
                self.home_window.set_login_window(self)

                self.home_window.show()
                self.hide()  # Hide instead of close to allow returning
            except Exception as e:
                QMessageBox.warning(
                    self, "Error", f"Could not open home window: {str(e)}"
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Error connecting to database: {str(e)}\n\nEnsure database connection is properly configured.",
            )

    def _open_register(self):
        self.register_window = RegisterWindow(self.user_model, parent=self)
        self.register_window.show()
        self.hide()
