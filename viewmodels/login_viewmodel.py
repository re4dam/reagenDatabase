# viewmodels/login_viewmodel.py
from PyQt6.QtCore import QObject, pyqtSignal


class LoginViewModel(QObject):
    """ViewModel for login functionality"""

    # Define signals for communication with view
    login_succeeded = pyqtSignal(int)  # Now passes the user ID
    login_failed = pyqtSignal(str)

    def __init__(self, user_model):
        super().__init__()
        self.user_model = user_model

    def authenticate(self, username, password):
        """Authenticate user with provided credentials"""
        try:
            user = self.user_model.get_by_username(username)

            if not user or user["password_hash"] != f"hashed_{password}":
                self.login_failed.emit("Invalid username or password.")
                return False

            if not user["is_active"]:
                self.login_failed.emit("User account is deactivated.")
                return False

            # Authentication successful, emit with user_id
            self.login_succeeded.emit(user["id"])
            return True

        except Exception as e:
            self.login_failed.emit(f"Database error: {str(e)}")
            return False
