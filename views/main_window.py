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
)
from PyQt6.QtCore import Qt, QAbstractTableModel
from typing import Optional


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


class MainWindow(QMainWindow):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.setWindowTitle("Database Manager")
        self.setGeometry(100, 100, 100, 100)

        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        """Initialize UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Table view
        self.table_view = QTableView()
        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.table_view)

        # input columns
        self.name_label = QLabel("Name")
        self.name_entry = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_entry)

        self.description_label = QLabel("Description")
        self.description_entry = QLineEdit()
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_entry)

        # Buttons
        self.add_button = QPushButton("Add Record")
        self.add_button.clicked.connect(self._add_record)
        layout.addWidget(self.add_button)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self._load_data)
        layout.addWidget(self.refresh_button)

    def _load_data(self):
        """Load data from database and display in table"""
        records = self.db.get_records()
        if records:
            headers = list(records[0].keys())
            data = [list(record.values()) for record in records]
            model = RecordsTableModel(data, headers)
            self.table_view.setModel(model)
        else:
            self.table_view.setModel(None)

    def _add_record(self):
        """Example method to add a record"""
        # in real app you'd have a dialog for this
        # record_id = self.db.create_record("New Record", "This is a sample description")
        # if record_id:
        #     QMessageBox.information(self, "Success", "Record added succesfully!")
        #     self._load_data()
        # else:
        #     QMessageBox.critical(self, "Error", "Failed to add record!")

        """Trying in real case with knowledge from examples"""
        try:
            name = self.name_entry.text()
            description = self.description_entry.text()

            # Validate fields
            if name == "" or description == "":
                QMessageBox.warning(self, "Warning", "Please fill all fields!")
                return

            record_id = self.db.create_record(name, description)
            if record_id:
                QMessageBox.information(self, "Success", "Record added succesfully!")
                self._load_data()
            else:
                QMessageBox.critical(self, "Error", "Failed to add record!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
