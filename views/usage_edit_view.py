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
    QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSlot, QDate, QSize, QRect, QPropertyAnimation, QSequentialAnimationGroup, QParallelAnimationGroup, QEasingCurve, QPoint
from PyQt6.QtGui import QFont, QPixmap, QIcon
from app_context import AppContext
from load_font import FontManager

class UsageEditView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.usage_edit_viewmodel = None
        self.sequence = None # Akan diinisialisasi di mainAnimation
        
        self._setup_ui()
        self.mainAnimation()

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
    
    def mainAnimation(self):

        start_panel_main_x, start_panel_main_y, _, _ = self.scale_rect(2009, 172, 1742, 830) # Target Y=0 (atas)
        target_panel_main_x, target_panel_main_y, _, _ = self.scale_rect(89, 172, 1742, 830) # Target Y=0 (atas)
        target_report_view_x, target_report_view_y, _, _ = self.scale_rect(-1831, 172, 1742, 830) # Target Y=0 (atas)

        # Hentikan animasi sebelumnya jika ada
        if hasattr(self, 'sequence') and self.sequence and \
           self.sequence.state() == QPropertyAnimation.State.Running:
            self.sequence.stop()

        self.sequence = QParallelAnimationGroup(self)

        self.panel_main_animation_obj = QPropertyAnimation(self.report_bg, b"pos", self) # Simpan referensi
        self.panel_main_animation_obj.setDuration(750)
        self.panel_main_animation_obj.setStartValue(QPoint(start_panel_main_x, start_panel_main_y)) # Tidak perlu jika sudah di posisi awal
        self.panel_main_animation_obj.setEndValue(QPoint(target_panel_main_x, target_panel_main_y))
        self.panel_main_animation_obj.setEasingCurve(QEasingCurve.Type.InOutBack)
        self.sequence.addAnimation(self.panel_main_animation_obj)

        self.panel_main_animation_obj2 = QPropertyAnimation(self.form_widget, b"pos", self) # Simpan referensi
        self.panel_main_animation_obj2.setDuration(750)
        self.panel_main_animation_obj2.setStartValue(QPoint(start_panel_main_x, start_panel_main_y)) # Tidak perlu jika sudah di posisi awal
        self.panel_main_animation_obj2.setEndValue(QPoint(target_panel_main_x, target_panel_main_y))
        self.panel_main_animation_obj2.setEasingCurve(QEasingCurve.Type.InOutBack)
        self.sequence.addAnimation(self.panel_main_animation_obj2)

        self.report_view_animation = QPropertyAnimation(self.report_view_bg, b"pos", self) # Simpan referensi
        self.report_view_animation.setDuration(750)
        self.report_view_animation.setStartValue(QPoint(target_panel_main_x, target_panel_main_y))# Tidak perlu jika sudah di posisi awal
        self.report_view_animation.setEndValue(QPoint(target_report_view_x, target_report_view_y))
        self.report_view_animation.setEasingCurve(QEasingCurve.Type.InOutBack)
        self.sequence.addAnimation(self.report_view_animation)

        self.sequence.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    def _setup_ui(self):
        self.screen_size = AppContext.get_screen_resolution()
        self.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        background_label = QLabel(self)
        background_label.setPixmap(QPixmap("assets/Report/background.png"))  # Use your actual image path
        background_label.setScaledContents(True)
        background_label.setGeometry(*self.scale_rect(0, 0, 1920, 1080))

        self.report_bg = QLabel(self)
        self.report_bg.setPixmap(QPixmap("assets/Report/report.png"))  # Use your actual image path
        self.report_bg.setScaledContents(True)
        self.report_bg.setGeometry(*self.scale_rect(2009, 172, 1742, 830))

        self.report_view_bg = QLabel(self)
        self.report_view_bg.setPixmap(QPixmap("assets/Report/report_view.png"))  # Use your actual image path
        self.report_view_bg.setScaledContents(True)
        self.report_view_bg.setGeometry(*self.scale_rect(89, 172, 1742, 830))

        # Form layout
        self.form_widget = QWidget(self)
        self.form_widget.setGeometry(*self.scale_rect(2009, 172, 1742, 830))
        form_layout = QVBoxLayout(self.form_widget)
        form_layout.setContentsMargins(20, 10, 20, 10)

        # Label Date
        date_used_label = QLabel(self.form_widget)
        date_used_label.setText("Date Used:")
        date_used_label.setFont(FontManager.get_font("Figtree-Regular", self.scale_style(30)))
        date_used_label.setFixedHeight(50)
        date_used_label.setStyleSheet("color: black; font-weight: bold;")
        form_layout.addWidget(date_used_label)

        # Field Date
        self.date_used_edit = QDateEdit(self.form_widget)
        self.date_used_edit.setCalendarPopup(True)
        self.date_used_edit.setStyleSheet("""
            QDateEdit {
                border: none; 
                background: rgba(0, 0, 0, 25); 
                color: #000000
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 40px;
            }
            QDateEdit::down-arrow {
                image: url(assets/ReagenView/calendar.png);
                width: 40px;
                height: 40px;
            }
        """)
        another_calendar = self.date_used_edit.calendarWidget()
        another_calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: #222;
                border: 1px solid #555;
                color: #ddd;
            }
            QCalendarWidget QToolButton {
                background-color: #333;
                color: #fff;
                border: none;
                margin: 5px;
                font-weight: bold;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #444;
            }
            QCalendarWidget QMenu {
                background-color: #333;
                color: #fff;
            }
            QCalendarWidget QSpinBox {
                background: #333;
                color: #fff;
            }
            QCalendarWidget QAbstractItemView:enabled {
                background-color: #111;
                color: #ccc;
                selection-background-color: #555;
                selection-color: #fff;
                gridline-color: #333;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #222;
            }
            QCalendarWidget QAbstractItemView {
                outline: 0;
            }
        """)
        another_calendar.setFixedSize(300, 300)
        self.date_used_edit.setFont(FontManager.get_font("Figtree-Regular", self.scale_style(26)))
        form_layout.addWidget(self.date_used_edit)

        spacer = QLabel("")
        form_layout.addWidget(spacer)

        # Label Amount
        amount_used_label = QLabel(self.form_widget)
        amount_used_label.setText("Amount Used:")
        amount_used_label.setFont(FontManager.get_font("Figtree-Regular", self.scale_style(30)))
        amount_used_label.setFixedHeight(50)
        amount_used_label.setStyleSheet("color: black; font-weight: bold;")
        form_layout.addWidget(amount_used_label)

        # Field Amount
        self.amount_used_spin = QSpinBox(self.form_widget)
        self.amount_used_spin.setFont(FontManager.get_font("Figtree-Regular", self.scale_style(26)))
        self.amount_used_spin.setRange(1, 10000)
        self.amount_used_spin.setStyleSheet("border: none; background: rgba(0, 0, 0, 25); color: #000000")
        form_layout.addWidget(self.amount_used_spin)

        spacer = QLabel("")
        form_layout.addWidget(spacer)

        # Label User
        user_label = QLabel(self.form_widget)
        user_label.setText("User: ")
        user_label.setFont(FontManager.get_font("Figtree-Regular", self.scale_style(30)))
        user_label.setFixedHeight(50)
        user_label.setStyleSheet("color: black; font-weight: bold;")
        form_layout.addWidget(user_label)

        # User field
        self.user_edit = QLineEdit(self.form_widget)
        self.user_edit.setFont(FontManager.get_font("Figtree-Regular", self.scale_style(26)))
        self.user_edit.setStyleSheet("border: none; background: rgba(0, 0, 0, 25); color: #000000")
        form_layout.addWidget(self.user_edit)

        spacer = QLabel("")
        form_layout.addWidget(spacer)

        # Label Supporting Materials
        supporting_materials_label = QLabel(self.form_widget)
        supporting_materials_label.setText("Supporting Materials: ")
        supporting_materials_label.setFont(FontManager.get_font("Figtree-Regular", self.scale_style(30)))
        supporting_materials_label.setFixedHeight(50)
        supporting_materials_label.setStyleSheet("color: black; font-weight: bold;")
        form_layout.addWidget(supporting_materials_label)

        # Supporting materials field
        self.supporting_materials_edit = QTextEdit(self.form_widget)
        self.supporting_materials_edit.setMaximumHeight(250)
        self.supporting_materials_edit.setFont(FontManager.get_font("Figtree-Regular", self.scale_style(20)))
        self.supporting_materials_edit.setStyleSheet("border: none; background: rgba(0, 0, 0, 25); color: #000000")
        form_layout.addWidget(self.supporting_materials_edit)

        spacer = QLabel("")
        form_layout.addWidget(spacer)

        # Current stock information
        self.current_stock_label = QLabel(self.form_widget)
        self.current_stock_label.setFont(FontManager.get_font("Figtree-Regular", self.scale_style(24)))
        self.current_stock_label.setStyleSheet("font-weight: bold;")
        form_layout.addWidget(self.current_stock_label)

        # Warning label for stock
        self.stock_warning_label = QLabel(self.form_widget)
        self.stock_warning_label.setFont(FontManager.get_font("Figtree-Regular", self.scale_style(24)))
        self.stock_warning_label.setStyleSheet("color: red; font-weight: bold;")
        self.stock_warning_label.setVisible(False)
        form_layout.addWidget(self.stock_warning_label)

        spacer = QLabel("")
        form_layout.addWidget(spacer)

        # Save button
        self.save_button = QPushButton(self)
        save_normal = QIcon("assets/Report/icon_save.png")
        save_hover = QIcon("assets/Report/save_hover.png")
        self.save_button.setIcon(save_normal)
        self.save_button.setIconSize(QSize(*self.scale_icon(155, 155)))
        self.save_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
        """)
        self.save_button.setGeometry(*self.scale_rect(1730, 875, 155, 155))
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

        if usage_data.get("Tanggal_Terpakai"):
            self.date_used_edit.setDate(
                QDate.fromString(usage_data["Tanggal_Terpakai"], "yyyy-MM-dd")
            )

        self.amount_used_spin.setValue(usage_data.get("Jumlah_Terpakai", 1))
        self.user_edit.setText(usage_data.get("User", ""))
        self.supporting_materials_edit.setText(usage_data.get("Bahan_Pendukung", ""))

        # self.current_stock_label.setText(f"Current Stock: {current_stock}")
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
