# views/usage_report_panel.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QPushButton,
    QFrame,
    QHeaderView,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from datetime import datetime


class UsageReportPanel(QWidget):
    def __init__(
        self, usage_model, identity_model, reagent_id, reagent_name, parent=None
    ):
        super().__init__(parent)
        self.usage_model = usage_model
        self.identity_model = identity_model
        self.reagent_id = reagent_id
        self.reagent_name = reagent_name
        self.parent_widget = parent

        # Set up the UI for this panel
        self._setup_ui()

        # Load usage data
        self._load_usage_data()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Panel title
        title_label = QLabel(f"Usage Reports for {self.reagent_name}")
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

        # Table for displaying usage reports
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(
            ["Date Used", "Amount Used", "User", "Supporting Materials", "Actions"]
        )
        self.table_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setStyleSheet(
            "QTableWidget { gridline-color: #d0d0d0; alternate-background-color: #f0f0f0; }"
        )
        main_layout.addWidget(self.table_widget)

        # Button layout
        button_layout = QHBoxLayout()

        # Add New Usage Report button
        self.new_report_button = QPushButton("Add New Usage Report")
        self.new_report_button.setMinimumHeight(40)
        self.new_report_button.setStyleSheet(
            "QPushButton { background-color: #ccccff; border: 2px solid #6666cc; "
            "border-radius: 5px; font-weight: bold; }"
            "QPushButton:hover { background-color: #a3a3d9; }"
        )
        self.new_report_button.clicked.connect(self._add_new_report)
        button_layout.addWidget(self.new_report_button)

        # Back button
        self.back_button = QPushButton("Back to Reagent Details")
        self.back_button.setMinimumHeight(40)
        self.back_button.clicked.connect(self._go_back)
        button_layout.addWidget(self.back_button)

        main_layout.addSpacing(10)
        main_layout.addLayout(button_layout)

    def _load_usage_data(self):
        """Load usage data for the current reagent"""
        try:
            print(
                f"[DEBUG] Usage model in _load_usage_data: {self.usage_model}"
            )  # Debug
            print(f"[DEBUG] Reagent ID: {self.reagent_id}")  # Debug
            usage_reports = self.usage_model.get_by_identity(self.reagent_id)

            # Clear the table
            self.table_widget.setRowCount(0)

            # Populate table with usage data
            for row, report in enumerate(usage_reports):
                self.table_widget.insertRow(row)

                # Format date to a more readable format
                date_used = report.get("Tanggal_Terpakai", "")
                if date_used:
                    try:
                        date_obj = datetime.strptime(date_used, "%Y-%m-%d")
                        date_used = date_obj.strftime("%d %b %Y")
                    except:
                        pass  # Keep original format if parsing fails

                # Create table items
                self.table_widget.setItem(row, 0, QTableWidgetItem(date_used))
                self.table_widget.setItem(
                    row, 1, QTableWidgetItem(str(report.get("Jumlah_Terpakai", 0)))
                )
                self.table_widget.setItem(
                    row, 2, QTableWidgetItem(report.get("User", ""))
                )
                self.table_widget.setItem(
                    row, 3, QTableWidgetItem(report.get("Bahan_Pendukung", ""))
                )

                # Create action button (for edit and delete)
                actions_layout = QHBoxLayout()

                edit_button = QPushButton("Edit")
                edit_button.setProperty("report_id", report.get("id"))
                edit_button.clicked.connect(self._edit_report)
                edit_button.setStyleSheet("QPushButton { max-width: 60px; }")

                delete_button = QPushButton("Delete")
                delete_button.setProperty("report_id", report.get("id"))
                delete_button.clicked.connect(self._delete_report)
                delete_button.setStyleSheet("QPushButton { max-width: 60px; }")

                actions_layout.addWidget(edit_button)
                actions_layout.addWidget(delete_button)
                actions_layout.setContentsMargins(0, 0, 0, 0)

                # Create a widget to hold the buttons
                actions_widget = QWidget()
                actions_widget.setLayout(actions_layout)

                # Add the widget to the table cell
                self.table_widget.setCellWidget(row, 4, actions_widget)

            # If no reports, show a message
            if len(usage_reports) == 0:
                self.table_widget.setRowCount(1)
                no_data_item = QTableWidgetItem(
                    "No usage reports found for this reagent"
                )
                no_data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_widget.setItem(0, 0, no_data_item)
                self.table_widget.setSpan(0, 0, 1, 5)  # Span across all columns

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load usage data: {str(e)}")

    def _add_new_report(self):
        """Open panel to add a new usage report"""
        try:
            if self.parent_widget and hasattr(
                self.parent_widget, "show_new_usage_report_panel"
            ):
                self.parent_widget.show_new_usage_report_panel(
                    self.reagent_id, self.reagent_name
                )
            else:
                QMessageBox.warning(
                    self,
                    "Function Not Available",
                    "The show_new_usage_report_panel function is not available in the parent widget.",
                )
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to open new usage report panel: {str(e)}"
            )

    def _edit_report(self):
        """Edit the selected usage report"""
        try:
            button = self.sender()
            if button:
                report_id = button.property("report_id")
                if self.parent_widget and hasattr(
                    self.parent_widget, "show_edit_usage_report_panel"
                ):
                    self.parent_widget.show_edit_usage_report_panel(
                        report_id, self.reagent_id, self.reagent_name
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Function Not Available",
                        "The show_edit_usage_report_panel function is not available in the parent widget.",
                    )
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to open edit usage report panel: {str(e)}"
            )

    def _delete_report(self):
        """Delete the selected usage report"""
        button = self.sender()
        if button:
            report_id = button.property("report_id")

            confirm = QMessageBox.question(
                self,
                "Confirm Deletion",
                "Are you sure you want to delete this usage report?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if confirm == QMessageBox.StandardButton.Yes:
                try:
                    result = self.usage_model.delete(report_id)

                    if result:
                        QMessageBox.information(
                            self, "Success", "Usage report deleted successfully"
                        )
                        self._load_usage_data()  # Refresh the table
                    else:
                        QMessageBox.warning(
                            self, "Error", "Failed to delete usage report"
                        )

                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def _go_back(self):
        """Return to the reagent detail panel"""
        if self.parent_widget and hasattr(self.parent_widget, "_view_reagent_details"):
            self.parent_widget._view_reagent_details(self.reagent_id)

    def refresh_data(self):
        """Refresh the usage data display"""
        self._load_usage_data()
