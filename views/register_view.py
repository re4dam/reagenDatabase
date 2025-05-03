# views/register_view.py
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtCore import pyqtSlot


class RegisterView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent  # Store reference to parent
        self.register_viewmodel = None

        self._setup_ui()

    def set_viewmodel(self, viewmodel):
        """Set the ViewModel for this view"""
        self.register_viewmodel = viewmodel

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
        """Handle register button click"""
        if not self.register_viewmodel:
            QMessageBox.critical(self, "Error", "ViewModel not initialized")
            return

        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        # Use the ViewModel to register the user
        self.register_viewmodel.register_user(username, email, password)

    @pyqtSlot()
    def on_registration_success(self):
        """Handle successful registration"""
        QMessageBox.information(
            self, "Success", "Registration complete. You can now log in."
        )
        self._back_to_login()

    @pyqtSlot(str)
    def on_registration_failed(self, message):
        """Handle failed registration"""
        QMessageBox.warning(self, "Registration Error", message)

    def _back_to_login(self):
        """Return to login window"""
        if hasattr(self.parent_window, "show_login"):
            self.parent_window.show_login()
