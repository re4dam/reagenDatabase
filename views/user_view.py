from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableView,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QHeaderView,
    QFormLayout,
)
from PyQt6.QtCore import Qt, pyqtSlot


class UserView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.user_viewmodel = None
        self.current_user_id = None

        self._setup_ui()

    def set_viewmodel(self, viewmodel):
        """Set the ViewModel for this view"""
        self.user_viewmodel = viewmodel

    def _setup_ui(self):
        """Initialize UI components"""
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
        self.back_button.clicked.connect(self._back_to_home)
        button_layout.addWidget(self.back_button)

        # Table
        self.users_table = QTableView()
        self.users_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.users_table.clicked.connect(self._on_user_selected)

        # Add to main layout
        main_layout.addWidget(form_widget)
        main_layout.addWidget(button_widget)
        main_layout.addWidget(self.users_table)

    @pyqtSlot(list)
    def on_users_loaded(self, users):
        """Handle loaded users data"""
        if users:
            headers = ["ID", "Username", "Email", "Status"]
            data = [
                [
                    u["id"],
                    u["username"],
                    u["email"],
                    "Active" if u["is_active"] else "Inactive",
                ]
                for u in users
            ]
            model = self._create_table_model(data, headers)
            self.users_table.setModel(model)
        else:
            self.users_table.setModel(None)

    def _create_table_model(self, data, headers):
        """Helper to create table model"""
        from PyQt6.QtCore import QAbstractTableModel

        class TableModel(QAbstractTableModel):
            def __init__(self, data, headers):
                super().__init__()
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

            def headerData(self, section, orientation, role):
                if role != Qt.ItemDataRole.DisplayRole:
                    return None
                return (
                    self._headers[section]
                    if orientation == Qt.Orientation.Horizontal
                    else str(section + 1)
                )

        return TableModel(data, headers)

    def _on_user_selected(self, index):
        """Handle table row selection"""
        model = self.users_table.model()
        if not model:
            return

        row = index.row()
        self.current_user_id = int(model.index(row, 0).data())
        self.username_entry.setText(model.index(row, 1).data())
        self.email_entry.setText(model.index(row, 2).data())
        self.password_entry.clear()

        status = model.index(row, 3).data()
        self.toggle_active_button.setText(
            "Deactivate" if status == "Active" else "Activate"
        )

        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)
        self.toggle_active_button.setEnabled(True)
        self.add_button.setEnabled(False)

    def _clear_form(self):
        """Clear the form"""
        self.username_entry.clear()
        self.email_entry.clear()
        self.password_entry.clear()
        self.current_user_id = None
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.toggle_active_button.setEnabled(False)
        self.add_button.setEnabled(True)

    def _add_user(self):
        """Handle add user request"""
        if self.user_viewmodel:
            username = self.username_entry.text().strip()
            email = self.email_entry.text().strip()
            password = self.password_entry.text().strip()
            self.user_viewmodel.add_user(username, email, password)

    def _update_user(self):
        """Handle update user request"""
        if self.user_viewmodel and self.current_user_id:
            email = self.email_entry.text().strip()
            password = self.password_entry.text().strip()
            self.user_viewmodel.update_user(self.current_user_id, email, password)

    def _delete_user(self):
        """Handle delete user request"""
        if self.user_viewmodel and self.current_user_id:
            self.user_viewmodel.delete_user(self.current_user_id)

    def _toggle_active(self):
        """Handle toggle active request"""
        if self.user_viewmodel and self.current_user_id:
            self.user_viewmodel.toggle_user_active(self.current_user_id)

    def _back_to_home(self):
        """Return to home view"""
        if self.parent_window:
            self.parent_window.show_home()

    @pyqtSlot(str)
    def on_user_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, "Error", message)

    @pyqtSlot(str)
    def on_user_success(self, message):
        """Show success message"""
        QMessageBox.information(self, "Success", message)
        self._clear_form()
        if self.user_viewmodel:
            self.user_viewmodel.load_users()
