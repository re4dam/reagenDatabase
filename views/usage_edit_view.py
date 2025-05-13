from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QDateEdit,
    QSpinBox,
    QFrame,
    QMessageBox,
    QComboBox,
)
from PyQt6.QtCore import Qt, pyqtSlot, QDate
from PyQt6.QtGui import QFont


class UsageEditView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.usage_edit_viewmodel = None

        self._setup_ui()

    def set_viewmodel(self, viewmodel):
        """Set the ViewModel for this view"""
        self.usage_edit_viewmodel = viewmodel

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Panel title
        self.title_label = QLabel()
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(divider)
        main_layout.addSpacing(10)

        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Date used field
        self.date_used_edit = QDateEdit()
        self.date_used_edit.setCalendarPopup(True)
        form_layout.addRow("Date Used:", self.date_used_edit)

        # Amount used field
        self.amount_used_spin = QSpinBox()
        self.amount_used_spin.setRange(1, 10000)
        form_layout.addRow("Amount Used:", self.amount_used_spin)

        # User field
        self.user_edit = QLineEdit()
        form_layout.addRow("User:", self.user_edit)

        # Supporting materials field (now a combo box)
        self.supporting_materials_combo = QComboBox()
        self.supporting_materials_combo.setEditable(True)
        self.supporting_materials_combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.supporting_materials_combo.setMinimumHeight(30)
        form_layout.addRow("Supporting Materials:", self.supporting_materials_combo)

        main_layout.addLayout(form_layout)

        # Current stock information
        self.current_stock_label = QLabel()
        self.current_stock_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(self.current_stock_label)

        # Warning label for stock
        self.stock_warning_label = QLabel()
        self.stock_warning_label.setStyleSheet("color: red; font-weight: bold;")
        self.stock_warning_label.setVisible(False)
        main_layout.addWidget(self.stock_warning_label)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.setMinimumHeight(40)
        self.save_button.setStyleSheet("QPushButton { background-color: #ccffcc; }")
        self.save_button.clicked.connect(self._save_usage)
        buttons_layout.addWidget(self.save_button)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMinimumHeight(40)
        self.cancel_button.setStyleSheet("QPushButton { background-color: #f0f0f0; }")
        self.cancel_button.clicked.connect(self._cancel)
        buttons_layout.addWidget(self.cancel_button)

        main_layout.addSpacing(20)
        main_layout.addLayout(buttons_layout)

    @pyqtSlot(dict, bool, int, list)
    def on_usage_loaded(self, usage_data, is_new, current_stock, supporting_materials):
        """Update UI with usage data"""
        self.title_label.setText(
            f"{'Add New' if is_new else 'Edit'} Usage Report for {usage_data.get('ReagentName', '')}"
        )

        if usage_data.get("Tanggal_Terpakai"):
            self.date_used_edit.setDate(
                QDate.fromString(usage_data["Tanggal_Terpakai"], "yyyy-MM-dd")
            )

        self.amount_used_spin.setValue(usage_data.get("Jumlah_Terpakai", 1))
        self.user_edit.setText(usage_data.get("User", ""))

        # Populate supporting materials dropdown
        self.supporting_materials_combo.clear()
        self.supporting_materials_combo.addItem("-- Select or type new --", None)
        for material in supporting_materials:
            self.supporting_materials_combo.addItem(material["name"], material["id"])

        # Set current value if exists
        current_material = usage_data.get("Bahan_Pendukung", "")
        if current_material:
            index = self.supporting_materials_combo.findText(current_material)
            if index >= 0:
                self.supporting_materials_combo.setCurrentIndex(index)
            else:
                self.supporting_materials_combo.setEditText(current_material)

        self.current_stock_label.setText(f"Current Stock: {current_stock}")
        self._check_stock_level()

    @pyqtSlot(str)
    def on_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, "Error", message)

    @pyqtSlot(str)
    def on_success(self, message):
        """Show success message"""
        QMessageBox.information(self, "Success", message)

    def _check_stock_level(self):
        """Check stock level"""
        if self.usage_edit_viewmodel:
            self.usage_edit_viewmodel.check_stock_level(self.amount_used_spin.value())

    def _save_usage(self):
        """Save usage data"""
        if self.usage_edit_viewmodel:
            # Get supporting material text (either selected or entered)
            supporting_material = self.supporting_materials_combo.currentText()
            if supporting_material == "-- Select or type new --":
                supporting_material = ""

            data = {
                "Tanggal_Terpakai": self.date_used_edit.date().toString("yyyy-MM-dd"),
                "Jumlah_Terpakai": self.amount_used_spin.value(),
                "User": self.user_edit.text(),
                "Bahan_Pendukung": supporting_material,
            }
            self.usage_edit_viewmodel.save_usage(data)

    def _cancel(self):
        """Cancel edit"""
        if self.usage_edit_viewmodel:
            self.usage_edit_viewmodel.cancel()

    @pyqtSlot(bool, str)
    def on_stock_warning(self, show_warning, message):
        """Show/hide stock warning"""
        self.stock_warning_label.setText(message)
        self.stock_warning_label.setVisible(show_warning)
