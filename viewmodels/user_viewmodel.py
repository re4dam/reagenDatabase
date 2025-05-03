from PyQt6.QtCore import QObject, pyqtSignal


class UserViewModel(QObject):
    users_loaded = pyqtSignal(list)
    user_error = pyqtSignal(str)
    user_success = pyqtSignal(str)

    def __init__(self, user_model):
        super().__init__()
        self.user_model = user_model
        self.user_view = None

    def create_user_view(self, parent_window):
        """Create and show the user view"""
        from views.user_view import UserView

        if not parent_window:
            return False

        if not hasattr(parent_window, "user_widget") or not parent_window.user_widget:
            parent_window.user_widget = UserView(parent_window)
            parent_window.stacked_widget.addWidget(parent_window.user_widget)
            self.user_view = parent_window.user_widget
            self.user_view.set_viewmodel(self)
            self.users_loaded.connect(self.user_view.on_users_loaded)
            self.user_error.connect(self.user_view.on_user_error)
            self.user_success.connect(self.user_view.on_user_success)

        parent_window.stacked_widget.setCurrentWidget(parent_window.user_widget)
        self.load_users()
        return True

    def load_users(self):
        """Load users from database"""
        try:
            users = self.user_model.get_all_active()
            self.users_loaded.emit(users if users else [])
        except Exception as e:
            self.user_error.emit(f"Error loading users: {str(e)}")

    def add_user(self, username, email, password):
        """Add a new user"""
        if not username or not email or not password:
            self.user_error.emit("Username, email and password are required")
            return
        if "@" not in email:
            self.user_error.emit("Invalid email format")
            return

        try:
            # In a real app, hash the password properly
            password_hash = f"hashed_{password}"
            user_id = self.user_model.create(username, email, password_hash)
            if user_id:
                self.user_success.emit("User created successfully!")
            else:
                self.user_error.emit("Failed to create user")
        except Exception as e:
            self.user_error.emit(f"Error creating user: {str(e)}")

    def update_user(self, user_id, email, password):
        """Update existing user"""
        if not email:
            self.user_error.emit("Email is required")
            return
        if "@" not in email:
            self.user_error.emit("Invalid email format")
            return

        try:
            # Only update password if provided
            password_hash = None
            if password:
                password_hash = f"hashed_{password}"

            success = self.user_model.update_email(user_id, email)
            if success:
                self.user_success.emit("User updated successfully!")
            else:
                self.user_error.emit("Failed to update user")
        except Exception as e:
            self.user_error.emit(f"Error updating user: {str(e)}")

    def delete_user(self, user_id):
        """Delete a user"""
        try:
            success = self.user_model.deactivate(user_id)
            if success:
                self.user_success.emit("User deactivated successfully!")
            else:
                self.user_error.emit("Failed to deactivate user")
        except Exception as e:
            self.user_error.emit(f"Error deactivating user: {str(e)}")

    def toggle_user_active(self, user_id):
        """Toggle user active status"""
        try:
            user = self.user_model.get_by_id(user_id)
            if not user:
                self.user_error.emit("User not found")
                return

            new_status = not user["is_active"]
            if new_status:
                success = True  # In a real app, you'd have an activate method
            else:
                success = self.user_model.deactivate(user_id)

            if success:
                status = "activated" if new_status else "deactivated"
                self.user_success.emit(f"User {status} successfully!")
                self.load_users()
            else:
                self.user_error.emit("Failed to change user status")
        except Exception as e:
            self.user_error.emit(f"Error changing user status: {str(e)}")
