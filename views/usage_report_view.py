# reagenDatabaseGUI/views/usage_report_view.py
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
    QFileDialog,  # Ensure QFileDialog is imported
    QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal, QSize, QPropertyAnimation, QSequentialAnimationGroup, QParallelAnimationGroup, QEasingCurve, QPoint
from PyQt6.QtGui import QPixmap, QIcon
from viewmodels.usage_report_viewmodel import (
    UsageReportViewModel,
)  # Ensure this import is correct
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

        self.view_model = UsageReportViewModel(usage_model, identity_model)
        self.reagent_id = reagent_id
        self.reagent_name = reagent_name
        self.parent_widget = parent

        self._setup_ui()

        self.view_model.data_changed.connect(self._refresh_table)
        self.view_model.export_finished.connect(self._on_export_finished)

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
    
    def mainAnimation(self):
        start_panel_main_x, start_panel_main_y, _, _ = self.scale_rect(0, 1080, 0, 0) # Target Y=0 (atas)
        target_panel_main_x, target_panel_main_y, _, _ = self.scale_rect(0, 0, 0, 0) # Target Y=0 (atas)

        self.sequence = QParallelAnimationGroup(self)

        self.panel_main_animation_obj = QPropertyAnimation(self.panel_main, b"pos") # Simpan referensi
        self.panel_main_animation_obj.setDuration(750)
        self.panel_main_animation_obj.setStartValue(QPoint(start_panel_main_x, start_panel_main_y)) # Tidak perlu jika sudah di posisi awal
        self.panel_main_animation_obj.setEndValue(QPoint(target_panel_main_x, target_panel_main_y))
        self.panel_main_animation_obj.setEasingCurve(QEasingCurve.Type.OutBack)
        self.sequence.addAnimation(self.panel_main_animation_obj)

        export_button_animation = QPropertyAnimation(self.export_button_effect, b"opacity")
        export_button_animation.setDuration(750)
        export_button_animation.setStartValue(0.0)
        export_button_animation.setEndValue(1.0)
        export_button_animation.setEasingCurve(QEasingCurve.Type.InQuad)
        self.sequence.addAnimation(export_button_animation)

        self.sequence.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
    
    def TransitionAnimation(self):
        start_panel_main_x, start_panel_main_y, _, _ = self.scale_rect(-1920, 0, 0, 0) # Target Y=0 (atas)
        target_panel_main_x, target_panel_main_y, _, _ = self.scale_rect(0, 0, 0, 0) # Target Y=0 (atas)

        self.sequence = QParallelAnimationGroup(self)

        self.panel_main_animation_obj = QPropertyAnimation(self.panel_main, b"pos") # Simpan referensi
        self.panel_main_animation_obj.setDuration(750)
        self.panel_main_animation_obj.setStartValue(QPoint(start_panel_main_x, start_panel_main_y)) # Tidak perlu jika sudah di posisi awal
        self.panel_main_animation_obj.setEndValue(QPoint(target_panel_main_x, target_panel_main_y))
        self.panel_main_animation_obj.setEasingCurve(QEasingCurve.Type.InOutBack)
        self.sequence.addAnimation(self.panel_main_animation_obj)

        export_button_animation = QPropertyAnimation(self.export_button_effect, b"opacity")
        export_button_animation.setDuration(750)
        export_button_animation.setStartValue(0.0)
        export_button_animation.setEndValue(1.0)
        export_button_animation.setEasingCurve(QEasingCurve.Type.InQuad)
        self.sequence.addAnimation(export_button_animation)

        self.sequence.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    def _setup_ui(self):
        self.screen_size = AppContext.get_screen_resolution()
        self.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())

        background_label = QLabel(self)
        background_label.setPixmap(QPixmap("assets/Report/background.png"))
        background_label.setScaledContents(True)
        background_label.setGeometry(*self.scale_rect(0, 0, 1920, 1080))

        self.panel_main = QWidget(self)
        self.panel_main.setGeometry(0, 1080, self.screen_size.width() * 2, self.screen_size.height())

        report_bg = QLabel(self.panel_main)
        report_bg.setPixmap(QPixmap("assets/report/report.png"))
        report_bg.setScaledContents(True)
        report_bg.setGeometry(*self.scale_rect(89, 172, 1742, 830))

        report_bg2 = QLabel(self.panel_main)
        report_bg2.setPixmap(QPixmap("assets/Report/report_edit.png"))
        report_bg2.setScaledContents(True)
        report_bg2.setGeometry(*self.scale_rect(2009, 172, 1742, 830))

        self.table_widget = QTableWidget(self.panel_main)
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
                color: black; outline: none; background: transparent; border: none;
            }}
            QHeaderView{{
                color: black; background: rgba(0, 0, 0, 35); border: none;
                border-top-left-radius: {self.scale_style(25)}px;
                border-top-right-radius: {self.scale_style(25)}px; 
            }}
            QHeaderView::section {{
                background: transparent; border: none; font-family: Figtree;
                font-size: {self.scale_style(40)}px; font-weight: bold;
                padding-right: {self.scale_style(30)}px;
            }}
            QTableWidget::item {{
                padding-left: {self.scale_style(10)}px; padding-right: {self.scale_style(10)}px;
                border-bottom: 1px solid #ccc;
            }}
            QTableWidget::item:selected {{
                color: white; background-color: rgba(0, 0, 0, 100);
            }}
        """)
        self.table_widget.setGeometry(*self.scale_rect(89, 172, 1742, 830 - 70))
        self.table_widget.setFont(
            FontManager.get_font("Figtree-Regular", self.scale_style(24))
        )
        self.table_widget.verticalHeader().setDefaultSectionSize(self.scale_style(55))
        self.table_widget.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.anew_report_button = QPushButton(self.panel_main)
        self.anew_report_button.setIconSize(QSize(*self.scale_icon(170, 170)))
        self.anew_report_button.setStyleSheet("border: none; background: transparent;")
        self.anew_report_button.setGeometry(*self.scale_rect(1722, 865, 170, 170))
        self.make_hover_event(
            self.anew_report_button,
            "assets/Report/add.png",
            "assets/Report/add_hover.png",
        )
        self.anew_report_button.clicked.connect(self._on_add_new_report)

        self.export_button = QPushButton(self)
        self.export_button.setIconSize(QSize(*self.scale_icon(80, 80)))
        self.export_button.setStyleSheet("border: none; background: transparent;")
        self.export_button.setGeometry(*self.scale_rect(1800, 35, 80, 80))
        self.make_hover_event(
            self.export_button,
            "assets/Report/icon_normal.png",
            "assets/Report/icon_hover.png",
        )
        self.export_button.clicked.connect(self._on_export_report)
        self.export_button_effect = QGraphicsOpacityEffect(self.export_button)
        self.export_button.setGraphicsEffect(self.export_button_effect)
        self.export_button_effect.setOpacity(0.0)

        self.back_button = QPushButton(self)
        self.make_hover_event(
            self.back_button,
            "assets/Report/icon_back.png",
            "assets/Report/back_hover.png",
        )
        self.back_button.setIconSize(QSize(*self.scale_icon(130, 130)))
        self.back_button.setStyleSheet("border: none; background-color: transparent;")
        self.back_button.setGeometry(*self.scale_rect(12, 12, 130, 130))
        self.back_button.clicked.connect(self._on_back_clicked)

    def make_hover_event(self, button, normal_icon_path, hover_icon_path):
        normal_icon = QIcon(normal_icon_path)
        hover_icon = QIcon(hover_icon_path)
        if normal_icon.isNull() or hover_icon.isNull():
            print(
                f"Warning: Could not load icons for button: {normal_icon_path} or {hover_icon_path}"
            )
            # Fallback to text if button has no text yet and icons failed
            if not button.text():
                button.setText(
                    normal_icon_path.split("/")[-1].split(".")[0][:3]
                )  # e.g. "ico" from "icon_back.png"
            return

        button.setIcon(normal_icon)

        # Store icons on the button itself to prevent them from being garbage collected
        # if they are not referenced elsewhere, which can happen with lambdas in some cases.
        button._normal_icon = normal_icon
        button._hover_icon = hover_icon

        button.enterEvent = lambda event, b=button: b.setIcon(b._hover_icon)
        button.leaveEvent = lambda event, b=button: b.setIcon(b._normal_icon)

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
            self.table_widget.item(row, 0).setTextAlignment(
                Qt.AlignmentFlag.AlignCenter
            )
            self.table_widget.setItem(
                row, 1, QTableWidgetItem(str(report["amount_used"]))
            )
            self.table_widget.item(row, 1).setTextAlignment(
                Qt.AlignmentFlag.AlignCenter
            )
            self.table_widget.setItem(row, 2, QTableWidgetItem(report["user"]))
            self.table_widget.item(row, 2).setTextAlignment(
                Qt.AlignmentFlag.AlignCenter
            )
            self.table_widget.setItem(
                row, 3, QTableWidgetItem(report["supporting_materials"])
            )
            self.table_widget.item(row, 3).setTextAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

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

        if len(usage_reports) == 0:
            self.table_widget.setRowCount(1)
            no_data_item = QTableWidgetItem("No usage reports found for this reagent")
            no_data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_widget.setItem(0, 0, no_data_item)
            self.table_widget.setSpan(0, 0, 1, 5)

    def _on_add_new_report(self):
        self.add_report_clicked.emit(self.reagent_id, self.reagent_name)

    def _on_edit_report(self):
        button = self.sender()
        if button:
            report_id = button.property("report_id")
            self.edit_report_clicked.emit(report_id, self.reagent_id, self.reagent_name)

    def _on_delete_report(self):
        button = self.sender()
        if button:
            report_id = button.property("report_id")
            confirm = QMessageBox.question(
                self,
                "Confirm Deletion",
                "Are you sure you want to delete this usage report? This will revert the stock.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if confirm == QMessageBox.StandardButton.Yes:
                if self.view_model.delete_report(report_id, self.reagent_id):
                    QMessageBox.information(
                        self,
                        "Success",
                        "Usage report deleted and stock updated successfully.",
                    )
                else:
                    QMessageBox.warning(
                        self, "Error", "Failed to delete usage report or update stock."
                    )

    def _on_back_clicked(self):
        self.back_clicked.emit()

    def refresh_data(self):
        try:
            if not self.view_model.load_usage_data(self.reagent_id):
                QMessageBox.warning(
                    self,
                    "Data Load Issue",
                    f"Could not fully load usage data for {self.reagent_name}.",
                )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load usage data: {str(e)}")

    def _on_export_report(self):
        default_filename = f"{self.reagent_name.replace(' ', '_')}_usage_report.xlsx"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Usage Report",
            default_filename,
            "Excel Files (*.xlsx);;All Files (*)",
        )
        if file_path:
            self.view_model.export_usage_data_to_xlsx(
                self.reagent_id, file_path, self.reagent_name
            )

    @pyqtSlot(bool, str)
    def _on_export_finished(self, success, message):
        if success:
            QMessageBox.information(self, "Export Successful", message)
        else:
            QMessageBox.critical(self, "Export Failed", message)
