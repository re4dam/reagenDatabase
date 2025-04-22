# views/home_widget.py
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
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from views.record_window import RecordWidget
from views.user_window import UserWidget


class HomeWidget(QWidget):
    def __init__(self, record_model, user_model, parent=None):
        super().__init__(parent)
        self.record_model = record_model
        self.user_model = user_model
        self.parent_window = parent  # Reference to the parent window (LoginWindow)
        self.rack_widgets = [None, None, None, None]  # Initialize rack widgets list

        # Create a stacked widget to manage different views within the home widget
        self.stacked_widget = QStackedWidget(self)

        # Create the main home view widget
        self.main_view = QWidget()
        self._setup_main_ui()

        # Add main view to stacked widget
        self.stacked_widget.addWidget(self.main_view)

        # Initialize other widgets as None
        self.record_widget = None
        self.user_widget = None

        # Set up the main layout for HomeWidget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.stacked_widget)

    def _setup_main_ui(self):
        """Set up the UI components for the home page"""
        main_layout = QVBoxLayout(self.main_view)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title_label = QLabel("Sistem Manajemen Reagen Laboratorium")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Next Title
        next_title_label = QLabel(
            "Departemen Biokimia Fakultas Kedokteran Universitas Indonesia"
        )
        next_title_font = QFont()
        next_title_font.setPointSize(20)
        next_title_font.setBold(True)
        next_title_label.setFont(title_font)
        next_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(next_title_label)

        # Add a divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(divider)
        main_layout.addSpacing(20)

        # Subtitle for main modules
        modules_label = QLabel("Main Modules:")
        modules_font = QFont()
        modules_font.setPointSize(12)
        modules_label.setFont(modules_font)
        modules_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(modules_label)

        # Buttons for navigation
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        # Record Manager Button
        self.db_button = QPushButton("Record Manager")
        self.db_button.setMinimumHeight(60)
        self.db_button.setMinimumWidth(180)
        self.db_button.clicked.connect(self._show_record_manager)
        buttons_layout.addWidget(self.db_button)

        # User Management Button
        self.user_button = QPushButton("User Management")
        self.user_button.setMinimumHeight(60)
        self.user_button.setMinimumWidth(180)
        self.user_button.clicked.connect(self._show_user_management)
        buttons_layout.addWidget(self.user_button)

        main_layout.addLayout(buttons_layout)
        main_layout.addSpacing(30)

        # reagent rack buttons in grid layout
        rack_label = QLabel("Reagent Racks:")
        rack_label.setFont(modules_font)
        main_layout.addWidget(rack_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # reagent rack buttons in grid layout
        rack_layout = QGridLayout()
        rack_layout.setSpacing(15)

        # create/initiate 4 rack buttons in a 2 x 2 grid
        self.rack_buttons = []
        rack_names = ["Rack A", "Rack B", "Rack C", "Rack D"]

        for i in range(4):
            row = i // 2
            col = i % 2

            rack_button = QPushButton(rack_names[i])
            rack_button.setMinimumHeight(80)
            rack_button.setMinimumWidth(250)

            # Set a distinct style for rack buttons
            rack_button.setStyleSheet(
                "QPushButton { background-color: #ddeeff; border: 2px solid #bbccee; border-radius: 8px; font-size: 14px; font-weight: bold; }"
                "QPushButton:hover { background-color: #cce4ff; }"
            )

            rack_button.clicked.connect(lambda checked, index=i: self._show_rack(index))

            rack_layout.addWidget(rack_button, row, col)
            self.rack_buttons.append(rack_button)

        main_layout.addLayout(rack_layout)
        main_layout.addSpacing(40)

        # Bottom buttons container
        bottom_buttons_layout = QHBoxLayout()
        bottom_buttons_layout.setSpacing(20)
        bottom_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

    def _show_record_manager(self):
        """Show the record manager widget"""
        if not self.record_widget:
            self.record_widget = RecordWidget(self.record_model, self)
            self.stacked_widget.addWidget(self.record_widget)

        # Switch to record widget
        self.stacked_widget.setCurrentWidget(self.record_widget)

    def _show_user_management(self):
        """Show the user management widget"""
        if not self.user_widget:
            self.user_widget = UserWidget(self.user_model, self)
            self.stacked_widget.addWidget(self.user_widget)

        # Switch to user widget
        self.stacked_widget.setCurrentWidget(self.user_widget)

    def _show_rack(self, rack_index):
        """Show a specific reagent rack widget"""
        try:
            # This is where you would import your rack widget class
            from views.rack_window import RackWidget  # You'll need to create this

            if not self.rack_widgets[rack_index]:
                rack_name = f"Rack {chr(65 + rack_index)}"  # A, B, C, D
                self.rack_widgets[rack_index] = RackWidget(
                    self.record_model, rack_name, self
                )
                self.stacked_widget.addWidget(self.rack_widgets[rack_index])

            # Switch to rack widget
            self.stacked_widget.setCurrentWidget(self.rack_widgets[rack_index])

        except ImportError:
            # If the rack widget class isn't created yet, show a message
            QMessageBox.information(
                self,
                "Coming Soon",
                f"Rack {chr(65 + rack_index)} management widget is not yet implemented.",
            )

    def show_home(self):
        """Switch back to the main home view"""
        self.stacked_widget.setCurrentWidget(self.main_view)

    def _logout(self):
        """Logout the current user and return to login view"""
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Clear any sensitive data or state
            # Then tell the parent LoginWindow to show the login view
            if self.parent_window:
                self.parent_window.show_login()
                # Clear any sensitive data from the login form
                self.parent_window.username_input.clear()
                self.parent_window.password_input.clear()
