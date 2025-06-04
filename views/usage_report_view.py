# views/usage_report_view.py
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
    QFileDialog,  # Import QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from viewmodels.usage_report_viewmodel import UsageReportViewModel


class UsageReportView(QWidget):
    # Signals to communicate with parent
    back_clicked = pyqtSignal()
    add_report_clicked = pyqtSignal(int, str)
    edit_report_clicked = pyqtSignal(int, int, str)
    # Add a new signal for export
    export_report_requested = pyqtSignal(int, str)  # reagent_id, file_path

    def __init__(
        self, usage_model, identity_model, reagent_id, reagent_name, parent=None
    ):
        super().__init__(parent)

        # Create the view model
        self.view_model = UsageReportViewModel(usage_model, identity_model)

        # Store reagent information
        self.reagent_id = reagent_id
        self.reagent_name = reagent_name

        # Set up the UI for this panel
        self._setup_ui()

        # Connect view model signals
        self.view_model.data_changed.connect(self._refresh_table)
        # Connect the new signal from view model for export feedback
        self.view_model.export_finished.connect(self._on_export_finished)

        # Load initial data
        self.refresh_data()

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
        self.table_widget.setColumnCount(5)  # Adjusted for actions
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
        self.new_report_button.clicked.connect(self._on_add_new_report)
        button_layout.addWidget(self.new_report_button)

        # Export to XLSX button
        self.export_button = QPushButton("Export to XLSX")
        self.export_button.setMinimumHeight(40)
        self.export_button.setStyleSheet(
            "QPushButton { background-color: #cceeff; border: 2px solid #66aabb; "  # Example style
            "border-radius: 5px; font-weight: bold; }"
            "QPushButton:hover { background-color: #a3ccdd; }"
        )
        self.export_button.clicked.connect(
            self._on_export_report
        )  # Connect to new handler
        button_layout.addWidget(self.export_button)

        # Back button
        self.back_button = QPushButton("Back to Reagent Details")
        self.back_button.setMinimumHeight(40)
        self.back_button.clicked.connect(self._on_back_clicked)
        button_layout.addWidget(self.back_button)

        main_layout.addSpacing(10)
        main_layout.addLayout(button_layout)

    def _refresh_table(self):
        """Refresh the table with data from view model"""
        # Clear the table
        self.table_widget.setRowCount(0)

        usage_reports = self.view_model.usage_reports

        # Populate table with usage data
        for row, report in enumerate(usage_reports):
            self.table_widget.insertRow(row)

            # Fill cells with data
            self.table_widget.setItem(
                row, 0, QTableWidgetItem(report["formatted_date"])
            )
            self.table_widget.setItem(
                row, 1, QTableWidgetItem(str(report["amount_used"]))
            )
            self.table_widget.setItem(row, 2, QTableWidgetItem(report["user"]))
            self.table_widget.setItem(
                row, 3, QTableWidgetItem(report["supporting_materials"])
            )

            # Create action buttons (for edit and delete)
            actions_layout = QHBoxLayout()

            edit_button = QPushButton("Edit")
            edit_button.setProperty("report_id", report["id"])
            edit_button.clicked.connect(self._on_edit_report)
            edit_button.setStyleSheet("QPushButton { max-width: 60px; }")

            delete_button = QPushButton("Delete")
            delete_button.setProperty("report_id", report["id"])
            delete_button.clicked.connect(self._on_delete_report)
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
            no_data_item = QTableWidgetItem("No usage reports found for this reagent")
            no_data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_widget.setItem(0, 0, no_data_item)
            self.table_widget.setSpan(0, 0, 1, 5)  # Span across all columns

    def _on_add_new_report(self):
        """Handler for add new report button click"""
        self.add_report_clicked.emit(self.reagent_id, self.reagent_name)

    def _on_edit_report(self):
        """Handler for edit report button click"""
        button = self.sender()
        if button:
            report_id = button.property("report_id")
            self.edit_report_clicked.emit(report_id, self.reagent_id, self.reagent_name)

    def _on_delete_report(self):
        """Handler for delete report button click"""
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
                    success = self.view_model.delete_report(report_id)

                    if success:
                        QMessageBox.information(
                            self, "Success", "Usage report deleted successfully"
                        )
                        self.refresh_data()  # Refresh the table
                    else:
                        QMessageBox.warning(
                            self, "Error", "Failed to delete usage report"
                        )

                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def _on_back_clicked(self):
        """Handler for back button click"""
        self.back_clicked.emit()

    def refresh_data(self):
        """Refresh the usage data display"""
        try:
            self.view_model.load_usage_data(self.reagent_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load usage data: {str(e)}")

    def _on_export_report(self):
        """Handle export report button click."""
        # Open a file dialog to get the save path
        # The default name could include the reagent name and current date
        default_filename = f"{self.reagent_name.replace(' ', '_')}_usage_report.xlsx"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Usage Report",
            default_filename,  # Default file name
            "Excel Files (*.xlsx)",
        )

        if file_path:
            # Emit the signal with reagent_id and chosen file_path
            # self.export_report_requested.emit(self.reagent_id, file_path) # Old signal
            # Call viewmodel directly
            if self.view_model:
                self.view_model.export_usage_data_to_xlsx(
                    self.reagent_id, file_path, self.reagent_name
                )

    @pyqtSlot(bool, str)
    def _on_export_finished(self, success, message):
        """Handle feedback from the export process."""
        if success:
            QMessageBox.information(self, "Export Successful", message)
        else:
            QMessageBox.warning(self, "Export Failed", message)
