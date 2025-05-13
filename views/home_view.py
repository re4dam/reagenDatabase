# views/home_view.py
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
from PyQt6.QtCore import Qt, pyqtSlot


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

    def _setup_main_ui(self):
        """Set up the UI components for the home page"""
        main_layout = QVBoxLayout(self.main_view)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title_label = QLabel("Sistem Manajemen Reagen Laboratorium")
        title_font = QLabel().font()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Next Title
        next_title_label = QLabel(
            "Departemen Biokimia Fakultas Kedokteran Universitas Indonesia"
        )
        next_title_font = QLabel().font()
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
        modules_font = QLabel().font()
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

        # Storage/Rack label
        rack_label = QLabel("Reagent Storage:")
        rack_label.setFont(modules_font)
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

    def _show_record_manager(self):
        """Show the record manager widget"""
        if self.home_viewmodel:
            self.home_viewmodel.show_record_manager()

    def _show_user_management(self):
        """Show the user management widget"""
        if self.home_viewmodel:
            self.home_viewmodel.show_user_management()

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
