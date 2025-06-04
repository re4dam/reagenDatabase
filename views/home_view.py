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
    QFrame,
    QDialog,
)
from PyQt6.QtCore import Qt, pyqtSlot, QSize
from PyQt6.QtGui import QPixmap, QIcon, QFont
from app_context import AppContext
from load_font import FontManager

# class UserProfileDialog(QDialog):
#     """Dialog to display user profile information"""

#     def __init__(self, parent=None, user_data=None):
#         super().__init__(parent)
#         self.setWindowTitle("User Profile")
#         self.setFixedSize(400, 350)
#         self.setModal(True)

#         # Remove the ? from the title bar
#         self.setWindowFlags(
#             self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
#         )

#         # Main layout
#         layout = QVBoxLayout(self)
#         layout.setSpacing(15)
#         layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         # Background styling for the dialog
#         self.setStyleSheet("QDialog { background-color: #f0f0f0; }")

#         # Title
#         title_label = QLabel("USER PROFILE")
#         title_font = QFont()
#         title_font.setPointSize(18)
#         title_font.setBold(True)
#         title_label.setFont(title_font)
#         title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(title_label)

#         layout.addSpacing(20)

#         # Container for user data
#         user_data_layout = QVBoxLayout()
#         user_data_layout.setSpacing(10)
#         user_data_layout.setContentsMargins(20, 0, 20, 0)

#         # Create a frame to hold the user data
#         user_data_frame = QFrame()
#         user_data_frame.setFrameShape(QFrame.Shape.StyledPanel)
#         user_data_frame.setStyleSheet(
#             "QFrame { background-color: #ffffff; border-radius: 8px; padding: 10px; border: 1px solid #dddddd; }"
#         )
#         user_data_frame.setLayout(user_data_layout)

#         # Username (if user_data is provided)
#         username_layout = QHBoxLayout()
#         username_label = QLabel("Username:")
#         username_label.setFont(QFont("", 12, QFont.Weight.Bold))
#         username_value = QLabel(
#             user_data.get("username", "N/A") if user_data else "N/A"
#         )
#         username_value.setFont(QFont("", 12))
#         username_layout.addWidget(username_label)
#         username_layout.addWidget(username_value, 1)
#         user_data_layout.addLayout(username_layout)

#         # Add a divider line
#         divider1 = QFrame()
#         divider1.setFrameShape(QFrame.Shape.HLine)
#         divider1.setFrameShadow(QFrame.Shadow.Sunken)
#         divider1.setStyleSheet("background-color: #dddddd;")
#         user_data_layout.addWidget(divider1)

#         # First Name
#         first_name_layout = QHBoxLayout()
#         first_name_label = QLabel("First Name:")
#         first_name_label.setFont(QFont("", 12, QFont.Weight.Bold))
#         first_name_value = QLabel(
#             user_data.get("first_name", "N/A") if user_data else "N/A"
#         )
#         first_name_value.setFont(QFont("", 12))
#         first_name_layout.addWidget(first_name_label)
#         first_name_layout.addWidget(first_name_value, 1)
#         user_data_layout.addLayout(first_name_layout)

#         # Add a divider line
#         divider2 = QFrame()
#         divider2.setFrameShape(QFrame.Shape.HLine)
#         divider2.setFrameShadow(QFrame.Shadow.Sunken)
#         divider2.setStyleSheet("background-color: #dddddd;")
#         user_data_layout.addWidget(divider2)

#         # Last Name
#         last_name_layout = QHBoxLayout()
#         last_name_label = QLabel("Last Name:")
#         last_name_label.setFont(QFont("", 12, QFont.Weight.Bold))
#         last_name_value = QLabel(
#             user_data.get("last_name", "N/A") if user_data else "N/A"
#         )
#         last_name_value.setFont(QFont("", 12))
#         last_name_layout.addWidget(last_name_label)
#         last_name_layout.addWidget(last_name_value, 1)
#         user_data_layout.addLayout(last_name_layout)

#         layout.addWidget(user_data_frame)

#         layout.addSpacing(20)

#         # Close button
#         close_button = QPushButton("Close")
#         close_button.setFixedWidth(100)
#         close_button.clicked.connect(self.accept)
#         close_button.setStyleSheet(
#             "QPushButton { background-color: #e6e6e6; border: 1px solid #999999; border-radius: 5px; padding: 8px; }"
#             "QPushButton:hover { background-color: #d9d9d9; }"
#         )
#         layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)


