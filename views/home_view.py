# Updated views/home_view.py with search bar instead of button
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QMessageBox,
    QStackedWidget,
    QLineEdit,
    QComboBox,
    QSizePolicy,
    QGraphicsOpacityEffect,
)
from PyQt6.QtCore import Qt, pyqtSlot, QSize
from PyQt6.QtGui import QPixmap, QIcon
from app_context import AppContext
from load_font import FontManager

class HomeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.home_viewmodel = None
        self.storage_data = []
        self.rack_buttons = []
        self.rack_views = {}

        # Create stacked widget for views
        self.stacked_widget = QStackedWidget(self)

        # Create main view
        self.main_view = QWidget()
        self._setup_main_ui()

        # Add main view to stacked widget
        self.stacked_widget.addWidget(self.main_view)

        # Initialize other views as None
        self.record_view = None
        self.user_view = None
        self.usage_report_view = None

        # Set up main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.stacked_widget)

    def set_viewmodel(self, viewmodel):
        """Set the ViewModel for this view"""
        self.home_viewmodel = viewmodel

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
    
    def _setup_main_ui(self):
        self.screen_size = AppContext.get_screen_resolution()
        self.opacity = QGraphicsOpacityEffect()
        """Set up the UI components for the home page"""
        # Main Content
        self.main_layer = QWidget(self.main_view)
        self.main_layer.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        self.main_layer_layout = QVBoxLayout(self.main_layer)
        self.main_layer_layout.setContentsMargins(0, 0, 0, 0)

        background_label = QLabel(self.main_layer)
        background_label.setPixmap(QPixmap("assets/Home/Dashboard.png"))
        background_label.setScaledContents(True)
        background_label.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        background_label.lower()

        # Rack Layout
        self.rack_main = QWidget(self.main_layer)
        self.rack_layout = QHBoxLayout(self.rack_main)
        self.rack_layout.setSpacing(40)
        self.rack_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layer_layout.addWidget(self.rack_main)

        self.background_search = QLabel(self.main_layer)
        self.background_search.setPixmap(QPixmap("assets/Home/bg_blur.png"))
        self.background_search.setScaledContents(True)
        self.background_search.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        self.background_search.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.background_search_opacity = QGraphicsOpacityEffect()
        self.background_search_opacity.setOpacity(0.0)
        self.background_search.setGraphicsEffect(self.background_search_opacity)

        # Background Blur (search)
        self.bg_blur = QPushButton(self.main_layer)
        self.bg_blur.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.bg_blur.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        self.bg_blur.setGeometry(*self.scale_rect(0, 0, 1920, 1080))
        self.bg_blur_opacity = QGraphicsOpacityEffect()
        self.bg_blur_opacity.setOpacity(0.0)
        self.bg_blur.setGraphicsEffect(self.bg_blur_opacity)
        self.bg_blur.clicked.connect(self._exit_search)

        # Search bar section
        self.top_search = QPushButton(self.main_layer)
        icon_normal = QIcon("assets/Home/top_bar.png")
        self.top_search.setIcon(icon_normal)
        self.top_search.setIconSize(QSize(*self.scale_icon(814, 19)))  # Ukuran ikon/gambar
        self.top_search.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        self.top_search.setGeometry(*self.scale_rect(557, 17, 814, 19))
        self.top_search.clicked.connect(self._search_appear)

        # Search input background
        self.bg_search_input = QLabel(self.main_layer)
        self.bg_search_input.setPixmap(QPixmap("assets/Home/search_bar.png"))
        self.bg_search_input.setScaledContents(True)
        self.bg_search_input.setStyleSheet("border: none;")
        self.bg_search_input.setGeometry(*self.scale_rect(0, -94, 1920, 94))

        # Search input field
        self.search_input = QLineEdit(self.main_layer)
        self.search_input.setFont(FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(28)))
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_input.setStyleSheet(f"""color: black; padding-left: {self.scale_style(20)}px; border: none; background: transparent;""")
        self.search_input.returnPressed.connect(self._perform_search)
        self.search_input.setGeometry(*self.scale_rect(0, -94, 1615, 94))

        # Search by field dropdown
        self.search_field = QComboBox(self.main_layer)
        self.search_field.setFont(FontManager.get_font("PlusJakartaSans-Regular", 16))
        self.search_field.addItems(
            ["All Fields", "Name", "Description", "Wujud", "Category_Hazard", "Sifat"]
        )
        self.search_field.setStyleSheet("""
            QComboBox {
                color: black;
                border: none;
                background: transparent;
            }
            QComboBox QAbstractItemView {
                outline: none;
                border: none;
                background-color: white;
                color: black;
                selection-background-color: #2d2d2d;
                selection-color: white;
            }
            QComboBox QAbstractItemView::item:hover {
                padding-left: 5px;
                outline: none;
                border: none;
                background-color: #2d2d2d;
                color: white;
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
        self.search_field.setGeometry(*self.scale_rect(1629, -94, 200, 94))

        # Search button
        self.search_button = QPushButton(self.main_layer)
        search = QIcon("assets/Home/search_icon.png")
        self.search_button.setIcon(search)
        self.search_button.setIconSize(QSize(*self.scale_icon(65, 65)))
        self.search_button.setStyleSheet(
            "border: none; background: transparent;"
        )
        self.search_button.clicked.connect(self._perform_search)
        self.search_button.setGeometry(*self.scale_rect(1829, -79, 65, 65))

        self.background_search2 = QLabel(self.main_layer)
        self.background_search2.setPixmap(QPixmap("assets/Home/bg_blur.png"))
        self.background_search2.setScaledContents(True)
        self.background_search2.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        self.background_search2.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.background_search2_opacity = QGraphicsOpacityEffect()
        self.background_search2_opacity.setOpacity(0.0)
        self.background_search2.setGraphicsEffect(self.background_search2_opacity)

        # Background Blur (search)
        self.bg_blur2 = QPushButton(self.main_layer)
        self.bg_blur2.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.bg_blur2.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        self.bg_blur2.setGeometry(*self.scale_rect(0, 0, 1920, 1080))
        self.bg_blur2_opacity = QGraphicsOpacityEffect()
        self.bg_blur2_opacity.setOpacity(0.0)
        self.bg_blur2.setGraphicsEffect(self.bg_blur2_opacity)
        self.bg_blur2.clicked.connect(self._exit_sidebar)

        # Sidebar
        self.sidebar = QPushButton(self.main_layer)
        icon_sidebar = QIcon("assets/Home/side_bar.png")
        self.sidebar.setIcon(icon_sidebar)
        self.sidebar.setIconSize(QSize(*self.scale_icon(17, 708)))  # Ukuran ikon/gambar
        self.sidebar.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        self.sidebar.setGeometry(*self.scale_rect(1890, 200, 17, 708))
        self.sidebar_opacity = QGraphicsOpacityEffect()
        self.sidebar_opacity.setOpacity(1.0)
        self.sidebar.setGraphicsEffect(self.sidebar_opacity)
        self.sidebar.clicked.connect(self._sidebar_appear)

        # Sidebar background
        self.profilebar = QLabel(self.main_layer)
        self.profilebar.setPixmap(QPixmap("assets/Home/profile_bar.png"))
        self.profilebar.setScaledContents(True)
        self.profilebar.setStyleSheet("border: none;")
        self.profilebar.setGeometry(*self.scale_rect(2426, 0, 506, 1080))

        # # Bottom buttons container
        # bottom_buttons_layout = QHBoxLayout()
        # bottom_buttons_layout.setSpacing(20)
        # bottom_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # # Refresh button
        # self.refresh_button = QPushButton("Refresh Storage")
        # self.refresh_button.setMinimumHeight(40)
        # self.refresh_button.setMinimumWidth(120)
        # self.refresh_button.setStyleSheet(
        #     "QPushButton { background-color: #ccffcc; border: 2px solid #99cc99; border-radius: 5px; }"
        #     "QPushButton:hover { background-color: #bbffbb; }"
        # )
        # self.refresh_button.clicked.connect(self._refresh_storage)
        # bottom_buttons_layout.addWidget(self.refresh_button)

        # # Logout button
        # self.logout_button = QPushButton("Logout")
        # self.logout_button.setMinimumHeight(40)
        # self.logout_button.setMinimumWidth(100)
        # self.logout_button.setStyleSheet(
        #     "QPushButton { background-color: #ffeecc; border: 2px solid #eeddaa; border-radius: 5px; }"
        #     "QPushButton:hover { background-color: #ffddaa; }"
        # )
        # self.logout_button.clicked.connect(self._logout)
        # bottom_buttons_layout.addWidget(self.logout_button)

        # # Exit button
        # self.exit_button = QPushButton("Exit")
        # self.exit_button.setMinimumHeight(40)
        # self.exit_button.setMinimumWidth(100)
        # self.exit_button.clicked.connect(lambda: self.parent_window.close())
        # bottom_buttons_layout.addWidget(self.exit_button)

        # main_layout.addLayout(bottom_buttons_layout)
    def _search_appear(self):
        self.top_search.setGeometry(*self.scale_rect(557, 117, 814, 19))
        self.background_search_opacity.setOpacity(1.0)
        self.bg_blur_opacity.setOpacity(1.0)
        self.background_search.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.bg_blur.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.sidebar_opacity.setOpacity(0.0)
        self.sidebar.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.bg_search_input.setGeometry(*self.scale_rect(0, 0, 1920, 94))
        self.search_input.setGeometry(*self.scale_rect(0, 0, 1615, 94))
        self.search_field.setGeometry(*self.scale_rect(1629, 0, 200, 94))
        self.search_button.setGeometry(*self.scale_rect(1829, 14, 65, 65))

    def _exit_search(self):
        self.top_search.setGeometry(*self.scale_rect(557, 17, 814, 19))
        self.background_search_opacity.setOpacity(0.0)
        self.bg_blur_opacity.setOpacity(0.0)
        self.background_search.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.bg_blur.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.sidebar_opacity.setOpacity(1.0)
        self.sidebar.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.bg_search_input.setGeometry(*self.scale_rect(0, -94, 1920, 94))
        self.search_input.setGeometry(*self.scale_rect(0, -94, 1615, 94))
        self.search_field.setGeometry(*self.scale_rect(1629, -94, 200, 94))
        self.search_button.setGeometry(*self.scale_rect(1829, -79, 65, 65))
        self.search_input.clear()

    def _sidebar_appear(self):
        self.sidebar.setGeometry(*self.scale_rect(1380, 200, 17, 708))
        self.profilebar.setGeometry(*self.scale_rect(1414, 0, 506, 1080))
        self.bg_blur2_opacity.setOpacity(1.0)
        self.background_search2_opacity.setOpacity(1.0)
        self.background_search2.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.bg_blur2.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)

    def _exit_sidebar(self):
        self.sidebar.setGeometry(*self.scale_rect(1890, 200, 17, 708))
        self.profilebar.setGeometry(*self.scale_rect(2426, 0, 506, 1080))
        self.bg_blur2_opacity.setOpacity(0.0)
        self.background_search2_opacity.setOpacity(0.0)
        self.background_search2.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.bg_blur2.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

    def _perform_search(self):
        """Execute search based on current input"""
        if not self.home_viewmodel:
            return

        search_term = self.search_input.text().strip()
        search_field = self.search_field.currentText()

        # Don't search if term is too short (unless cleared)
        if len(search_term) < 2 and search_term != "":
            return

        # First show the search view
        self._show_search()

        # Then perform the search with the current terms
        if (
            hasattr(self.parent_window, "search_widget")
            and self.parent_window.search_widget
        ):
            search_view = self.parent_window.search_widget
            if hasattr(search_view, "search_input"):
                search_view.search_input.setText(search_term)
            if hasattr(search_view, "search_field"):
                index = search_view.search_field.findText(search_field)
                if index >= 0:
                    search_view.search_field.setCurrentIndex(index)

    def _show_search(self):
        """Show the search widget"""
        if self.home_viewmodel:
            self.home_viewmodel.show_search()

    def _show_rack(self, storage_id, storage_name):
        """Show a specific rack widget"""
        if self.home_viewmodel:
            self.home_viewmodel.show_rack(storage_id, storage_name)

    def show_home(self):
        """Switch back to the main home view"""
        self.stacked_widget.setCurrentWidget(self.main_view)

    def _view_reagent_details(self, reagent_id):
        """Show reagent details panel"""
        if self.home_viewmodel:
            self.home_viewmodel.view_reagent_details(reagent_id)

    def _refresh_storage(self):
        """Refresh the storage data"""
        if self.home_viewmodel:
            self.home_viewmodel.load_storage_data()
            self._update_storage_buttons()
            QMessageBox.information(
                self,
                "Storage Refreshed",
                "Storage locations have been refreshed from the database.",
            )

    def _logout(self):
        """Logout the current user"""
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes and self.home_viewmodel:
            self.home_viewmodel.logout()

    @pyqtSlot(list)
    def on_storage_data_loaded(self, storage_data):
        """Handle loaded storage data"""
        self.storage_data = storage_data
        self._update_storage_buttons()

    @pyqtSlot(str)
    def on_storage_error(self, error_message):
        """Handle storage loading error"""
        QMessageBox.warning(
            self,
            "Storage Error",
            error_message,
        )

    def search_hover_event(self, button):
        def on_enter(event):
            button.setGeometry(*self.scale_rect(557, 17, 814, 19))
        def on_leave(event):
            button.setGeometry(*self.scale_rect(557, 117, 814, 19))
        button.enterEvent = on_enter
        button.leaveEvent = on_leave

    def make_hover_event(self, button, normal_icon, hover_icon):
        def on_enter(event):
            button.setIcon(hover_icon)
        def on_leave(event):
            button.setIcon(normal_icon)
        button.enterEvent = on_enter
        button.leaveEvent = on_leave

    def _update_storage_buttons(self):
        """Update the storage buttons display"""
        # Clear existing buttons first
        for i in reversed(range(self.rack_layout.count())):
            widget = self.rack_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        self.rack_buttons = []

        # Create buttons for each storage location
        for i, storage in enumerate(self.storage_data):

            storage_name = storage.get("Name", f"Storage {i + 1}")
            storage_id = storage.get("id")

            rack_button = QPushButton()
            rack_image = QIcon(f"assets/Home/Lemari{i + 1}.png")
            rack_image_hover = QIcon(f"assets/Home/Lemari_hover{i + 1}.png")

            rack_button.setIcon(rack_image)
            rack_button.setIconSize(QSize(*self.scale_icon(381, 941)))
            rack_button.setFixedSize(*self.scale_icon(381, 941))
            rack_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            rack_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: transparent;
                }
            """)

            # Hover event binding
            self.make_hover_event(rack_button, rack_image, rack_image_hover)

            # Create a custom slot function for each button
            def create_slot_function(s_id, s_name):
                def slot_function():
                    self._show_rack(s_id, s_name)

                return slot_function

            # Connect button to show the storage/rack using a proper closure
            rack_button.clicked.connect(create_slot_function(storage_id, storage_name))
            self.rack_layout.addWidget(rack_button)
            self.rack_buttons.append(rack_button)

        # If no storage found, show a message
        if not self.storage_data:
            no_storage_label = QLabel(
                "No storage locations found. Please add storage in the database."
            )
            no_storage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.rack_layout.addWidget(no_storage_label, 0, 0, 1, 2)
