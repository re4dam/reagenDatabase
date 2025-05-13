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
)
from PyQt6.QtCore import Qt, pyqtSlot


class RecordView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.record_viewmodel = None
        self.current_record_id = None

        self._setup_ui()

    def set_viewmodel(self, viewmodel):
        """Set the ViewModel for this view"""
        self.record_viewmodel = viewmodel

    def _setup_ui(self):
        """Initialize UI components"""
        main_layout = QVBoxLayout(self)

        # Form
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)

        # Input fields
        self.name_label = QLabel("Name:")
        self.name_entry = QLineEdit()
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_entry)

        self.description_label = QLabel("Description:")
        self.description_entry = QLineEdit()
        form_layout.addWidget(self.description_label)
        form_layout.addWidget(self.description_entry)

        # Buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self._add_record)
        button_layout.addWidget(self.add_button)

        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self._update_record)
        self.update_button.setEnabled(False)
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self._delete_record)
        self.delete_button.setEnabled(False)
        button_layout.addWidget(self.delete_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self._clear_form)
        button_layout.addWidget(self.clear_button)

        self.back_button = QPushButton("Back to Home")
        self.back_button.clicked.connect(self._back_to_home)
        button_layout.addWidget(self.back_button)

        # Table
        self.table_view = QTableView()
        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table_view.clicked.connect(self._on_table_click)

        # Add to main layout
        main_layout.addWidget(form_widget)
        main_layout.addWidget(button_widget)
        main_layout.addWidget(self.table_view)

    @pyqtSlot(list)
    def on_records_loaded(self, records):
        """Handle loaded records data"""
        if records:
            headers = ["ID", "Name", "Description"]
            data = [[r["id"], r["name"], r["description"]] for r in records]
            model = self._create_table_model(data, headers)
            self.table_view.setModel(model)
        else:
            self.table_view.setModel(None)

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

    def _on_table_click(self, index):
        """Handle table row selection"""
        model = self.table_view.model()
        if not model:
            return

        row = index.row()
        self.current_record_id = int(model.index(row, 0).data())
        self.name_entry.setText(model.index(row, 1).data())
        self.description_entry.setText(model.index(row, 2).data())

        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)
        self.add_button.setEnabled(False)

    def _clear_form(self):
        """Clear the form"""
        self.name_entry.clear()
        self.description_entry.clear()
        self.current_record_id = None
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.add_button.setEnabled(True)

    def _add_record(self):
        """Handle add record request"""
        if self.record_viewmodel:
            name = self.name_entry.text().strip()
            description = self.description_entry.text().strip()
            self.record_viewmodel.add_record(name, description)

    def _update_record(self):
        """Handle update record request"""
        if self.record_viewmodel and self.current_record_id:
            name = self.name_entry.text().strip()
            description = self.description_entry.text().strip()
            self.record_viewmodel.update_record(
                self.current_record_id, name, description
            )

    def _delete_record(self):
        """Handle delete record request"""
        if self.record_viewmodel and self.current_record_id:
            self.record_viewmodel.delete_record(self.current_record_id)

    def _back_to_home(self):
        """Return to home view"""
        if self.parent_window:
            self.parent_window.show_home()

    @pyqtSlot(str)
    def on_record_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, "Error", message)

    @pyqtSlot(str)
    def on_record_success(self, message):
        """Show success message"""
        QMessageBox.information(self, "Success", message)
        self._clear_form()
        if self.record_viewmodel:
            self.record_viewmodel.load_records()