class AboutDialog(QDialog):
    """Dialog to display About information"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setFixedSize(400, 300)
        self.setModal(True)

        # Remove the ? from the title bar
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )

        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Background styling for the dialog
        self.setStyleSheet("QDialog { background-color: #f0f0f0; }")

        # Title
        title_label = QLabel("ABOUT")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Version
        version_label = QLabel("MaSiLab V1.0")
        version_font = QFont()
        version_font.setPointSize(14)
        version_font.setBold(True)
        version_label.setFont(version_font)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        layout.addSpacing(10)

        # Credit line 1
        credit1_label = QLabel("Created by ILKOM UPI")
        credit1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(credit1_label)

        # Credit line 2
        credit2_label = QLabel("in collaboration with FKUI")
        credit2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(credit2_label)

        layout.addSpacing(20)

        # Icons credit
        icons_label = QLabel("Icons by Icons8")
        icons_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icons_label)

        layout.addSpacing(20)

        # Close button
        close_button = QPushButton("Close")
        close_button.setFixedWidth(100)
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet(
            "QPushButton { background-color: #e6e6e6; border: 1px solid #999999; border-radius: 5px; padding: 8px; }"
            "QPushButton:hover { background-color: #d9d9d9; }"
        )
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)


class HomeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.home_viewmodel = None
        self.storage_data = []
        self.rack_buttons = []
        self.rack_views = {}
        self.current_user = None

        # Intialize sidebar user info labels as instance attributes
        self.fullname_value_label = None
        self.username_value_label = None

        # Create stacked widget for views
        self.stacked_widget = QStackedWidget(self)

        # Create main view
        self.main_view = QWidget()

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
        self._setup_main_ui()  # Setup UI after viewmodel is set

        # Explicitly try to get user data when viewmodel is set,
        # especially if the view is being reused.
        if self.home_viewmodel and self.home_viewmodel.current_user_id:
            cached_user_data = self.home_viewmodel.get_current_user()
            if cached_user_data:  # If user data was already in ViewModel (e.g. cached)
                self.set_user_data(cached_user_data)
            # If not cached, get_current_user would have triggered load_current_user in VM,
            # which emits user_data_loaded, and set_user_data will be called.

    @pyqtSlot(dict)
    def set_user_data(self, user_data):
        """Set the current user's data and update the UI."""
        self.current_user = user_data  # Update HomeView's own record of the user
        self._update_sidebar_user_info()  # Refresh the sidebar labels

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
        self._get_user_profile()

        """Set up the UI components for the home page"""
        # Main Content
        self.main_layer = QWidget(self.main_view)
        self.main_layer.setGeometry(
            0, 0, self.screen_size.width(), self.screen_size.height()
        )
        self.main_layer_layout = QVBoxLayout(self.main_layer)
        self.main_layer_layout.setContentsMargins(0, 0, 0, 0)

        background_label = QLabel(self.main_layer)
        background_label.setPixmap(QPixmap("assets/Home/Dashboard.png"))
        background_label.setScaledContents(True)
        background_label.setGeometry(
            0, 0, self.screen_size.width(), self.screen_size.height()
        )
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
        self.background_search.setGeometry(
            0, 0, self.screen_size.width(), self.screen_size.height()
        )
        self.background_search.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents, True
        )
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
        self.top_search.setIconSize(
            QSize(*self.scale_icon(814, 19))
        )  # Ukuran ikon/gambar
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
        self.search_input.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(28))
        )
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_input.setStyleSheet(
            f"""color: black; padding-left: {self.scale_style(20)}px; border: none; background: transparent;"""
        )
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
        self.search_button.setStyleSheet("border: none; background: transparent;")
        self.search_button.clicked.connect(self._perform_search)
        self.search_button.setGeometry(*self.scale_rect(1829, -79, 65, 65))

        self.background_search2 = QLabel(self.main_layer)
        self.background_search2.setPixmap(QPixmap("assets/Home/bg_blur.png"))
        self.background_search2.setScaledContents(True)
        self.background_search2.setGeometry(
            0, 0, self.screen_size.width(), self.screen_size.height()
        )
        self.background_search2.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents, True
        )
        self.background_search2_opacity = QGraphicsOpacityEffect()
        self.background_search2_opacity.setOpacity(0.0)
        self.background_search2.setGraphicsEffect(self.background_search2_opacity)

        # Background Blur (search)
        self.bg_blur2 = QPushButton(self.main_layer)
        self.bg_blur2.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents, True
        )
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
        self.profilebar.setGeometry(*self.scale_rect(2426, 0, 506, 1055))

        # Sidebar Layout
        self.sidebar_widget = QWidget(self.main_layer)
        self.sidebar_widget.setGeometry(*self.scale_rect(2426, 0, 506, 1055))
        sidebar_layout = QVBoxLayout(self.sidebar_widget)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter
        )

        # Base Profile Picture
        profile_container = QWidget(self.sidebar_widget)
        profile_layout = QHBoxLayout(profile_container)
        profile_layout.setContentsMargins(0, 0, 0, 0)
        profile_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        base_profile = QLabel(profile_container)
        base_profile.setPixmap(QPixmap("assets/Home/base_profile.png"))
        base_profile.setScaledContents(True)
        base_profile.setFixedSize(*self.scale_icon(140, 140))
        profile_layout.addWidget(base_profile)
        sidebar_layout.addWidget(profile_container)

        # Fullname Label - now an instance attribute
        self.fullname_value_label = QLabel(self.sidebar_widget)
        self.fullname_value_label.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(45))
        )
        self.fullname_value_label.setFixedHeight(self.scale_style(94))
        self.fullname_value_label.setStyleSheet("color: black; font-weight: bold;")
        self.fullname_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(self.fullname_value_label)

        # Username Label - now an instance attribute
        self.username_value_label = QLabel(self.sidebar_widget)
        self.username_value_label.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(30))
        )
        self.username_value_label.setStyleSheet("color: black;")
        self.username_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(self.username_value_label)

        spacer = QLabel("")
        spacer.setFixedHeight(600)
        sidebar_layout.addWidget(spacer)

        # Base Profile Picture
        bottom_container = QWidget(self.sidebar_widget)
        bottom_layout = QVBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.about_button = QPushButton(bottom_container)
        self.about_button.setText("About")
        self.about_button.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(35))
        )
        self.about_button.setStyleSheet(
            "QPushButton { background: transparent; color: black; font-weight: bold; }"
            "QPushButton:hover { background: transparent; color: grey; font-weight: bold; }"
        )
        self.about_button.clicked.connect(self._show_about_dialog)
        bottom_layout.addWidget(self.about_button)

        # Logout button
        self.logout_button = QPushButton(bottom_container)
        self.logout_button.setText("Logout")
        self.logout_button.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(65))
        )
        self.logout_button.setStyleSheet(
            "QPushButton { background: transparent; color: red; font-weight: bold; }"
            "QPushButton:hover { background: transparent; color: black; font-weight: bold; }"
        )
        self.logout_button.clicked.connect(self._logout)
        bottom_layout.addWidget(self.logout_button)

        sidebar_layout.addWidget(bottom_container)

    def _update_sidebar_user_info(self):
        """Updates the sidebar user information labels with current_user data."""
        if (
            self.fullname_value_label and self.username_value_label
        ):  # Check if labels are created
            if self.current_user:
                self.fullname_value_label.setText(
                    f"{self.current_user.get('first_name', 'N/A')} {self.current_user.get('last_name', 'N/A')}"
                )
                self.username_value_label.setText(
                    self.current_user.get("username", "N/A")
                )
            else:
                self.fullname_value_label.setText("N/A N/A")
                self.username_value_label.setText("N/A")

    def _search_appear(self):
        self.top_search.setGeometry(*self.scale_rect(557, 117, 814, 19))
        self.background_search_opacity.setOpacity(1.0)
        self.bg_blur_opacity.setOpacity(1.0)
        self.background_search.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents, False
        )
        self.bg_blur.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents, False
        )
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
        self.background_search.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents, True
        )
        self.bg_blur.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.sidebar_opacity.setOpacity(1.0)
        self.sidebar.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents, False
        )
        self.bg_search_input.setGeometry(*self.scale_rect(0, -94, 1920, 94))
        self.search_input.setGeometry(*self.scale_rect(0, -94, 1615, 94))
        self.search_field.setGeometry(*self.scale_rect(1629, -94, 200, 94))
        self.search_button.setGeometry(*self.scale_rect(1829, -79, 65, 65))
        self.search_input.clear()

    def _sidebar_appear(self):
        self.sidebar.setGeometry(*self.scale_rect(1380, 200, 17, 708))
        self.profilebar.setGeometry(*self.scale_rect(1414, 0, 506, 1055))
        self.sidebar_widget.setGeometry(*self.scale_rect(1414, 0, 506, 1055))
        self.bg_blur2_opacity.setOpacity(1.0)
        self.background_search2_opacity.setOpacity(1.0)
        self.background_search2.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents, False
        )
        self.bg_blur2.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents, False
        )

    def _exit_sidebar(self):
        self.sidebar.setGeometry(*self.scale_rect(1890, 200, 17, 708))
        self.profilebar.setGeometry(*self.scale_rect(2426, 0, 506, 1055))
        self.sidebar_widget.setGeometry(*self.scale_rect(2426, 0, 506, 1055))
        self.bg_blur2_opacity.setOpacity(0.0)
        self.background_search2_opacity.setOpacity(0.0)
        self.background_search2.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents, True
        )
        self.bg_blur2.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents, True
        )

    def _get_user_profile(self):
        """
        Tries to populate self.current_user from the ViewModel.
        This is mainly for the initial setup of the view.
        Subsequent updates should come via the set_user_data slot.
        """
        # print("HomeView: _get_user_profile called") # For debugging
        if self.home_viewmodel and not self.current_user:
            # print("HomeView: current_user is None, attempting to fetch from viewmodel.") # For debugging
            # This call will trigger load_current_user in VM if data isn't cached,
            # which then emits user_data_loaded, calling self.set_user_data.
            # If data is cached, it's returned here directly.
            user_data_from_vm = self.home_viewmodel.get_current_user()
            if user_data_from_vm:  # If data was available from VM (cached or loaded synchronously by get_current_user)
                self.current_user = user_data_from_vm
            # print(f"HomeView: _get_user_profile - self.current_user is now {self.current_user}") # For debugging

    def _show_about_dialog(self):
        """Show the About dialog"""
        about_dialog = AboutDialog(self)
        about_dialog.exec()

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
            rack_button.setSizePolicy(
                QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
            )
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
