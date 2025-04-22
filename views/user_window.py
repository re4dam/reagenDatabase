# views/user_window.py
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTableView,
    QPushButton,
    QMessageBox,
    QHeaderView,
    QHBoxLayout,
    QFormLayout,
)
from PyQt6.QtCore import Qt, QAbstractTableModel
from typing import Optional, Dict, List


class UserTableModel(QAbstractTableModel):
    def __init__(self, data, headers, parent=None):
        super().__init__(parent)
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[index.row()][index.column()])

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        return (
            self._headers[section]
            if orientation == Qt.Orientation.Horizontal
            else str(section + 1)
        )


class UserWidget(QWidget):
    def __init__(self, user_model, parent=None):
        super().__init__(parent)
        self.user_model = user_model
        self.parent_window = parent  # Store reference to parent
        self.current_user_id = None

        self._setup_ui()
        self._load_users()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Form
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)

        self.username_entry = QLineEdit()
        form_layout.addRow(QLabel("Username:"), self.username_entry)

        self.email_entry = QLineEdit()
        form_layout.addRow(QLabel("Email:"), self.email_entry)

        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow(QLabel("Password:"), self.password_entry)

        # Buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)

        self.add_button = QPushButton("Add User")
        self.add_button.clicked.connect(self._add_user)
        button_layout.addWidget(self.add_button)

        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self._update_user)
        self.update_button.setEnabled(False)
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self._delete_user)
        self.delete_button.setEnabled(False)
        button_layout.addWidget(self.delete_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self._clear_form)
        button_layout.addWidget(self.clear_button)

        self.toggle_active_button = QPushButton("Deactivate")
        self.toggle_active_button.clicked.connect(self._toggle_active)
        self.toggle_active_button.setEnabled(False)
        button_layout.addWidget(self.toggle_active_button)

        self.back_button = QPushButton("Back to Home")
        self.back_button.clicked.connect(self._back_to_home)  # Return to home widget
        button_layout.addWidget(self.back_button)

        # Table
        self.users_table = QTableView()
        self.users_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.users_table.clicked.connect(self._on_user_selected)

        # Add widgets to main layout
        main_layout.addWidget(form_widget)
        main_layout.addWidget(button_widget)
        main_layout.addWidget(self.users_table)

    def _back_to_home(self):
        """Go back to home widget"""
        if hasattr(self.parent_window, "show_home"):
            self.parent_window.show_home()

    def _load_users(self):
        users = self.user_model.get_all_active()
        if users:
            headers = ["ID", "Username", "Email", "Password", "Status"]
            # Map is_active to "Active"/"Inactive"
            data = [
                [
                    user["id"],
                    user["username"],
                    user["email"],
                    user["password_hash"],
                    "Active" if user["is_active"] else "Inactive",
                ]
                for user in users
            ]
            model = UserTableModel(data, headers)
            self.users_table.setModel(model)
        else:
            self.users_table.setModel(None)

    def _on_user_selected(self, index):
        model = self.users_table.model()
        if not model:
            return

        row = index.row()
        self.current_user_id = int(model.index(row, 0).data())
        self.username_entry.setText(model.index(row, 1).data())
        self.email_entry.setText(model.index(row, 2).data())
        self.password_entry.clear()

        # Update button states
        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)
        self.toggle_active_button.setEnabled(True)
        self.add_button.setEnabled(False)

        # Update toggle button text based on status
        status = model.index(row, 4).data()  # Status is in column 4
        self.toggle_active_button.setText(
            "Deactivate" if status == "Active" else "Activate"
        )

    def _clear_form(self):
        self.username_entry.clear()
        self.email_entry.clear()
        self.password_entry.clear()
        self.current_user_id = None

        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.toggle_active_button.setEnabled(False)
        self.add_button.setEnabled(True)

    def _validate_fields(self, require_password=True):
        username = self.username_entry.text()
        email = self.email_entry.text()
        password = self.password_entry.text()

        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")
        if "@" not in email:
            raise ValueError("Invalid email format")
        if require_password and not password:
            raise ValueError("Password is required")

        return username, email, password

    def _add_user(self):
        try:
            username, email, password = self._validate_fields()

            # In a real app, you would hash the password first
            password_hash = f"hashed_{password}"  # Replace with actual hashing

            user_id = self.user_model.create(username, email, password_hash)
            if user_id:
                QMessageBox.information(self, "Success", "User created successfully!")
                self._clear_form()
                self._load_users()
            else:
                QMessageBox.critical(self, "Error", "Failed to create user!")

        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")

    def _update_user(self):
        if not self.current_user_id:
            return

        try:
            username, email, password = self._validate_fields(require_password=False)

            # Get existing user data
            user = self.user_model.get_by_id(self.current_user_id)
            if not user:
                raise ValueError("User not found")

            # Only update password if it was provided
            password_hash = user["password_hash"]
            if password:
                password_hash = f"hashed_{password}"  # Replace with actual hashing

            # Update email (username is likely not meant to be changed)
            success = self.user_model.update_email(self.current_user_id, email)

            if success:
                QMessageBox.information(self, "Success", "User updated successfully!")
                self._clear_form()
                self._load_users()
            else:
                QMessageBox.critical(self, "Error", "Failed to update user!")

        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")

    def _delete_user(self):
        if not self.current_user_id:
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Permanently delete this user?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.user_model.deactivate(self.current_user_id)
                if success:
                    QMessageBox.information(self, "Success", "User deactivated!")
                    self._clear_form()
                    self._load_users()
                else:
                    QMessageBox.critical(self, "Error", "Failed to deactivate user!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Database error: {str(e)}")

    def _toggle_active(self):
        if not self.current_user_id:
            return

        try:
            user = self.user_model.get_by_id(self.current_user_id)
            if not user:
                raise ValueError("User not found")

            new_status = not user["is_active"]
            success = (
                self.user_model.deactivate(self.current_user_id)
                if not new_status
                else True
            )

            if success:
                status_text = "deactivated" if not new_status else "activated"
                QMessageBox.information(
                    self, "Success", f"User {status_text} successfully!"
                )
                self._clear_form()
                self._load_users()
            else:
                QMessageBox.critical(self, "Error", "Failed to change user status!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")


# For backward compatibility
class UserManagementWindow(QMainWindow):
    def __init__(self, user_model, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Management System")
        self.setGeometry(100, 100, 800, 600)

        # Create the user widget as the central widget
        self.user_widget = UserWidget(user_model, self)
        self.setCentralWidget(self.user_widget)
