# views/reagent_panel.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QLabel,
    QPushButton,
    QDateEdit,
    QSpinBox,
    QComboBox,
    QMessageBox,
    QFrame,
)
from PyQt6.QtCore import Qt, QDate


class ReagentDetailPanel(QWidget):
    def __init__(self, identity_model, reagent_id=None, rack_name=None, parent=None):
        super().__init__(parent)
        self.identity_model = identity_model
        self.reagent_id = reagent_id
        self.rack_name = rack_name
        self.parent_widget = parent
        self.is_new = reagent_id is None

        # Set up the UI for this panel
        self._setup_ui()

        # If editing existing reagent, load its data
        if not self.is_new and self.reagent_id:
            self._load_reagent_data()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Panel title
        title_text = "Add New Reagent" if self.is_new else "Edit Reagent Details"
        title_label = QLabel(title_text)
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

        # Form layout for reagent details
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Name field
        self.name_edit = QLineEdit()
        form_layout.addRow("Name:", self.name_edit)

        # Description field
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        form_layout.addRow("Description:", self.description_edit)

        # Wujud (form/state) field
        self.wujud_combo = QComboBox()
        self.wujud_combo.addItems(["Solid", "Liquid", "Gas", "Solution"])
        form_layout.addRow("Form:", self.wujud_combo)

        # Stock field
        self.stock_spin = QSpinBox()
        self.stock_spin.setRange(0, 10000)
        form_layout.addRow("Stock:", self.stock_spin)

        # Massa field
        self.massa_spin = QSpinBox()
        self.massa_spin.setRange(0, 100000)
        form_layout.addRow("Mass (g):", self.massa_spin)

        # Tanggal_Expire field
        self.expire_date_edit = QDateEdit()
        self.expire_date_edit.setCalendarPopup(True)
        self.expire_date_edit.setDate(
            QDate.currentDate().addYears(1)
        )  # Default 1 year from now
        form_layout.addRow("Expiry Date:", self.expire_date_edit)

        # Category_Hazard field
        self.hazard_combo = QComboBox()
        self.hazard_combo.addItems(["None", "Low", "Medium", "High", "Extreme"])
        form_layout.addRow("Hazard Category:", self.hazard_combo)

        # Sifat field
        self.sifat_edit = QTextEdit()
        self.sifat_edit.setMaximumHeight(100)
        form_layout.addRow("Properties:", self.sifat_edit)

        # Tanggal_Produksi field
        self.prod_date_edit = QDateEdit()
        self.prod_date_edit.setCalendarPopup(True)
        self.prod_date_edit.setDate(QDate.currentDate())  # Default today
        form_layout.addRow("Production Date:", self.prod_date_edit)

        # Tanggal_Pembelian field
        self.purchase_date_edit = QDateEdit()
        self.purchase_date_edit.setCalendarPopup(True)
        self.purchase_date_edit.setDate(QDate.currentDate())  # Default today
        form_layout.addRow("Purchase Date:", self.purchase_date_edit)

        # SDS field
        self.sds_edit = QLineEdit()
        form_layout.addRow("SDS Reference:", self.sds_edit)

        # Storage ID field - will be set based on the rack_name
        self.storage_id_label = QLabel(f"Storage: {self.rack_name}")
        form_layout.addRow("Storage Location:", self.storage_id_label)

        main_layout.addLayout(form_layout)

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
        self.save_button.clicked.connect(self._save_reagent)
        buttons_layout.addWidget(self.save_button)

        # Delete button (only for existing reagents)
        if not self.is_new:
            self.delete_button = QPushButton("Delete")
            self.delete_button.setMinimumHeight(40)
            self.delete_button.setStyleSheet(
                "QPushButton { background-color: #ffcccc; border: 2px solid #ff6666; "
                "border-radius: 5px; font-weight: bold; }"
                "QPushButton:hover { background-color: #ffaaaa; }"
            )
            self.delete_button.clicked.connect(self._delete_reagent)
            buttons_layout.addWidget(self.delete_button)

        # Back button
        self.back_button = QPushButton("Back to Rack View")
        self.back_button.setMinimumHeight(40)
        self.back_button.clicked.connect(self._go_back)
        buttons_layout.addWidget(self.back_button)

        main_layout.addSpacing(20)
        main_layout.addLayout(buttons_layout)

    def _load_reagent_data(self):
        """Load data for an existing reagent"""
        # In a real implementation, fetch from database using self.identity_model
        reagent = self.identity_model.get_by_id(self.reagent_id)

        if reagent:
            self.name_edit.setText(reagent.get("Name", ""))
            self.description_edit.setText(reagent.get("Description", ""))

            # Set combobox value
            wujud_index = self.wujud_combo.findText(reagent.get("Wujud", ""))
            if wujud_index >= 0:
                self.wujud_combo.setCurrentIndex(wujud_index)

            self.stock_spin.setValue(reagent.get("Stock", 0))
            self.massa_spin.setValue(reagent.get("Massa", 0))

            # Set date values if available
            if reagent.get("Tanggal_Expire"):
                self.expire_date_edit.setDate(
                    QDate.fromString(reagent["Tanggal_Expire"], "yyyy-MM-dd")
                )

            hazard_index = self.hazard_combo.findText(
                reagent.get("Category_Hazard", "")
            )
            if hazard_index >= 0:
                self.hazard_combo.setCurrentIndex(hazard_index)

            self.sifat_edit.setText(reagent.get("Sifat", ""))

            if reagent.get("Tanggal_Produksi"):
                self.prod_date_edit.setDate(
                    QDate.fromString(reagent["Tanggal_Produksi"], "yyyy-MM-dd")
                )

            if reagent.get("Tanggal_Pembelian"):
                self.purchase_date_edit.setDate(
                    QDate.fromString(reagent["Tanggal_Pembelian"], "yyyy-MM-dd")
                )

            self.sds_edit.setText(reagent.get("SDS", ""))

    def _save_reagent(self):
        """Save the reagent data"""
        # Collect data from form fields
        reagent_data = {
            "Name": self.name_edit.text(),
            "Description": self.description_edit.toPlainText(),
            "Wujud": self.wujud_combo.currentText(),
            "Stock": self.stock_spin.value(),
            "Massa": self.massa_spin.value(),
            "Tanggal_Expire": self.expire_date_edit.date().toString("yyyy-MM-dd"),
            "Category_Hazard": self.hazard_combo.currentText(),
            "Sifat": self.sifat_edit.toPlainText(),
            "Tanggal_Produksi": self.prod_date_edit.date().toString("yyyy-MM-dd"),
            "Tanggal_Pembelian": self.purchase_date_edit.date().toString("yyyy-MM-dd"),
            "SDS": self.sds_edit.text(),
            # In a real implementation, you would get the actual storage ID based on rack_name
            "id_storage": self._get_storage_id_from_rack_name(),
        }

        try:
            if self.is_new:
                # Create new reagent
                result = self.identity_model.create(
                    name=reagent_data["Name"],
                    description=reagent_data["Description"],
                    wujud=reagent_data["Wujud"],
                    stock=reagent_data["Stock"],
                    massa=reagent_data["Massa"],
                    tanggal_expire=reagent_data["Tanggal_Expire"],
                    category_hazard=reagent_data["Category_Hazard"],
                    sifat=reagent_data["Sifat"],
                    tanggal_produksi=reagent_data["Tanggal_Produksi"],
                    tanggal_pembelian=reagent_data["Tanggal_Pembelian"],
                    sds=reagent_data["SDS"],
                    id_storage=reagent_data["id_storage"],
                )
                success_message = "New reagent added successfully"
            else:
                # Update existing reagent
                result = self.identity_model.update(self.reagent_id, **reagent_data)
                success_message = "Reagent updated successfully"

            if result:
                QMessageBox.information(self, "Success", success_message)
                # Return to rack view after successful save
                if self.parent_widget and hasattr(
                    self.parent_widget, "refresh_reagents"
                ):
                    self.parent_widget.refresh_reagents()
                    self.parent_widget.show_rack_view()
            else:
                QMessageBox.warning(self, "Error", "Failed to save reagent data")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def _delete_reagent(self):
        """Delete the current reagent"""
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this reagent?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                result = self.identity_model.delete(self.reagent_id)

                if result:
                    QMessageBox.information(
                        self, "Success", "Reagent deleted successfully"
                    )
                    # Return to rack view after successful deletion
                    if self.parent_widget and hasattr(
                        self.parent_widget, "refresh_reagents"
                    ):
                        self.parent_widget.refresh_reagents()
                        self.parent_widget.show_rack_view()
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete reagent")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def _go_back(self):
        """Return to the rack view without saving"""
        if self.parent_widget and hasattr(self.parent_widget, "show_rack_view"):
            self.parent_widget.show_rack_view()

    def _get_storage_id_from_rack_name(self):
        """Get storage ID from rack name - in a real app, query the database"""
        # This is a placeholder. In a real app, you'd query your Storage table
        # For now, we'll return a dummy ID based on the rack name
        # Example:
        # storage = self.storage_model.get_by_name(self.rack_name)
        # return storage["id"] if storage else 1

        # Dummy implementation - converts rack name to an integer ID
        if not self.rack_name:
            return 1

        try:
            # Extract any numeric part from the rack name
            import re

            match = re.search(r"\d+", self.rack_name)
            if match:
                return int(match.group())
            else:
                return 1
        except:
            return 1
