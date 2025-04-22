# views/home_window.py
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class HomeWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sistem Manajemen Reagen")
        self.setGeometry(200, 200, 600, 400)
        self.record_window = None
        self.user_window = None
        self.record_model = None
        self.user_model = None
        self.login_window = None  # Reference to the login window
        self.rack_windows = [None, None, None, None]  # Initialize rack windows list

        self._setup_ui()

    def setup_models(self, record_model, user_model):
        """Store the models for use when opening windows"""
        self.record_model = record_model
        self.user_model = user_model

    def set_login_window(self, login_window):
        """Store a reference to the login window for logout functionality"""
        self.login_window = login_window

    def _setup_ui(self):
        """Set up the UI components for the home page"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
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
        self.db_button.clicked.connect(self._open_record_manager)
        buttons_layout.addWidget(self.db_button)

        # User Management Button
        self.user_button = QPushButton("User Management")
        self.user_button.setMinimumHeight(60)
        self.user_button.setMinimumWidth(180)
        self.user_button.clicked.connect(self._open_user_management)
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

            rack_button.clicked.connect(lambda checked, index=i: self._open_rack(index))

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
        self.exit_button.clicked.connect(self.close)
        bottom_buttons_layout.addWidget(self.exit_button)

        main_layout.addLayout(bottom_buttons_layout)

    def _open_record_manager(self):
        """Open the database manager window"""
        from views.record_window import MainWindow

        if not self.record_window:
            self.record_window = MainWindow(self.record_model)

            # Add back button functionality to return to home
            self.record_window.closeEvent = lambda event: self._on_window_close(
                event, self.record_window
            )

        self.record_window.show()
        self.hide()  # Hide the home window

    def _open_user_management(self):
        """Open the user management window"""
        from views.user_window import UserManagementWindow

        if not self.user_window:
            self.user_window = UserManagementWindow(self.user_model)

            # Add back button functionality to return to home
            self.user_window.closeEvent = lambda event: self._on_window_close(
                event, self.user_window
            )

        self.user_window.show()
        self.hide()  # Hide the home window

    def _open_rack(self, rack_index):
        """Open a specific reagent rack window"""
        try:
            # This is where you would import your rack window class
            # For now, we'll use a placeholder implementation
            from views.rack_window import RackWindow  # You'll need to create this

            if not self.rack_windows[rack_index]:
                rack_name = f"Rack {chr(65 + rack_index)}"  # A, B, C, D
                self.rack_windows[rack_index] = RackWindow(self.record_model, rack_name)

                # Add back button functionality to return to home
                self.rack_windows[rack_index].closeEvent = (
                    lambda event: self._on_window_close(
                        event, self.rack_windows[rack_index]
                    )
                )

            self.rack_windows[rack_index].show()
            self.hide()  # Hide the home window

        except ImportError:
            # If the rack window class isn't created yet, show a message
            from PyQt6.QtWidgets import QMessageBox

            QMessageBox.information(
                self,
                "Coming Soon",
                f"Rack {chr(65 + rack_index)} management window is not yet implemented.",
            )

    def _logout(self):
        """Logout the current user and return to login window"""
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.login_window:
                # Clear any sensitive data from the login form
                self.login_window.username_input.clear()
                self.login_window.password_input.clear()

                # Show the login window
                self.login_window.show()

                # Close all child windows
                self._close_all_child_windows()

                # Close this window
                self.close()
            else:
                # If login window reference is not available, create a new one
                from views.login_window import LoginWindow

                login_window = LoginWindow(self.user_model)
                if hasattr(self, "record_model") and self.record_model:
                    login_window.setup_models(self.record_model, self.user_model)

                login_window.show()
                self.close()

    def _close_all_child_windows(self):
        """Close all child windows"""
        if self.record_window and self.record_window.isVisible():
            self.record_window.close()

        if self.user_window and self.user_window.isVisible():
            self.user_window.close()

        for rack_window in self.rack_windows:
            if rack_window and rack_window.isVisible():
                rack_window.close()

    def _on_window_close(self, event, window):
        """Handle when a child window is closed"""
        # Show the home window again
        self.show()

        # Let the window close as normal
        event.accept()
