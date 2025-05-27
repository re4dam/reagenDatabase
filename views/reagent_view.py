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
    QFileDialog,
    QStyledItemDelegate,
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal, QSize, QRectF
from PyQt6.QtGui import QPixmap, QImage, QIcon, QPainter, QPainterPath

from load_font import FontManager
from app_context import AppContext
from viewmodels.reagent_viewmodel import ReagentViewModel
import io


class ReagentDetailPanel(QWidget):
    """
    View component responsible for displaying and interacting with reagent data.
    """

    back_to_rack_view = pyqtSignal()
    refresh_requested = pyqtSignal()
    delegate = QStyledItemDelegate()

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
        screen_size = AppContext.get_screen_resolution()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create container widget for layering
        container = QWidget()
        container.setGeometry(0, 0, screen_size.width(), screen_size.height())
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        # Background layer - Lab image
        background_label = QLabel(container)
        background_label.setPixmap(
            QPixmap("assets/ReagenView/background.png")
        )  # Use your actual image path
        background_label.setScaledContents(True)
        background_label.setGeometry(0, 0, screen_size.width(), screen_size.height())

        # Add circular back button in top-left corner
        self.back_button = QPushButton(container)
        back_normal = QIcon("assets/Rack/icon_back.png")
        back_hover = QIcon("assets/Rack/back_hover.png")
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
        self.back_button.leaveEvent = lambda event: self.back_button.setIcon(
            back_normal
        )
        self.back_button.clicked.connect(self._go_back)
        self.back_button.raise_()

        # Foreground layer
        panel_label = QLabel(container)
        panel_label.setPixmap(QPixmap("assets/ReagenView/foreground.png"))
        panel_label.setScaledContents(True)
        panel_label.setGeometry(*self.scale_rect(87, 160, 1742, 861))
        panel_label.raise_()

        # Label layer
        label_layer = QLabel(container)
        label_layer.setPixmap(QPixmap("assets/ReagenView/Label.png"))
        label_layer.setScaledContents(True)
        label_layer.setGeometry(*self.scale_rect(125, 200, 1072, 537))
        label_layer.raise_()

        # Name field
        self.name_edit = QLineEdit(container)
        self.name_edit.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(28))
        )
        self.name_edit.setGeometry(*self.scale_rect(122, 240, 506, 55))
        self.name_edit.raise_()

        # Tanggal_Pembelian field
        self.purchase_date_edit = QDateEdit(container)
        self.purchase_date_edit.setCalendarPopup(True)
        self.purchase_date_edit.setDate(QDate.currentDate())  # Default today
        calendar = self.purchase_date_edit.calendarWidget()
        calendar.setStyleSheet("""
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
        calendar.setFixedSize(300, 300)
        self.purchase_date_edit.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(28))
        )
        self.purchase_date_edit.setGeometry(*self.scale_rect(122, 355, 506, 60))
        self.purchase_date_edit.raise_()

        # Stock field
        self.stock_spin = QSpinBox(container)
        self.stock_spin.setRange(0, 10000)
        self.stock_spin.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(28))
        )
        self.stock_spin.setGeometry(*self.scale_rect(122, 461, 506, 60))
        self.stock_spin.raise_()

        # Massa field
        self.massa_spin = QSpinBox(container)
        self.massa_spin.setRange(0, 100000)
        self.massa_spin.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(28))
        )
        self.massa_spin.setGeometry(*self.scale_rect(122, 573, 506, 60))
        self.massa_spin.raise_()

        # Category_Hazard field
        self.hazard_combo = QComboBox(container)
        self.hazard_combo.addItems(["None", "Low", "Medium", "High", "Extreme"])
        self.hazard_combo.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(28))
        )
        self.hazard_combo.setGeometry(*self.scale_rect(124, 685, 506, 60))
        self.hazard_combo.raise_()

        # Wujud (form/state) field
        self.wujud_combo = QComboBox(container)
        self.wujud_combo.addItems(["Solid", "Liquid", "Gas", "Solution"])
        self.wujud_combo.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(28))
        )
        self.wujud_combo.setGeometry(*self.scale_rect(670, 235, 506, 60))
        self.set_combo_align_right(self.wujud_combo)
        self.wujud_combo.raise_()

        # Sifat field
        self.sifat_edit = QTextEdit(container)
        self.sifat_edit.setMaximumHeight(100)
        self.sifat_edit.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(28))
        )
        self.sifat_edit.setGeometry(*self.scale_rect(670, 360, 506, 60))
        self.sifat_edit.raise_()

        # Storage ID field - will be set based on the rack_name
        self.storage_id_label = QLabel(container)
        self.storage_id_label.setText(f"{self.view_model.rack_name}")
        tipe = self.view_model.rack_name
        if tipe == 1:
            self.storage_id_label.setText("Lemari Rak A")
        elif tipe == 2:
            self.storage_id_label.setText("Lemari Rak B")
        elif tipe == 3:
            self.storage_id_label.setText("Lemari Rak C")
        elif tipe == 4:
            self.storage_id_label.setText("Lemari Rak D")
        self.storage_id_label.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(28))
        )
        self.storage_id_label.setStyleSheet("color: black;")
        self.storage_id_label.setGeometry(*self.scale_rect(670, 475, 506, 60))
        self.storage_id_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.storage_id_label.raise_()

        # Tanggal_Expire field
        self.expire_date_edit = QDateEdit(container)
        self.expire_date_edit.setCalendarPopup(True)
        self.expire_date_edit.setDate(
            QDate.currentDate().addYears(1)
        )  # Default 1 year from now
        another_calendar = self.expire_date_edit.calendarWidget()
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
        self.expire_date_edit.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(28))
        )
        self.expire_date_edit.setGeometry(*self.scale_rect(670, 600, 506, 60))
        self.expire_date_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.expire_date_edit.raise_()

        # SDS field
        self.sds_status_label = QLabel(container)
        self.sds_status_label.setText("No SDS file")
        self.sds_status_label.setFont(
            FontManager.get_font("PlusJakartaSans-Italic", self.scale_style(20))
        )
        self.sds_status_label.setStyleSheet("color: #666;")
        self.sds_status_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.sds_status_label.setGeometry(*self.scale_rect(670, 725, 506, 60))
        self.sds_status_label.raise_()

        self.view_sds_button = QPushButton(container)
        self.view_sds_button.setText("View")
        self.view_sds_button.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(16))
        )
        self.view_sds_button.setGeometry(*self.scale_rect(930, 692, 65, 40))
        self.view_sds_button.clicked.connect(self._view_sds)
        self.view_sds_button.raise_()

        # SDS Upload/Clear buttons

        self.upload_sds_button = QPushButton(container)
        self.upload_sds_button.setText("Upload SDS")
        self.upload_sds_button.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(16))
        )
        self.upload_sds_button.setGeometry(*self.scale_rect(933, 773, 135, 40))
        self.upload_sds_button.clicked.connect(self._upload_sds)
        self.upload_sds_button.raise_()

        self.clear_sds_button = QPushButton(container)
        self.clear_sds_button.setText("Clear SDS")
        self.clear_sds_button.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(16))
        )
        self.clear_sds_button.setGeometry(*self.scale_rect(1068, 773, 110, 40))
        self.clear_sds_button.clicked.connect(self._clear_sds)
        self.clear_sds_button.raise_()

        # Image display (now bigger)
        self.image_label = QLabel(container)
        self.image_label.setMinimumSize(250, 250)  # Larger size for the image
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet(
            f"""border: 1px; border-radius: {self.scale_style(35)}px; solid #cccccc; background-color: #f9f9f9;"""
        )
        self.image_label.setText("No Image")
        self.image_label.setGeometry(*self.scale_rect(1202, 204, 586, 586))
        self.image_label.raise_()

        self.upload_image_button = QPushButton(container)
        self.upload_image_button.setText("Upload Image")
        self.upload_image_button.clicked.connect(self._upload_image)
        self.upload_image_button.setGeometry(*self.scale_rect(1202, 800, 293, 50))
        self.upload_image_button.raise_()

        self.clear_image_button = QPushButton(container)
        self.clear_image_button.setText("Clear Image")
        self.clear_image_button.clicked.connect(self._clear_image)
        self.clear_image_button.setGeometry(*self.scale_rect(1495, 800, 293, 50))
        self.clear_image_button.raise_()

        # Description field
        # self.description_edit = QTextEdit(container)
        # self.description_edit.setMaximumHeight(100)
        # self.description_edit.setFont(FontManager.get_font("PlusJakartaSans-Regular", 28))
        # self.description_edit.setGeometry(*self.scale_rect(670, 510, 506, 60))
        # self.description_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        # desc_cursor = self.description_edit.textCursor()
        # desc_cursor.select(desc_cursor.SelectionType.Document)
        # block_format = desc_cursor.blockFormat()
        # block_format.setAlignment(Qt.AlignmentFlag.AlignRight)
        # desc_cursor.setBlockFormat(block_format)
        # self.description_edit.setTextCursor(desc_cursor)
        # self.description_edit.raise_()

        # # Tanggal_Produksi field
        # self.prod_date_edit = QDateEdit()
        # self.prod_date_edit.setCalendarPopup(True)
        # self.prod_date_edit.setDate(QDate.currentDate())  # Default today
        # form_layout.addRow("Production Date:", self.prod_date_edit)

        # Edit button (only for existing reagents)
        if not self.view_model.is_new:
            self.edit_button = QPushButton(container)
            icon_normal = QIcon("assets/ReagenView/icon_edit.png")
            icon_hover = QIcon("assets/ReagenView/edit_hover.png")
            self.edit_button.setIcon(icon_normal)
            self.edit_button.setIconSize(QSize(*self.scale_icon(94, 94)))
            self.edit_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: transparent;
                }
            """)
            self.edit_button.setGeometry(*self.scale_rect(121, 900, 94, 94))
            self.edit_button.enterEvent = lambda event: self.edit_button.setIcon(
                icon_hover
            )
            self.edit_button.leaveEvent = lambda event: self.edit_button.setIcon(
                icon_normal
            )
            self.edit_button.clicked.connect(self._toggle_edit_mode)
            self.edit_button.raise_()

        # Save button
        self.save_button = QPushButton(container)
        save_normal = QIcon("assets/ReagenView/icon_save.png")
        save_hover = QIcon("assets/ReagenView/save_hover.png")
        self.save_button.setIcon(save_normal)
        self.save_button.setIconSize(QSize(*self.scale_icon(94, 94)))
        self.save_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        self.save_button.setGeometry(*self.scale_rect(121, 900, 94, 94))
        self.save_button.enterEvent = lambda event: self.save_button.setIcon(save_hover)
        self.save_button.leaveEvent = lambda event: self.save_button.setIcon(
            save_normal
        )
        self.save_button.clicked.connect(self._save_reagent)
        self.save_button.raise_()

        # Delete button (only for existing reagents)
        if not self.view_model.is_new:
            self.delete_button = QPushButton(container)
            delete_normal = QIcon("assets/ReagenView/icon_delete.png")
            delete_hover = QIcon("assets/ReagenView/delete_hover.png")
            self.delete_button.setIcon(delete_normal)
            self.delete_button.setIconSize(QSize(*self.scale_icon(94, 94)))
            self.delete_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: transparent;
                }
            """)
            self.delete_button.setGeometry(*self.scale_rect(241, 900, 94, 94))
            self.delete_button.enterEvent = lambda event: self.delete_button.setIcon(
                delete_hover
            )
            self.delete_button.leaveEvent = lambda event: self.delete_button.setIcon(
                delete_normal
            )
            self.delete_button.clicked.connect(self._delete_reagent)
            self.delete_button.raise_()

        # Usage Reports button (only for existing reagents)
        if not self.view_model.is_new:
            self.usage_button = QPushButton(container)
            usage_normal = QIcon("assets/ReagenView/icon_usage.png")
            usage_hover = QIcon("assets/ReagenView/icon_usage_hover.png")
            self.usage_button.setIcon(usage_normal)
            self.usage_button.setIconSize(QSize(*self.scale_icon(615, 109)))
            self.usage_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: transparent;
                }
            """)
            self.usage_button.setGeometry(*self.scale_rect(1187, 890, 615, 109))
            self.usage_button.enterEvent = lambda event: self.usage_button.setIcon(
                usage_hover
            )
            self.usage_button.leaveEvent = lambda event: self.usage_button.setIcon(
                usage_normal
            )
            self.usage_button.clicked.connect(self._show_usage_reports)
            self.usage_button.raise_()

        # Cancel button (only visible in edit mode)
        if not self.view_model.is_new:
            self.cancel_button = QPushButton(container)
            cancel_normal = QIcon("assets/ReagenView/icon_cancel.png")
            cancel_hover = QIcon("assets/ReagenView/cancel_hover.png")
            self.cancel_button.setIcon(cancel_normal)
            self.cancel_button.setIconSize(QSize(*self.scale_icon(94, 94)))
            self.cancel_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: transparent;
                }
            """)
            self.cancel_button.setGeometry(*self.scale_rect(361, 900, 94, 94))
            self.cancel_button.enterEvent = lambda event: self.cancel_button.setIcon(
                cancel_hover
            )
            self.cancel_button.leaveEvent = lambda event: self.cancel_button.setIcon(
                cancel_normal
            )
            self.cancel_button.clicked.connect(self._cancel_edit)
            self.cancel_button.raise_()

        main_layout.addWidget(container)

        # Create a list of all input widgets for easy access when toggling edit mode
        self.input_widgets = [
            self.name_edit,
            self.purchase_date_edit,
            self.stock_spin,
            self.massa_spin,
            self.hazard_combo,
            # self.description_edit,
            self.wujud_combo,
            self.sifat_edit,
            self.expire_date_edit,
            # self.prod_date_edit,
        ]

        # Current image data
        self.current_image_data = None

        # Current SDS data
        self.current_sds_data = None
        self.current_sds_filename = None

    def set_combo_align_right(self, combo: QComboBox):
        delegate = QStyledItemDelegate()

        def align_right_delegate(option, index):
            QStyledItemDelegate.initStyleOption(delegate, option, index)
            option.displayAlignment = Qt.AlignmentFlag.AlignRight

        delegate.initStyleOption = align_right_delegate
        combo.setItemDelegate(delegate)

        # Set alignment untuk tampilan utama
        combo.setEditable(True)
        line_edit = combo.lineEdit()
        line_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        line_edit.setReadOnly(True)  # Agar user tidak bisa mengetik

    def _load_reagent_data(self):
        """Load data for an existing reagent from the ViewModel"""
        reagent = self.view_model.get_reagent_data()

        if reagent:
            self.name_edit.setText(reagent.get("Name", ""))
            # self.description_edit.setText(reagent.get("Description", ""))

            if reagent.get("Tanggal_Pembelian"):
                self.purchase_date_edit.setDate(
                    QDate.fromString(reagent["Tanggal_Pembelian"], "yyyy-MM-dd")
                )

            self.stock_spin.setValue(reagent.get("Stock", 0))
            self.massa_spin.setValue(reagent.get("Massa", 0))

            # Set combobox value
            wujud_index = self.wujud_combo.findText(reagent.get("Wujud", ""))
            if wujud_index >= 0:
                self.wujud_combo.setCurrentIndex(wujud_index)

            # Set date values if available
            if reagent.get("Tanggal_Expire"):
                self.expire_date_edit.setDate(
                    QDate.fromString(reagent["Tanggal_Expire"], "yyyy-MM-dd")
                )
                self.expire_date_edit.setAlignment(Qt.AlignmentFlag.AlignRight)

            hazard_index = self.hazard_combo.findText(
                reagent.get("Category_Hazard", "")
            )
            if hazard_index >= 0:
                self.hazard_combo.setCurrentIndex(hazard_index)

            self.sifat_edit.setText(reagent.get("Sifat", ""))
            self.sifat_edit.setAlignment(Qt.AlignmentFlag.AlignRight)

            # if reagent.get("Tanggal_Produksi"):
            #     self.prod_date_edit.setDate(
            #         QDate.fromString(reagent["Tanggal_Produksi"], "yyyy-MM-dd")
            #     )

            # Load image if available
            self._load_image()

            # Load SDS if available
            self._load_sds()

    def _load_image(self):
        """Load image from ViewModel and display it"""
        try:
            image_data = self.view_model.get_image()
            if image_data:
                self.current_image_data = image_data
                image = QImage.fromData(image_data)
                if not image.isNull():
                    pixmap = QPixmap.fromImage(image)
                    pixmap = pixmap.scaled(
                        self.image_label.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    # Buat pixmap baru dengan rounded corner
                    rounded_pixmap = QPixmap(self.image_label.size())
                    rounded_pixmap.fill(Qt.GlobalColor.transparent)
                    painter = QPainter(rounded_pixmap)
                    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                    path = QPainterPath()
                    path.addRoundedRect(
                        QRectF(
                            0, 0, self.image_label.width(), self.image_label.height()
                        ),
                        30,
                        30,
                    )  # 30px radius lengkungan

                    painter.setClipPath(path)
                    painter.drawPixmap(0, 0, pixmap)
                    painter.end()

                    self.image_label.setPixmap(rounded_pixmap)
                    return

            # If no image or invalid image data
            self.image_label.setText("No Image")
            self.image_label.setPixmap(QPixmap())
            self.current_image_data = None

        except Exception as e:
            print(f"Error loading image: {str(e)}")
            self.image_label.setText("Error loading image")
            self.current_image_data = None

    def _load_sds(self):
        """Load SDS data from ViewModel and update UI accordingly"""
        try:
            sds_info = self.view_model.get_sds()
            if sds_info and sds_info.get("data"):
                self.current_sds_data = sds_info["data"]
                self.current_sds_filename = sds_info["filename"]

                # Update the SDS status label
                self.sds_status_label.setText(self.current_sds_filename)
                self.sds_status_label.setStyleSheet(
                    "font-style: italic; color: #0066cc;"
                )
                self.view_sds_button.setEnabled(True)
            else:
                # No SDS data available
                self.sds_status_label.setText("No SDS file")
                self.sds_status_label.setStyleSheet("font-style: italic; color: #666;")
                self.view_sds_button.setEnabled(False)
                self.current_sds_data = None
                self.current_sds_filename = None

        except Exception as e:
            print(f"Error loading SDS data: {str(e)}")
            self.sds_status_label.setText("Error loading SDS")
            self.sds_status_label.setStyleSheet("color: #cc0000;")
            self.view_sds_button.setEnabled(False)
            self.current_sds_data = None
            self.current_sds_filename = None

    def _upload_image(self):
        """Open file dialog to select an image"""
        if not self.view_model.edit_mode and not self.view_model.is_new:
            QMessageBox.warning(
                self, "Warning", "Please enter edit mode to change the image."
            )
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)",
        )

        if file_path:
            try:
                with open(file_path, "rb") as file:
                    image_data = file.read()

                # Store image data and update display
                self.current_image_data = image_data

                # Update in viewmodel
                result, message = self.view_model.update_image(image_data)

                # Update the UI
                self._load_image()

                if not result:
                    QMessageBox.warning(self, "Warning", message)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")

    def _clear_image(self):
        """Clear the current image"""
        if not self.view_model.edit_mode and not self.view_model.is_new:
            QMessageBox.warning(
                self, "Warning", "Please enter edit mode to clear the image."
            )
            return

        self.current_image_data = None
        self.image_label.setText("No Image")
        self.image_label.setPixmap(QPixmap())

        # Update in viewmodel
        self.view_model.update_image(None)

    def _upload_sds(self):
        """Open file dialog to select a PDF file for SDS"""
        if not self.view_model.edit_mode and not self.view_model.is_new:
            QMessageBox.warning(
                self, "Warning", "Please enter edit mode to change the SDS file."
            )
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Safety Data Sheet (PDF)",
            "",
            "PDF Files (*.pdf);;All Files (*)",
        )

        if file_path:
            try:
                with open(file_path, "rb") as file:
                    sds_data = file.read()

                # Get the filename from the path
                import os

                sds_filename = os.path.basename(file_path)

                # Store SDS data
                self.current_sds_data = sds_data
                self.current_sds_filename = sds_filename

                # Update in viewmodel
                result, message = self.view_model.update_sds(sds_data, sds_filename)

                # Update the UI
                if result:
                    self.sds_status_label.setText(sds_filename)
                    self.sds_status_label.setStyleSheet(
                        "font-weight: bold; color: #0066cc;"
                    )
                    self.view_sds_button.setEnabled(True)
                else:
                    QMessageBox.warning(self, "Warning", message)

            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to load SDS file: {str(e)}"
                )

    def _clear_sds(self):
        """Clear the current SDS file"""
        if not self.view_model.edit_mode and not self.view_model.is_new:
            QMessageBox.warning(
                self, "Warning", "Please enter edit mode to clear the SDS file."
            )
            return

        # Confirm with user
        confirm = QMessageBox.question(
            self,
            "Confirm Clear SDS",
            "Are you sure you want to remove the Safety Data Sheet?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if confirm == QMessageBox.StandardButton.Yes:
            # Clear SDS data
            self.current_sds_data = None
            self.current_sds_filename = None

            # Update the UI
            self.sds_status_label.setText("No SDS file")
            self.sds_status_label.setStyleSheet("font-style: italic; color: #666;")
            self.view_sds_button.setEnabled(False)

            # Update in viewmodel
            result, message = self.view_model.clear_sds()

            if not result:
                QMessageBox.warning(self, "Warning", message)

    def _view_sds(self):
        """View the SDS file using system's default PDF viewer"""
        if not self.current_sds_data:
            QMessageBox.information(
                self, "Information", "No SDS file available for this reagent."
            )
            return

        try:
            # Create a temporary file to view the PDF
            import tempfile
            import os
            import subprocess
            import platform

            # Create a temp file with the correct extension
            fd, temp_path = tempfile.mkstemp(suffix=".pdf")
            os.close(fd)

            # Write the PDF data to the temp file
            with open(temp_path, "wb") as f:
                f.write(self.current_sds_data)

            # Open the PDF with the default system viewer
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["open", temp_path], check=True)
            elif platform.system() == "Windows":
                os.startfile(temp_path)
            else:  # Linux and other Unix-like
                subprocess.run(["xdg-open", temp_path], check=True)

            # Note: The temp file will remain until the application exits or the OS cleans it up

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open SDS file: {str(e)}")

    def _toggle_edit_mode(self):
        """Toggle between view and edit modes"""
        self.view_model.toggle_edit_mode()
        self._set_edit_state(self.view_model.edit_mode)

        # # Update title based on mode
        # if self.view_model.edit_mode:
        #     self.title_label.setText("Edit Reagent Details")
        # else:
        #     self.title_label.setText("Reagent Details")

    def _set_edit_state(self, editable):
        """Set the edit state of all input widgets"""
        for widget in self.input_widgets:
            if isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
                widget.setReadOnly(not editable)
                # Apply style to indicate read-only state
                if not editable:
                    widget.setStyleSheet(
                        "border: none; background: transparent; color: #000000"
                    )
                else:
                    widget.setStyleSheet(
                        "border: none; background: rgba(0, 0, 0, 25); color: #000000"
                    )
            elif isinstance(widget, QSpinBox):
                widget.setEnabled(editable)
                if not editable:
                    widget.setStyleSheet("""
                        QSpinBox {
                            border: none;
                            background: transparent;
                            color: #000000
                        }
                        QAbstractSpinBox::up-button, QAbstractSpinBox::down-button {
                            width: 0px;
                            height: 0px;
                            border: none;
                        }
                    """)
                else:
                    widget.setStyleSheet(
                        "border: none; background: rgba(0, 0, 0, 25); color: #000000"
                    )
            elif isinstance(widget, QDateEdit):
                widget.setEnabled(editable)
                if not editable:
                    widget.setStyleSheet("""
                        QDateEdit {
                            border: none; 
                            background: transparent; 
                            color: #000000
                        }
                        QDateEdit::drop-down {
                            subcontrol-origin: padding;
                            subcontrol-position: top right;
                            width: 0px;
                        }
                        QDateEdit::down-arrow {
                            width: 0px;
                            height: 0px;
                        }
                    """)
                else:
                    widget.setStyleSheet("""
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
            elif isinstance(widget, QComboBox):
                widget.setEnabled(editable)
                if not editable:
                    widget.setStyleSheet("""
                        QComboBox {
                        border: none;
                        background: transparent;
                        color: #000000;
                        }
                        QComboBox::drop-down {
                            subcontrol-origin: padding;
                            subcontrol-position: top right;
                            width: 0px;
                        }
                        QComboBox::down-arrow {
                            width: 0px;
                            height: 0px;
                        }
                    """)
                else:
                    widget.setStyleSheet("""
                        QComboBox {
                            border: none;
                            background: rgba(0, 0, 0, 25);
                            color: #000000;
                        }
                        QComboBox QAbstractItemView {
                            background-color: white;
                            color: black;
                            selection-background-color: #0078d7;
                            selection-color: white;
                        }
                        QComboBox::drop-down {
                            subcontrol-origin: padding;
                            subcontrol-position: top right;
                            width: 20px;
                        }
                        QComboBox::down-arrow {
                            width: 20px;
                            height: 20px;
                        }
                    """)
        # Set image controls edit state
        self.upload_image_button.setEnabled(editable)
        self.clear_image_button.setEnabled(editable)

        # Set SDS controls edit state
        self.upload_sds_button.setEnabled(editable)
        self.clear_sds_button.setEnabled(editable)

        # Defensive checks for button visibility
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

    def _collect_form_data(self):
        """Collect the form data from UI elements"""
        form_data = {
            "Name": self.name_edit.text(),
            # "Description": self.description_edit.toPlainText(),
            "Wujud": self.wujud_combo.currentText(),
            "Stock": self.stock_spin.value(),
            "Massa": self.massa_spin.value(),
            "Tanggal_Expire": self.expire_date_edit.date().toString("yyyy-MM-dd"),
            "Category_Hazard": self.hazard_combo.currentText(),
            "Sifat": self.sifat_edit.toPlainText(),
            # "Tanggal_Produksi": self.prod_date_edit.date().toString("yyyy-MM-dd"),
            "Tanggal_Pembelian": self.purchase_date_edit.date().toString("yyyy-MM-dd"),
        }

        # Add image data if available
        if self.current_image_data is not None:
            form_data["Image"] = self.current_image_data

        # Add SDS data if available
        if self.current_sds_data is not None:
            form_data["SDS"] = self.current_sds_data
            form_data["SDS_Filename"] = self.current_sds_filename

        return form_data

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

    def resizeEvent(self, event):
        """Handle resize events to scale the image properly"""
        super().resizeEvent(event)
        if (
            hasattr(self, "image_label")
            and self.current_image_data
            and self.image_label.pixmap()
        ):
            # Reload and rescale the image
            image = QImage.fromData(self.current_image_data)
            if not image.isNull():
                pixmap = QPixmap.fromImage(image)
                pixmap = pixmap.scaled(
                    self.image_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                # Buat pixmap baru dengan rounded corner
                rounded_pixmap = QPixmap(self.image_label.size())
                rounded_pixmap.fill(Qt.GlobalColor.transparent)
                painter = QPainter(rounded_pixmap)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                path = QPainterPath()
                path.addRoundedRect(
                    QRectF(0, 0, self.image_label.width(), self.image_label.height()),
                    self.scale_style(30),
                    self.scale_style(30),
                )  # 30px radius lengkungan

                painter.setClipPath(path)
                painter.drawPixmap(0, 0, pixmap)
                painter.end()

                self.image_label.setPixmap(rounded_pixmap)
