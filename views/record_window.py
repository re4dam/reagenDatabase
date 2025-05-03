# views/record_window.py
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QWidget,
    QVBoxLayout,
    QTableView,
    QPushButton,
    QMessageBox,
    QHeaderView,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from typing import Optional, Tuple


class RecordsTableModel(QAbstractTableModel):
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
            row = index.row()
            col = index.column()
            return str(self._data[row][col])

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            return self._headers[section]

        return str(section + 1)


class RecordWidget(QWidget):
    def __init__(self, record_model, parent=None):
        super().__init__(parent)
        self.record_model = record_model
        self.parent_window = parent  # Store reference to parent
        self.current_selected_id = None  # To keep track of selected record for update

        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        """Initialize UI components"""
        main_layout = QVBoxLayout(self)

        # Form Layout
        form_widget = QWidget()
        form_layout = QVBoxLayout()
        form_widget.setLayout(form_layout)

        # Input fields
        self.name_label = QLabel("Name:")
        self.name_entry = QLineEdit()
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_entry)

        self.description_label = QLabel("Description:")
        self.description_entry = QLineEdit()
        form_layout.addWidget(self.description_label)
        form_layout.addWidget(self.description_entry)

        # Button Layout
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_widget.setLayout(button_layout)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self._add_record)
        button_layout.addWidget(self.add_button)

        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self._update_record)
        self.update_button.setEnabled(False)  # Disabled until a record is selected
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self._delete_record)
        self.delete_button.setEnabled(False)  # Disabled until a record is selected
        button_layout.addWidget(self.delete_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self._clear_form)
        button_layout.addWidget(self.clear_button)

        self.back_button = QPushButton("Back to Home")
        self.back_button.clicked.connect(self._back_to_home)  # Return to home widget
        button_layout.addWidget(self.back_button)

        # Table View
        self.table_view = QTableView()
        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table_view.clicked.connect(
            self._on_table_click
        )  # Connect selection signal

        # Add widgets to main layout
        main_layout.addWidget(form_widget)
        main_layout.addWidget(button_widget)
        main_layout.addWidget(self.table_view)

    def _back_to_home(self):
        """Go back to home widget"""
        if hasattr(self.parent_window, "show_home"):
            self.parent_window.show_home()

    def _load_data(self):
        """Load data from database and display in table"""
        records = self.record_model.get_all()
        if records:
            headers = ["ID", "Name", "Description"]
            data = [
                [record["id"], record["name"], record["description"]]
                for record in records
            ]
            model = RecordsTableModel(data, headers)
            self.table_view.setModel(model)
        else:
            self.table_view.setModel(None)

    def _on_table_click(self, index: QModelIndex):
        """Handle table row selection"""
        model = self.table_view.model()
        if not model:
            return

        row = index.row()
        self.current_record_id = int(
            model.index(row, 0).data()
        )  # Get ID from first column
        self.name_entry.setText(model.index(row, 1).data())
        self.description_entry.setText(model.index(row, 2).data())

        # Enable update and delete buttons
        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)
        self.add_button.setEnabled(False)

    def _clear_form(self):
        """Clear the form and reset buttons"""
        self.name_entry.clear()
        self.description_entry.clear()
        self.current_selected_id = None
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.add_button.setEnabled(True)

    def _validate_fields(self) -> Tuple[str, str]:
        """Validate input fields and return values"""
        name = self.name_entry.text().strip()
        description = self.description_entry.text().strip()

        if not name:
            raise ValueError("Name field is required")
        if not description:
            raise ValueError("Description field is required")

        return name, description

    def _add_record(self):
        """Add a new record to the database"""
        try:
            name, description = self._validate_fields()

            record_id = self.record_model.create_record(name, description)
            if record_id:
                QMessageBox.information(self, "Success", "Record added successfully!")
                self._clear_form()
                self._load_data()
            else:
                QMessageBox.critical(self, "Error", "Failed to add record!")

        except ValueError as e:
            QMessageBox.warning(self, "Warning", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def _update_record(self):
        """Update the selected record"""
        if not self.current_selected_id:
            return

        try:
            name, description = self._validate_fields()

            success = self.record_model.update_record(
                self.current_selected_id, name, description
            )
            if success:
                QMessageBox.information(self, "Success", "Record updated successfully!")
                self._clear_form()
                self._load_data()
            else:
                QMessageBox.critical(self, "Error", "Failed to update record!")

        except ValueError as e:
            QMessageBox.warning(self, "Warning", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def _delete_record(self):
        """Delete the selected record"""
        if not self.current_selected_id:
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this record?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.record_model.delete_record(self.current_selected_id)
                if success:
                    QMessageBox.information(
                        self, "Success", "Record deleted successfully!"
                    )
                    self._clear_form()
                    self._load_data()
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete record!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
