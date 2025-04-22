# views/register_window.py
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)


class RegisterWindow(QMainWindow):
    def __init__(self, user_model=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register")
        self.setGeometry(100, 100, 400, 250)
        self.user_model = user_model
        self._setup_ui()

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self._register)

        back_button = QPushButton("Back to Login")
        back_button.clicked.connect(self._go_back)

        layout.addWidget(QLabel("Register New User"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(register_button)
        layout.addWidget(back_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not username or not email or not password:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        password_hash = f"hashed_{password}"

        # Since we don't have a database, we'll use the parent's add_user method
        parent = self.parent()
        if parent and hasattr(parent, "add_user"):
            success = parent.add_user(username, email, password_hash)
            if success:
                QMessageBox.information(
                    self, "Success", "Registration complete. You can now log in."
                )
                self._go_back()
            else:
                QMessageBox.critical(self, "Error", "Username already exists.")
        else:
            # If parent doesn't have add_user, show success anyway for testing
            QMessageBox.information(
                self, "Success", "Registration complete (placeholder mode)."
            )
            self._go_back()

    def _go_back(self):
        """Return to login window"""
        parent = self.parent()
        if parent:
            parent.show()
        self.close()
