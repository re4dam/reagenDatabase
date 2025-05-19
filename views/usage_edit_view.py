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
from PyQt6.QtCore import Qt, pyqtSlot, QDate, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon
from app_context import AppContext
from load_font import FontManager

class UsageEditView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.usage_edit_viewmodel = None

        self._setup_ui()

    def set_viewmodel(self, viewmodel):
        """Set the ViewModel for this view"""
        self.usage_edit_viewmodel = viewmodel

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

        # Supporting materials field
        self.supporting_materials_edit = QTextEdit()
        self.supporting_materials_edit.setMaximumHeight(100)
        form_layout.addRow("Supporting Materials:", self.supporting_materials_edit)

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

        # Save button
        self.save_button = QPushButton(self)
        save_normal = QIcon("assets/Report/icon_save.png")
        save_hover = QIcon("assets/Report/save_hover.png")
        self.save_button.setIcon(save_normal)
        self.save_button.setIconSize(QSize(*self.scale_icon(174, 174)))
        self.save_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
        """)
        self.save_button.setGeometry(*self.scale_rect(1722, 865, 174, 174))
        self.save_button.enterEvent = lambda event: self.save_button.setIcon(save_hover)
        self.save_button.leaveEvent = lambda event: self.save_button.setIcon(save_normal)
        self.save_button.clicked.connect(self._save_usage)

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
        self.back_button.clicked.connect(self._cancel)

    @pyqtSlot(dict, bool, int)
    def on_usage_loaded(self, usage_data, is_new, current_stock):
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
        self.supporting_materials_edit.setText(usage_data.get("Bahan_Pendukung", ""))

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
            data = {
                "Tanggal_Terpakai": self.date_used_edit.date().toString("yyyy-MM-dd"),
                "Jumlah_Terpakai": self.amount_used_spin.value(),
                "User": self.user_edit.text(),
                "Bahan_Pendukung": self.supporting_materials_edit.toPlainText(),
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
