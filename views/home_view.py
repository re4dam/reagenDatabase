# Updated views/home_view.py with About button and dialog, plus UserProfileDialog
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QMessageBox,
    QStackedWidget,
    QLineEdit,
    QComboBox,
    QDialog,
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont


class UserProfileDialog(QDialog):
    """Dialog to display user profile information"""

    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.setWindowTitle("User Profile")
        self.setFixedSize(400, 350)
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
        title_label = QLabel("USER PROFILE")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        layout.addSpacing(20)

        # Container for user data
        user_data_layout = QVBoxLayout()
        user_data_layout.setSpacing(10)
        user_data_layout.setContentsMargins(20, 0, 20, 0)

        # Create a frame to hold the user data
        user_data_frame = QFrame()
        user_data_frame.setFrameShape(QFrame.Shape.StyledPanel)
        user_data_frame.setStyleSheet(
            "QFrame { background-color: #ffffff; border-radius: 8px; padding: 10px; border: 1px solid #dddddd; }"
        )
        user_data_frame.setLayout(user_data_layout)

        # Username (if user_data is provided)
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        username_label.setFont(QFont("", 12, QFont.Weight.Bold))
        username_value = QLabel(
            user_data.get("username", "N/A") if user_data else "N/A"
        )
        username_value.setFont(QFont("", 12))
        username_layout.addWidget(username_label)
        username_layout.addWidget(username_value, 1)
        user_data_layout.addLayout(username_layout)

        # Add a divider line
        divider1 = QFrame()
        divider1.setFrameShape(QFrame.Shape.HLine)
        divider1.setFrameShadow(QFrame.Shadow.Sunken)
        divider1.setStyleSheet("background-color: #dddddd;")
        user_data_layout.addWidget(divider1)

        # First Name
        first_name_layout = QHBoxLayout()
        first_name_label = QLabel("First Name:")
        first_name_label.setFont(QFont("", 12, QFont.Weight.Bold))
        first_name_value = QLabel(
            user_data.get("first_name", "N/A") if user_data else "N/A"
        )
        first_name_value.setFont(QFont("", 12))
        first_name_layout.addWidget(first_name_label)
        first_name_layout.addWidget(first_name_value, 1)
        user_data_layout.addLayout(first_name_layout)

        # Add a divider line
        divider2 = QFrame()
        divider2.setFrameShape(QFrame.Shape.HLine)
        divider2.setFrameShadow(QFrame.Shadow.Sunken)
        divider2.setStyleSheet("background-color: #dddddd;")
        user_data_layout.addWidget(divider2)

        # Last Name
        last_name_layout = QHBoxLayout()
        last_name_label = QLabel("Last Name:")
        last_name_label.setFont(QFont("", 12, QFont.Weight.Bold))
        last_name_value = QLabel(
            user_data.get("last_name", "N/A") if user_data else "N/A"
        )
        last_name_value.setFont(QFont("", 12))
        last_name_layout.addWidget(last_name_label)
        last_name_layout.addWidget(last_name_value, 1)
        user_data_layout.addLayout(last_name_layout)

        layout.addWidget(user_data_frame)

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

    def set_user_data(self, user_data):
        """Set the current user's data"""
        self.current_user = user_data

    def _setup_main_ui(self):
        """Set up the UI components for the home page"""
        main_layout = QVBoxLayout(self.main_view)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Header layout with title, User Profile button, and About button
        header_layout = QHBoxLayout()

        # Title container
        title_container = QVBoxLayout()

        # Title
        title_label = QLabel("Sistem Manajemen Reagen Laboratorium")
        title_font = QLabel().font()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_container.addWidget(title_label)

        # Next Title
        next_title_label = QLabel(
            "Departemen Biokimia Fakultas Kedokteran Universitas Indonesia"
        )
        next_title_font = QLabel().font()
        next_title_font.setPointSize(20)
        next_title_font.setBold(True)
        next_title_label.setFont(title_font)
        next_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_container.addWidget(next_title_label)

        header_layout.addLayout(title_container, 7)

        # Buttons container (for User Profile and About)
        buttons_container = QVBoxLayout()
        buttons_container.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop
        )
        buttons_container.setSpacing(10)

        # User Profile button
        self.user_profile_button = QPushButton("User Profile")
        self.user_profile_button.setFixedSize(100, 40)
        self.user_profile_button.setStyleSheet(
            "QPushButton { background-color: #ccffee; border: 2px solid #99ddcc; "
            "border-radius: 5px; font-weight: bold; }"
            "QPushButton:hover { background-color: #aaeedd; }"
        )
        self.user_profile_button.clicked.connect(self._show_user_profile_dialog)
        buttons_container.addWidget(self.user_profile_button)

        # About button
        self.about_button = QPushButton("About")
        self.about_button.setFixedSize(100, 40)
        self.about_button.setStyleSheet(
            "QPushButton { background-color: #dddddd; border: 2px solid #bbbbbb; "
            "border-radius: 5px; font-weight: bold; }"
            "QPushButton:hover { background-color: #cccccc; }"
        )
        self.about_button.clicked.connect(self._show_about_dialog)
        buttons_container.addWidget(self.about_button)

        buttons_container.addStretch()

        header_layout.addLayout(buttons_container, 1)

        main_layout.addLayout(header_layout)

        # Add a divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(divider)
        main_layout.addSpacing(20)

        # Search bar section
        search_label = QLabel("Search Reagents:")
        search_font = QLabel().font()
        search_font.setPointSize(12)
        search_label.setFont(search_font)
        main_layout.addWidget(search_label)

        # Search bar layout
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)

        # Search input field
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_input.setMinimumHeight(40)
        self.search_input.returnPressed.connect(self._perform_search)
        search_layout.addWidget(self.search_input, 3)

        # Search by field dropdown
        self.search_field = QComboBox()
        self.search_field.setMinimumHeight(40)
        self.search_field.addItems(
            ["All Fields", "Name", "Description", "Wujud", "Category_Hazard", "Sifat"]
        )
        search_layout.addWidget(self.search_field, 1)

        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.setMinimumHeight(40)
        self.search_button.setStyleSheet(
            "QPushButton { background-color: #e6ccff; border: 2px solid #cc99ff; border-radius: 8px; }"
            "QPushButton:hover { background-color: #d9b3ff; }"
        )
        self.search_button.clicked.connect(self._perform_search)
        search_layout.addWidget(self.search_button)

        main_layout.addLayout(search_layout)
        main_layout.addSpacing(20)

        # Storage/Rack label
        rack_label = QLabel("Reagent Storage:")
        rack_label.setFont(search_font)
        main_layout.addWidget(rack_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Storage/rack buttons in grid layout
        self.rack_layout = QGridLayout()
        self.rack_layout.setSpacing(15)
        main_layout.addLayout(self.rack_layout)

        # The storage buttons will be added when data is loaded

        main_layout.addSpacing(40)

        # Bottom buttons container
        bottom_buttons_layout = QHBoxLayout()
        bottom_buttons_layout.setSpacing(20)
        bottom_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Refresh button
        self.refresh_button = QPushButton("Refresh Storage")
        self.refresh_button.setMinimumHeight(40)
        self.refresh_button.setMinimumWidth(120)
        self.refresh_button.setStyleSheet(
            "QPushButton { background-color: #ccffcc; border: 2px solid #99cc99; border-radius: 5px; }"
            "QPushButton:hover { background-color: #bbffbb; }"
        )
        self.refresh_button.clicked.connect(self._refresh_storage)
        bottom_buttons_layout.addWidget(self.refresh_button)

        # Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.setMinimumHeight(40)
        self.logout_button.setMinimumWidth(100)
        self.logout_button.setStyleSheet(
            "QPushButton { background-color: #ffeecc; border: 2px solid #eeddaa; border-radius: 5px; }"
            "QPushButton:hover { background-color: #ffddaa; }"
        )
        self.logout_button.clicked.connect(self._logout)
        bottom_buttons_layout.addWidget(self.logout_button)

        # Exit button
        self.exit_button = QPushButton("Exit")
        self.exit_button.setMinimumHeight(40)
        self.exit_button.setMinimumWidth(100)
        self.exit_button.clicked.connect(lambda: self.parent_window.close())
        bottom_buttons_layout.addWidget(self.exit_button)

        main_layout.addLayout(bottom_buttons_layout)

    def _show_user_profile_dialog(self):
        """Show the User Profile dialog"""
        print("testing satu")
        if self.home_viewmodel:
            # Fetch current user data if needed
            if not self.current_user and self.home_viewmodel.user_model:
                # You might need to implement this method in home_viewmodel
                # This would get the current logged-in user's data
                print("proses mencoba mengambil current user")
                self.current_user = self.home_viewmodel.get_current_user()

        # print("ternyata langsung kesini cuy")
        user_profile_dialog = UserProfileDialog(self, self.current_user)
        user_profile_dialog.exec()

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
            row = i // 2
            col = i % 2

            storage_name = storage.get("Name", f"Storage {i + 1}")
            storage_id = storage.get("id")

            rack_button = QPushButton(storage_name)
            rack_button.setMinimumHeight(80)
            rack_button.setMinimumWidth(250)

            # Set a distinct style for rack buttons
            rack_button.setStyleSheet(
                "QPushButton { background-color: #ddeeff; border: 2px solid #bbccee; border-radius: 8px; font-size: 14px; font-weight: bold; }"
                "QPushButton:hover { background-color: #cce4ff; }"
            )

            # Create a custom slot function for each button
            def create_slot_function(s_id, s_name):
                def slot_function():
                    self._show_rack(s_id, s_name)

                return slot_function

            # Connect button to show the storage/rack using a proper closure
            rack_button.clicked.connect(create_slot_function(storage_id, storage_name))

            self.rack_layout.addWidget(rack_button, row, col)
            self.rack_buttons.append(rack_button)

        # If no storage found, show a message
        if not self.storage_data:
            no_storage_label = QLabel(
                "No storage locations found. Please add storage in the database."
            )
            no_storage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.rack_layout.addWidget(no_storage_label, 0, 0, 1, 2)
