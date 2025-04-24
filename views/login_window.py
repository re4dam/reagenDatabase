# views/login_window.py
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
from models import identity_model
from views.register_window import RegisterWidget
from views.home_window import (
    HomeWidget,
)  # Import the new HomeWidget instead of HomeWindow


class LoginWindow(QMainWindow):
    def __init__(self, user_model):
        super().__init__()
        self.setWindowTitle("Reagent Management System")
        self.setGeometry(
            100, 100, 800, 600
        )  # Larger window to accommodate the home view
        self.user_model = user_model
        self.record_model = None  # Will be set through setup_models
        self.storage_model = None  # Added storage model

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

    def setup_models(
        self, record_model, user_model, storage_model=None, identity_model=None
    ):
        """Store the models for use when opening widgets"""
        self.record_model = record_model
        self.user_model = user_model
        self.storage_model = storage_model  # Store the storage model
        self.identity_model = identity_model

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

            # On success, show HomeWidget
            try:
                # Create the home widget if it doesn't exist yet
                if not self.home_widget:
                    # Check if storage_model is available
                    if not self.storage_model:
                        QMessageBox.warning(
                            self,
                            "Missing Model",
                            "Storage model is not initialized. Some features may not work properly.",
                        )

                    self.home_widget = HomeWidget(
                        record_model=self.record_model,
                        user_model=self.user_model,
                        storage_model=self.storage_model,  # Pass the storage model
                        identity_model=self.identity_model,
                        parent=self,
                    )
                    self.stacked_widget.addWidget(self.home_widget)

                # Switch to home widget
                self.stacked_widget.setCurrentWidget(self.home_widget)

                # Set window title and size appropriate for main application
                self.setWindowTitle("Sistem Manajemen Reagen")
                self.setGeometry(100, 100, 800, 600)

            except Exception as e:
                QMessageBox.warning(
                    self, "Error", f"Could not open home view: {str(e)}"
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Error connecting to database: {str(e)}\n\nEnsure database connection is properly configured.",
            )

    def _show_register(self):
        """Show the register widget"""
        if not self.register_widget:
            self.register_widget = RegisterWidget(self.user_model, self)
            self.stacked_widget.addWidget(self.register_widget)

        # Switch to register widget
        self.stacked_widget.setCurrentWidget(self.register_widget)

    def show_login(self):
        """Switch back to the login widget"""
        # Reset window title and size for login view
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 250)

        # Switch to login widget
        self.stacked_widget.setCurrentWidget(self.login_widget)
