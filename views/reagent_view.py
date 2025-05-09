# views/reagent_panel_view.py
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
from PyQt6.QtCore import Qt, QDate, pyqtSignal

from viewmodels.reagent_viewmodel import ReagentViewModel


class ReagentDetailPanel(QWidget):
    """
    View component responsible for displaying and interacting with reagent data.
    """

    back_to_rack_view = pyqtSignal()
    refresh_requested = pyqtSignal()

    def __init__(self, identity_model, reagent_id=None, rack_name=None, parent=None):
        super().__init__(parent)
        self.parent_widget = parent

        # Initialize the ViewModel
        self.view_model = ReagentViewModel(identity_model, reagent_id, rack_name)

        # Set up the UI for this panel
        self._setup_ui()

        # If editing existing reagent, load its data
        if not self.view_model.is_new and self.view_model.reagent_id:
            self._load_reagent_data()

        # Set initial edit state
        self._set_edit_state(self.view_model.edit_mode)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Panel title
        title_text = "Add New Reagent" if self.view_model.is_new else "Reagent Details"
        self.title_label = QLabel(title_text)
        title_font = QLabel().font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.title_label)

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
        self.storage_id_label = QLabel(f"Storage: {self.view_model.rack_name}")
        form_layout.addRow("Storage Location:", self.storage_id_label)

        main_layout.addLayout(form_layout)

        # Buttons layout
        self.buttons_layout = QHBoxLayout()

        # Edit button (only for existing reagents)
        if not self.view_model.is_new:
            self.edit_button = QPushButton("Edit")
            self.edit_button.setMinimumHeight(40)
            self.edit_button.setStyleSheet(
                "QPushButton { background-color: #f0f0f0; border: 2px solid #c0c0c0; "
                "border-radius: 5px; font-weight: bold; }"
                "QPushButton:hover { background-color: #e0e0e0; }"
            )
            self.edit_button.clicked.connect(self._toggle_edit_mode)
            self.buttons_layout.addWidget(self.edit_button)

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.setMinimumHeight(40)
        self.save_button.setStyleSheet(
            "QPushButton { background-color: #ccffcc; border: 2px solid #66cc66; "
            "border-radius: 5px; font-weight: bold; }"
            "QPushButton:hover { background-color: #a3d9a3; }"
        )
        self.save_button.clicked.connect(self._save_reagent)
        self.buttons_layout.addWidget(self.save_button)

        # Delete button (only for existing reagents)
        if not self.view_model.is_new:
            self.delete_button = QPushButton("Delete")
            self.delete_button.setMinimumHeight(40)
            self.delete_button.setStyleSheet(
                "QPushButton { background-color: #ffcccc; border: 2px solid #ff6666; "
                "border-radius: 5px; font-weight: bold; }"
                "QPushButton:hover { background-color: #ffaaaa; }"
            )
            self.delete_button.clicked.connect(self._delete_reagent)
            self.buttons_layout.addWidget(self.delete_button)

        # Usage Reports button (only for existing reagents)
        if not self.view_model.is_new:
            self.usage_button = QPushButton("View Usage Reports")
            self.usage_button.setMinimumHeight(40)
            self.usage_button.setStyleSheet(
                "QPushButton { background-color: #ccccff; border: 2px solid #6666cc; "
                "border-radius: 5px; font-weight: bold; }"
                "QPushButton:hover { background-color: #a3a3d9; }"
            )
            self.usage_button.clicked.connect(self._show_usage_reports)
            self.buttons_layout.addWidget(self.usage_button)

        # Cancel button (only visible in edit mode)
        if not self.view_model.is_new:
            self.cancel_button = QPushButton("Cancel")
            self.cancel_button.setMinimumHeight(40)
            self.cancel_button.setStyleSheet(
                "QPushButton { background-color: #f0f0f0; border: 2px solid #c0c0c0; "
                "border-radius: 5px; font-weight: bold; }"
                "QPushButton:hover { background-color: #e0e0e0; }"
            )
            self.cancel_button.clicked.connect(self._cancel_edit)
            self.buttons_layout.addWidget(self.cancel_button)

        # Back button
        self.back_button = QPushButton("Back to Rack View")
        self.back_button.setMinimumHeight(40)
        self.back_button.clicked.connect(self._go_back)
        self.buttons_layout.addWidget(self.back_button)

        main_layout.addSpacing(20)
        main_layout.addLayout(self.buttons_layout)

        # Create a list of all input widgets for easy access when toggling edit mode
        self.input_widgets = [
            self.name_edit,
            self.description_edit,
            self.wujud_combo,
            self.stock_spin,
            self.massa_spin,
            self.expire_date_edit,
            self.hazard_combo,
            self.sifat_edit,
            self.prod_date_edit,
            self.purchase_date_edit,
            self.sds_edit,
        ]

    def _load_reagent_data(self):
        """Load data for an existing reagent from the ViewModel"""
        reagent = self.view_model.get_reagent_data()

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

    def _toggle_edit_mode(self):
        """Toggle between view and edit modes"""
        self.view_model.toggle_edit_mode()
        self._set_edit_state(self.view_model.edit_mode)

        # Update title based on mode
        if self.view_model.edit_mode:
            self.title_label.setText("Edit Reagent Details")
        else:
            self.title_label.setText("Reagent Details")

    def _set_edit_state(self, editable):
        """Set the edit state of all input widgets"""
        for widget in self.input_widgets:
            if isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
                widget.setReadOnly(not editable)
                # Apply style to indicate read-only state
                if not editable:
                    widget.setStyleSheet("background-color: #f0f0f0;")
                else:
                    widget.setStyleSheet("")
            elif (
                isinstance(widget, QComboBox)
                or isinstance(widget, QSpinBox)
                or isinstance(widget, QDateEdit)
            ):
                widget.setEnabled(editable)

        # Defensive checks
        if not self.view_model.is_new:
            if hasattr(self, "edit_button"):
                self.edit_button.setVisible(not editable)
            self.save_button.setVisible(editable)
            if hasattr(self, "delete_button"):
                self.delete_button.setVisible(True)
            if hasattr(self, "usage_button"):
                self.usage_button.setVisible(True)
            if hasattr(self, "cancel_button"):
                self.cancel_button.setVisible(editable)
        else:
            self.save_button.setVisible(True)
            if hasattr(self, "cancel_button"):
                self.cancel_button.setVisible(False)

        # # Update button visibility based on mode
        # if not self.view_model.is_new:
        #     self.edit_button.setVisible(not editable)
        #     self.save_button.setVisible(editable)
        #     self.delete_button.setVisible(True)  # Always visible
        #     self.usage_button.setVisible(True)  # Always visible
        #     self.cancel_button.setVisible(editable)
        # else:
        #     # For new reagents, save button is always visible
        #     self.save_button.setVisible(True)
        #     if hasattr(self, "cancel_button"):
        #         self.cancel_button.setVisible(False)

    def _collect_form_data(self):
        """Collect the form data from UI elements"""
        return {
            "name": self.name_edit.text(),
            "description": self.description_edit.toPlainText(),
            "wujud": self.wujud_combo.currentText(),
            "stock": self.stock_spin.value(),
            "massa": self.massa_spin.value(),
            "tanggal_expire": self.expire_date_edit.date().toString("yyyy-MM-dd"),
            "category_hazard": self.hazard_combo.currentText(),
            "sifat": self.sifat_edit.toPlainText(),
            "tanggal_produksi": self.prod_date_edit.date().toString("yyyy-MM-dd"),
            "tanggal_pembelian": self.purchase_date_edit.date().toString("yyyy-MM-dd"),
            "sds": self.sds_edit.text(),
        }

    def _save_reagent(self):
        """Save the reagent data"""
        reagent_data = self._collect_form_data()

        try:
            result, message = self.view_model.save_reagent(reagent_data)

            if result:
                QMessageBox.information(self, "Success", message)

                # If we just created a new reagent, update our state
                if self.view_model.is_new and self.view_model.reagent_id:
                    # Signal refresh to parent
                    self.refresh_requested.emit()
                    self._go_back()
                else:
                    # Reload data and exit edit mode for existing reagent
                    self._load_reagent_data()
                    self._set_edit_state(False)
                    self.title_label.setText("Reagent Details")
            else:
                QMessageBox.warning(
                    self, "Error", message or "Failed to save reagent data"
                )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def _cancel_edit(self):
        """Cancel editing and revert to original data"""
        self.view_model.cancel_edit()

        # Reload data from view model
        self._load_reagent_data()

        # Exit edit mode
        self._set_edit_state(False)
        self.title_label.setText("Reagent Details")

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
                result, message = self.view_model.delete_reagent()

                if result:
                    QMessageBox.information(self, "Success", message)
                    # Signal refresh to parent and go back
                    self.refresh_requested.emit()
                    self._go_back()
                else:
                    QMessageBox.warning(
                        self, "Error", message or "Failed to delete reagent"
                    )

            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def _show_usage_reports(self):
        """Show usage reports for this reagent"""
        if not self.view_model.is_new and self.view_model.reagent_id:
            if (self.parent_widget) and hasattr(
                self.parent_widget, "show_usage_reports"
            ):
                reagent_name = self.name_edit.text()
                self.parent_widget.show_usage_reports(
                    self.view_model.reagent_id, reagent_name
                )
            else:
                QMessageBox.warning(
                    self,
                    "Not Implemented",
                    "The parent widget does not have a show_usage_reports method.",
                )
        else:
            QMessageBox.warning(
                self, "Error", "Please save the reagent before viewing usage reports."
            )

    def _go_back(self):
        """Return to the rack view without saving"""
        self.back_to_rack_view.emit()

        # For backward compatibility with the original implementation
        # In case the signal isn't connected, try the legacy approach
        if self.parent_widget and hasattr(self.parent_widget, "show_rack_view"):
            self.parent_widget.show_rack_view()
