# views/usage_edit_panel.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QDateEdit,
    QSpinBox,
    QFrame,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QDate


class UsageEditPanel(QWidget):
    def __init__(
        self,
        usage_model,
        identity_model,
        reagent_id,
        reagent_name,
        usage_id=None,
        parent=None,
    ):
        super().__init__(parent)
        self.usage_model = usage_model
        self.identity_model = identity_model
        self.reagent_id = reagent_id
        self.reagent_name = reagent_name
        self.usage_id = usage_id
        self.parent_widget = parent
        self.is_new = usage_id is None

        # Set up the UI for this panel
        self._setup_ui()

        # If editing existing usage, load its data
        if not self.is_new and self.usage_id:
            self._load_usage_data()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Panel title
        title_text = "Add New Usage Report" if self.is_new else "Edit Usage Report"
        title_label = QLabel(f"{title_text} for {self.reagent_name}")
        title_font = QLabel().font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Add a divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(divider)
        main_layout.addSpacing(10)

        # Form layout for usage details
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Date used field
        self.date_used_edit = QDateEdit()
        self.date_used_edit.setCalendarPopup(True)
        self.date_used_edit.setDate(QDate.currentDate())  # Default to today
        form_layout.addRow("Date Used:", self.date_used_edit)

        # Amount used field
        self.amount_used_spin = QSpinBox()
        self.amount_used_spin.setRange(1, 10000)
        self.amount_used_spin.setValue(1)  # Default value
        form_layout.addRow("Amount Used:", self.amount_used_spin)

        # User field
        self.user_edit = QLineEdit()
        form_layout.addRow("User:", self.user_edit)

        # Supporting materials field
        self.supporting_materials_edit = QTextEdit()
        self.supporting_materials_edit.setMaximumHeight(100)
        self.supporting_materials_edit.setPlaceholderText(
            "Enter any supporting materials or notes about this usage"
        )
        form_layout.addRow("Supporting Materials:", self.supporting_materials_edit)

        main_layout.addLayout(form_layout)

        # Current stock information
        self.current_stock_label = QLabel()
        self.current_stock_label.setStyleSheet("font-weight: bold;")
        self._update_stock_info()
        main_layout.addWidget(self.current_stock_label)

        # Warning label for stock
        self.stock_warning_label = QLabel()
        self.stock_warning_label.setStyleSheet("color: red; font-weight: bold;")
        self.stock_warning_label.setVisible(False)
        main_layout.addWidget(self.stock_warning_label)

        # Connect amount used spin box to update warning
        self.amount_used_spin.valueChanged.connect(self._check_stock_level)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.setMinimumHeight(40)
        self.save_button.setStyleSheet(
            "QPushButton { background-color: #ccffcc; border: 2px solid #66cc66; "
            "border-radius: 5px; font-weight: bold; }"
            "QPushButton:hover { background-color: #a3d9a3; }"
        )
        self.save_button.clicked.connect(self._save_usage)
        buttons_layout.addWidget(self.save_button)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMinimumHeight(40)
        self.cancel_button.setStyleSheet(
            "QPushButton { background-color: #f0f0f0; border: 2px solid #c0c0c0; "
            "border-radius: 5px; font-weight: bold; }"
            "QPushButton:hover { background-color: #e0e0e0; }"
        )
        self.cancel_button.clicked.connect(self._cancel)
        buttons_layout.addWidget(self.cancel_button)

        main_layout.addSpacing(20)
        main_layout.addLayout(buttons_layout)

    def _load_usage_data(self):
        """Load data for an existing usage report"""
        usage = self.usage_model.get_by_id(self.usage_id)

        if usage:
            # Set date used
            if usage.get("Tanggal_Terpakai"):
                self.date_used_edit.setDate(
                    QDate.fromString(usage["Tanggal_Terpakai"], "yyyy-MM-dd")
                )

            # Set amount used
            self.amount_used_spin.setValue(usage.get("Jumlah_Terpakai", 1))

            # Set user
            self.user_edit.setText(usage.get("User", ""))

            # Set supporting materials
            self.supporting_materials_edit.setText(usage.get("Bahan_Pendukung", ""))

            # Check stock level
            self._check_stock_level()

    def _update_stock_info(self):
        """Update the current stock information"""
        reagent = self.identity_model.get_by_id(self.reagent_id)

        if reagent:
            current_stock = reagent.get("Stock", 0)
            self.current_stock = current_stock  # Store for stock checking
            self.current_stock_label.setText(f"Current Stock: {current_stock}")

    def _check_stock_level(self):
        """Check if the amount used exceeds current stock"""
        if hasattr(self, "current_stock"):
            amount_used = self.amount_used_spin.value()

            # If editing, we need to account for the original amount
            original_amount = 0
            if not self.is_new:
                usage = self.usage_model.get_by_id(self.usage_id)
                if usage:
                    original_amount = usage.get("Jumlah_Terpakai", 0)

            # Only show warning if new amount exceeds stock (for new reports)
            # or if the increase in amount exceeds remaining stock (for edits)
            if (self.is_new and amount_used > self.current_stock) or (
                not self.is_new and (amount_used - original_amount) > self.current_stock
            ):
                self.stock_warning_label.setText(
                    "Warning: Amount exceeds current stock!"
                )
                self.stock_warning_label.setVisible(True)
            else:
                self.stock_warning_label.setVisible(False)

    def _save_usage(self):
        """Save the usage report data"""
        # Collect data from form fields
        usage_data = {
            "Tanggal_Terpakai": self.date_used_edit.date().toString("yyyy-MM-dd"),
            "Jumlah_Terpakai": self.amount_used_spin.value(),
            "User": self.user_edit.text(),
            "Bahan_Pendukung": self.supporting_materials_edit.toPlainText(),
            "id_identity": self.reagent_id,
        }

        # Validate required fields
        if not usage_data["User"]:
            QMessageBox.warning(self, "Validation Error", "Please enter a user name.")
            return

        # Check stock level
        reagent = self.identity_model.get_by_id(self.reagent_id)
        current_stock = reagent.get("Stock", 0) if reagent else 0

        amount_used = usage_data["Jumlah_Terpakai"]

        # For editing, get original amount
        original_amount = 0
        if not self.is_new:
            original_usage = self.usage_model.get_by_id(self.usage_id)
            if original_usage:
                original_amount = original_usage.get("Jumlah_Terpakai", 0)

        # Calculate net change in stock
        stock_change = amount_used if self.is_new else (amount_used - original_amount)

        # Warn if stock will go negative, but allow saving anyway
        if stock_change > current_stock:
            confirm = QMessageBox.question(
                self,
                "Stock Warning",
                f"Amount used ({stock_change}) exceeds current stock ({current_stock}). Continue anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if confirm == QMessageBox.StandardButton.No:
                return

        try:
            # Save usage report
            if self.is_new:
                # Create new usage report
                result = self.usage_model.create(
                    tanggal_terpakai=usage_data["Tanggal_Terpakai"],
                    jumlah_terpakai=usage_data["Jumlah_Terpakai"],
                    user=usage_data["User"],
                    bahan_pendukung=usage_data["Bahan_Pendukung"],
                    id_identity=usage_data["id_identity"],
                )
                success_message = "Usage report added successfully"
            else:
                # Update existing usage report
                result = self.usage_model.update(
                    self.usage_id,
                    Tanggal_Terpakai=usage_data["Tanggal_Terpakai"],
                    Jumlah_Terpakai=usage_data["Jumlah_Terpakai"],
                    User=usage_data["User"],
                    Bahan_Pendukung=usage_data["Bahan_Pendukung"],
                )
                success_message = "Usage report updated successfully"

            if result:
                # Update reagent stock
                new_stock = max(0, current_stock - stock_change)
                self.identity_model.update(self.reagent_id, Stock=new_stock)

                QMessageBox.information(self, "Success", success_message)

                # Return to usage report panel
                if self.parent_widget and hasattr(
                    self.parent_widget, "show_usage_reports"
                ):
                    self.parent_widget.show_usage_reports(
                        self.reagent_id, self.reagent_name
                    )
            else:
                QMessageBox.warning(self, "Error", "Failed to save usage report")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def _cancel(self):
        """Cancel and return to usage report panel"""
        if self.parent_widget and hasattr(self.parent_widget, "show_usage_reports"):
            self.parent_widget.show_usage_reports(self.reagent_id, self.reagent_name)
