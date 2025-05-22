# views/usage_report_view.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QPushButton,
    QHeaderView,
    QMessageBox,
)
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QIcon
from viewmodels.usage_report_viewmodel import UsageReportViewModel
from app_context import AppContext
from load_font import FontManager

class UsageReportView(QWidget):
    # Signals to communicate with parent
    back_clicked = pyqtSignal()
    add_report_clicked = pyqtSignal(int, str)
    edit_report_clicked = pyqtSignal(int, int, str)

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

        # Load initial data
        self.refresh_data()

    def scale_rect(self, x, y, w, h):
        screen_size = AppContext.get_screen_resolution()
        scale_x = screen_size.width() / 1920
        scale_y = screen_size.height() / 1080
        return int(x * scale_x), int(y * scale_y), int(w * scale_x), int(h * scale_y)
    
    def scale_icon(self, w, h):
        screen_size = AppContext.get_screen_resolution()
        scale_x = screen_size.width() / 1920
        scale_y = screen_size.height() / 1080
        return int(w * scale_x), int(h * scale_y)
    
    def scale_style(self, px):
        screen_size = AppContext.get_screen_resolution()
        scale_y = screen_size.height() / 1080
        return int(px * scale_y)
    
    def _setup_ui(self):
        self.screen_size = AppContext.get_screen_resolution()
        self.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        background_label = QLabel(self)
        background_label.setPixmap(QPixmap("assets/Report/background.png"))  # Use your actual image path
        background_label.setScaledContents(True)
        background_label.setGeometry(*self.scale_rect(0, 0, 1920, 1080))

        report_bg = QLabel(self)
        report_bg.setPixmap(QPixmap("assets/report/report.png"))  # Use your actual image path
        report_bg.setScaledContents(True)
        report_bg.setGeometry(*self.scale_rect(89, 172, 1742, 830))

        # Table for displaying usage reports
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(
            ["Date Used", "Amount Used", "User", "Supporting\nMaterials", "Actions"]
        )
        self.table_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setShowGrid(False)
        self.table_widget.setStyleSheet(f"""
            QTableWidget {{
                color: black;
                outline: none;
                background: transparent;
                border: none;
            }}
            QHeaderView{{
                color: black;
                background: rgba(0, 0, 0, 35);
                border: none;
                border-top-left-radius: {self.scale_style(25)}px;
                border-top-right-radius: {self.scale_style(25)}px; 
            }}
            QHeaderView::section {{
                background: transparent;
                border: none;
                font-family: Figtree;
                font-size: {self.scale_style(40)}px;
                font-weight: bold;
                padding-right: {self.scale_style(30)}px;
            }}
            QTableWidget::item {{
                padding-left: {self.scale_style(10)}px;  /* isi menjauh dari header */
                padding-right: {self.scale_style(10)}px;  /* isi menjauh dari header */
                border-bottom: 1px solid #ccc;  /* hanya garis bawah antar baris */
            }}
            QTableWidget::item:selected {{
                color: white;
                background-color: rgba(0, 0, 0, 100);
            }}
        """)
        self.table_widget.setGeometry(*self.scale_rect(89, 172, 1742, 830))
        self.table_widget.setFont(FontManager.get_font("Figtree-Regular", self.scale_style(24)))
        self.table_widget.verticalHeader().setDefaultSectionSize(self.scale_style(55))
        self.table_widget.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        # Add New Usage Report button
        self.anew_report_button = QPushButton(self)
        add_normal = QIcon("assets/Report/add.png")
        add_hover = QIcon("assets/Report/add_hover.png")
        self.anew_report_button.setIcon(add_normal)
        self.anew_report_button.setIconSize(QSize(*self.scale_icon(170, 170)))
        self.anew_report_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
        """)
        self.anew_report_button.setGeometry(*self.scale_rect(1722, 865, 170, 170))
        self.anew_report_button.enterEvent = lambda event: self.anew_report_button.setIcon(add_hover)
        self.anew_report_button.leaveEvent = lambda event: self.anew_report_button.setIcon(add_normal)
        self.anew_report_button.clicked.connect(self._on_add_new_report)

        # Add circular back button in top-left corner
        self.back_button = QPushButton(self)
        back_normal = QIcon("assets/Report/icon_back.png")
        back_hover = QIcon("assets/Report/back_hover.png")
        self.back_button.setIcon(back_normal)
        self.back_button.setIconSize(QSize(*self.scale_icon(130, 130)))
        self.back_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        # Perubahan penting: Mengganti koneksi dari on_login_success ke _login
        self.back_button.setGeometry(*self.scale_rect(12, 12, 130, 130))
        self.back_button.enterEvent = lambda event: self.back_button.setIcon(back_hover)
        self.back_button.leaveEvent = lambda event: self.back_button.setIcon(back_normal)
        self.back_button.clicked.connect(self._on_back_clicked)

    def make_hover_event(self, button, normal_icon, hover_icon):
        def on_enter(event):
            button.setIcon(hover_icon)
        def on_leave(event):
            button.setIcon(normal_icon)
        button.enterEvent = on_enter
        button.leaveEvent = on_leave

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
            self.table_widget.item(row, 0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_widget.setItem(
                row, 1, QTableWidgetItem(str(report["amount_used"]))
            )
            self.table_widget.item(row, 1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_widget.setItem(row, 2, QTableWidgetItem(report["user"]))
            self.table_widget.item(row, 2).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_widget.setItem(
                row, 3, QTableWidgetItem(report["supporting_materials"])
            )
            self.table_widget.item(row, 3).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # Create action buttons (for edit and delete)
            actions_layout = QHBoxLayout()

            edit_button = QPushButton()
            edit_button.setProperty("report_id", report["id"])
            edit_button.clicked.connect(self._on_edit_report)
            icon_normal = QIcon("assets/Report/icon_edit.png")
            icon_hover = QIcon("assets/Report/edit_hover.png")
            edit_button.setIcon(icon_normal)
            edit_button.setIconSize(QSize(*self.scale_icon(38, 38)))
            edit_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: transparent;
                }
            """)
            self.make_hover_event(edit_button, icon_normal, icon_hover)
            edit_button.clicked.connect(self._on_edit_report)

            delete_button = QPushButton()
            delete_button.setProperty("report_id", report["id"])
            delete_button.clicked.connect(self._on_delete_report)
            delete_normal = QIcon("assets/Report/icon_delete.png")
            delete_hover = QIcon("assets/Report/delete_hover.png")
            delete_button.setIcon(delete_normal)
            delete_button.setIconSize(QSize(*self.scale_icon(38, 38)))
            delete_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: transparent;
                }
            """)
            self.make_hover_event(delete_button, delete_normal, delete_hover)

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

        # For backward compatibility with the original implementation
        # In case the signal isn't connected, try the legacy approach
        # if self.parent_widget and hasattr(self.parent_widget, "show_rack_view"):
        #     self.parent_widget.show_rack_view()

    def refresh_data(self):
        """Refresh the usage data display"""
        try:
            self.view_model.load_usage_data(self.reagent_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load usage data: {str(e)}")
