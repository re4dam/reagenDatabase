# viewmodels/register_viewmodel.py
from PyQt6.QtCore import QObject, pyqtSignal


class RegisterViewModel(QObject):
    """ViewModel for user registration functionality"""

    # Define signals for communication with view
    registration_succeeded = pyqtSignal()
    registration_failed = pyqtSignal(str)

    def __init__(self, user_model):
        super().__init__()
        self.user_model = user_model
        self.register_view = None

    def show_register_view(self, parent_window):
        """Create and show the register view"""
        from views.register_view import RegisterView

        if not parent_window:
            return False

        # Create the register view if it doesn't exist
        if (
            not hasattr(parent_window, "register_widget")
            or not parent_window.register_widget
        ):
            parent_window.register_widget = RegisterView(parent_window)
            parent_window.stacked_widget.addWidget(parent_window.register_widget)

            # Connect signals
            self.registration_succeeded.connect(
                parent_window.register_widget.on_registration_success
            )
            self.registration_failed.connect(
                parent_window.register_widget.on_registration_failed
            )

            # Set ViewModel reference
            parent_window.register_widget.set_viewmodel(self)

        # Switch to register widget
        parent_window.stacked_widget.setCurrentWidget(parent_window.register_widget)
        return True

    def register_user(self, username, first_name, last_name, password):
        """Register a new user with the provided information"""
        # Input validation
        if not username or not first_name or not last_name or not password:
            self.registration_failed.emit("All fields are required.")
            return False

        if len(password) < 6:
            self.registration_failed.emit(
                "Password must be at least 6 characters long."
            )
            return False

        # Hash password (in production, use a proper hashing algorithm)
        password_hash = f"hashed_{password}"

        try:
            # Check if username already exists
            existing_user = self.user_model.get_by_username(username)
            if existing_user:
                self.registration_failed.emit("Username already exists.")
                return False

            # Create the new user
            user_id = self.user_model.create(username, first_name, last_name, password_hash)
            if user_id:
                self.registration_succeeded.emit()
                return True
            else:
                self.registration_failed.emit("Registration failed. Please try again.")
                return False

        except Exception as e:
            self.registration_failed.emit(f"Database error: {str(e)}")
            return False