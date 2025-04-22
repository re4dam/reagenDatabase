# views/register_window.py
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
)


class RegisterWidget(QWidget):
    def __init__(self, user_model, parent=None):
        super().__init__(parent)
        self.user_model = user_model
        self.parent_window = parent  # Store reference to parent

        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)

        title_label = QLabel("Register New User")
        main_layout.addWidget(title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        main_layout.addWidget(self.username_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        main_layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        main_layout.addWidget(self.password_input)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self._register)
        main_layout.addWidget(register_button)

        back_button = QPushButton("Back to Login")
        back_button.clicked.connect(self._back_to_login)
        main_layout.addWidget(back_button)

    def _register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not username or not email or not password:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        # Perform simple validation
        if "@" not in email or "." not in email:
            QMessageBox.warning(
                self, "Input Error", "Please enter a valid email address."
            )
            return

        if len(password) < 6:
            QMessageBox.warning(
                self, "Input Error", "Password must be at least 6 characters long."
            )
            return

        password_hash = (
            f"hashed_{password}"  # In production, use a proper hashing algorithm
        )

        try:
            # Check if username already exists
            existing_user = self.user_model.get_by_username(username)
            if existing_user:
                QMessageBox.warning(
                    self, "Registration Error", "Username already exists."
                )
                return

            # Use UserModel to create the new user
            user_id = self.user_model.create(username, email, password_hash)
            if user_id:
                QMessageBox.information(
                    self, "Success", "Registration complete. You can now log in."
                )
                self._back_to_login()
            else:
                QMessageBox.critical(
                    self, "Error", "Registration failed. Please try again."
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Error creating user: {str(e)}\n\nMake sure database connection is configured properly.",
            )

    def _back_to_login(self):
        """Return to login window"""
        if hasattr(self.parent_window, "show_login"):
            self.parent_window.show_login()


# For backward compatibility
class RegisterWindow(QMainWindow):
    def __init__(self, user_model, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register")
        self.setGeometry(100, 100, 400, 250)

        # Create the register widget as the central widget
        self.register_widget = RegisterWidget(user_model, self)
        self.setCentralWidget(self.register_widget)
