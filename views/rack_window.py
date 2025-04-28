# views/rack_window.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QFrame,
    QMessageBox,
    QScrollArea,
    QStackedLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from views.reagent_panel import ReagentDetailPanel


class RackWidget(QWidget):
    def __init__(
        self, identity_model, storage_model, usage_model, rack_name, parent=None
    ):
        super().__init__(parent)
        self.identity_model = identity_model  # Model for reagent operations
        self.storage_model = storage_model  # Model for storage operations
        self.usage_model = usage_model
        self.rack_name = rack_name
        self.parent_widget = parent  # Reference to the parent HomeWidget
        self.current_page = 0
        self.items_per_page = 10  # 2x5 grid

        # Get storage ID for this rack
        self.storage_id = self._get_storage_id()

        # Get reagents for this storage location
        self.reagents = self._get_reagents()

        # Create a stacked layout to switch between views
        self.main_stack = QStackedLayout()

        # Create the rack view as a separate panel
        self.rack_panel = QWidget()
        self.rack_layout = QVBoxLayout(self.rack_panel)
        self._setup_rack_ui()  # Contains what was in _setup_ui

        # Add rack panel to stack
        self.main_stack.addWidget(self.rack_panel)

        # Main layout contains only the stack
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(self.main_stack)

    def _get_storage_id(self):
        """Get the storage ID for this rack"""
        try:
            # Query the storage based on rack name
            storage = self.storage_model.get_all()
            # Find the storage matching this rack name
            for item in storage:
                if item.get("Name") == self.rack_name:
                    return item.get("id")

            # If not found, return a default (for development)
            return 1
        except Exception as e:
            print(f"Error getting storage ID: {str(e)}")
            return 1

    def _get_reagents(self):
        """Return reagent data from the database"""
        try:
            # Get reagents from this storage location
            reagents = self.identity_model.get_by_storage(self.storage_id)
            return reagents if reagents else []
        except Exception as e:
            print(f"Error getting reagents: {str(e)}")
            return []

    def _setup_rack_ui(self):
        """Set up the UI components for the rack view"""
        # Title
        title_label = QLabel(f"{self.rack_name} - Reagent Management")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rack_layout.addWidget(title_label)

        # Add a divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        self.rack_layout.addWidget(divider)
        self.rack_layout.addSpacing(10)

        # Add button for new reagent
        add_button_layout = QHBoxLayout()
        add_button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.add_reagent_button = QPushButton("+ Add New Reagent")
        self.add_reagent_button.setMinimumHeight(40)
        self.add_reagent_button.setMinimumWidth(150)
        self.add_reagent_button.setStyleSheet(
            "QPushButton { background-color: #ccffcc; border: 2px solid #66cc66; "
            "border-radius: 5px; font-weight: bold; }"
            "QPushButton:hover { background-color: #a3d9a3; }"
        )
        self.add_reagent_button.clicked.connect(self._add_new_reagent)
        add_button_layout.addWidget(self.add_reagent_button)

        self.rack_layout.addLayout(add_button_layout)
        self.rack_layout.addSpacing(10)

        # Create a scrollable area for the reagent grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.grid_layout = QGridLayout(scroll_content)
        self.grid_layout.setSpacing(10)
        scroll_area.setWidget(scroll_content)
        self.rack_layout.addWidget(scroll_area)

        # Navigation buttons layout
        nav_layout = QHBoxLayout()
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Previous page button
        self.prev_button = QPushButton("◀ Previous")
        self.prev_button.setMinimumHeight(40)
        self.prev_button.clicked.connect(self._go_to_previous_page)
        nav_layout.addWidget(self.prev_button)

        # Page indicator
        self.page_label = QLabel("Page 1")
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_label.setMinimumWidth(100)
        nav_layout.addWidget(self.page_label)

        # Next page button
        self.next_button = QPushButton("Next ▶")
        self.next_button.setMinimumHeight(40)
        self.next_button.clicked.connect(self._go_to_next_page)
        nav_layout.addWidget(self.next_button)

        self.rack_layout.addLayout(nav_layout)
        self.rack_layout.addSpacing(10)

        # Back button
        back_layout = QHBoxLayout()
        back_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.back_button = QPushButton("Back to Home")
        self.back_button.setMinimumHeight(40)
        self.back_button.setMinimumWidth(120)
        self.back_button.clicked.connect(self._go_back)
        back_layout.addWidget(self.back_button)

        self.rack_layout.addLayout(back_layout)

        # Now load the first page of reagents AFTER all UI elements are created
        self._load_current_page()

        # Update the navigation buttons
        self._update_navigation_buttons()

    def _load_current_page(self):
        """Load the current page of reagents into the grid"""
        # Clear existing items in the grid
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Calculate start and end indices for the current page
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.reagents))

        # Populate the grid with reagent buttons
        for i in range(start_idx, end_idx):
            reagent = self.reagents[i]

            # Create button for each reagent
            reagent_button = QPushButton()
            reagent_button.setMinimumHeight(70)

            # Add info to the button
            name = reagent.get("Name", "Unknown")
            wujud = reagent.get("Wujud", "")
            stock = reagent.get("Stock", 0)

            # Format the button text
            button_text = f"{name}\n{wujud}\nStock: {stock}"
            reagent_button.setText(button_text)

            # Set style based on hazard category
            hazard = reagent.get("Category_Hazard", "Low")
            button_style = self._get_button_style_for_hazard(hazard)
            reagent_button.setStyleSheet(button_style)

            # Connect button to view reagent details
            reagent_button.clicked.connect(
                lambda checked, r_id=reagent["id"]: self._view_reagent_details(r_id)
            )

            # Calculate position in 2x5 grid
            relative_idx = i - start_idx
            row = relative_idx // 5
            col = relative_idx % 5

            # Add to grid
            self.grid_layout.addWidget(reagent_button, row, col)

        # Update page label
        self.page_label.setText(f"Page {self.current_page + 1}/{self._total_pages()}")

    def _get_button_style_for_hazard(self, hazard_category):
        """Return button style based on hazard category"""
        if hazard_category == "High" or hazard_category == "Extreme":
            return (
                "QPushButton { background-color: #ffcccc; border: 2px solid #ff6666; border-radius: 5px; text-align: center; }"
                "QPushButton:hover { background-color: #ffaaaa; }"  # Slightly brighter red
            )
        elif hazard_category == "Medium":
            return (
                "QPushButton { background-color: #fff2cc; border: 2px solid #ffcc66; border-radius: 5px; text-align: center; }"
                "QPushButton:hover { background-color: #ffebaa; }"  # Slightly brighter yellow
            )
        else:  # Low or None
            return (
                "QPushButton { background-color: #e6f2ff; border: 2px solid #99ccff; border-radius: 5px; text-align: center; }"
                "QPushButton:hover { background-color: #cce6ff; }"  # Slightly brighter blue
            )

    def _total_pages(self):
        """Calculate the total number of pages"""
        return max(
            1, (len(self.reagents) + self.items_per_page - 1) // self.items_per_page
        )

    def _go_to_previous_page(self):
        """Navigate to the previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self._load_current_page()
            self._update_navigation_buttons()

    def _go_to_next_page(self):
        """Navigate to the next page"""
        if self.current_page < self._total_pages() - 1:
            self.current_page += 1
            self._load_current_page()
            self._update_navigation_buttons()

    def _update_navigation_buttons(self):
        """Update the state of navigation buttons based on current page"""
        # Disable/enable previous button
        self.prev_button.setEnabled(self.current_page > 0)

        # Disable/enable next button
        self.next_button.setEnabled(self.current_page < self._total_pages() - 1)

    def _view_reagent_details(self, reagent_id):
        """Switch to reagent details view for a specific reagent"""
        # Create the detail panel
        self.detail_panel = ReagentDetailPanel(
            identity_model=self.identity_model,
            reagent_id=reagent_id,
            rack_name=self.rack_name,
            parent=self,
        )

        # Add to stack and switch to it
        self.main_stack.addWidget(self.detail_panel)
        self.main_stack.setCurrentWidget(self.detail_panel)

    def _add_new_reagent(self):
        """Switch to reagent details view for adding a new reagent"""
        # Create a new reagent panel with no reagent ID (for new reagent)
        self.detail_panel = ReagentDetailPanel(
            identity_model=self.identity_model,
            reagent_id=None,  # None indicates a new reagent
            rack_name=self.rack_name,
            parent=self,
        )

        # Add to stack and switch to it
        self.main_stack.addWidget(self.detail_panel)
        self.main_stack.setCurrentWidget(self.detail_panel)

    def show_rack_view(self):
        """Switch back to the rack view"""
        # Remove the detail panel from stack if it exists
        if hasattr(self, "detail_panel") and self.detail_panel is not None:
            self.main_stack.removeWidget(self.detail_panel)
            self.detail_panel.deleteLater()
            self.detail_panel = None

        # Ensure rack panel is current
        self.main_stack.setCurrentWidget(self.rack_panel)

    def refresh_reagents(self):
        """Refresh the list of reagents"""
        self.reagents = self._get_reagents()
        self.current_page = 0  # Reset to first page
        self._load_current_page()
        self._update_navigation_buttons()

    def _go_back(self):
        """Return to the home screen"""
        if self.parent_widget:
            self.parent_widget.show_home()

    def show_usage_reports(self, reagent_id, reagent_name):
        """Show usage reports for a specific reagent"""
        try:
            # For this to work, you'll need to import the UsageReportPanel
            from views.usage_report_panel import UsageReportPanel

            # # You'll also need a reference to the usage model
            # from models.usage_model import UsageModel  # Adjust path as needed
            #
            # usage_model = UsageModel()  # Instantiate the usage model

            # Create the usage report panel
            self.usage_panel = UsageReportPanel(
                usage_model=self.usage_model,
                identity_model=self.identity_model,
                reagent_id=reagent_id,
                reagent_name=reagent_name,
                parent=self,
            )

            # Add to stack and switch to it
            self.main_stack.addWidget(self.usage_panel)
            self.main_stack.setCurrentWidget(self.usage_panel)
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to show usage reports: {str(e)}"
            )
