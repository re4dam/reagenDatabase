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
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class RackWidget(QWidget):
    def __init__(self, record_model, rack_name, parent=None):
        super().__init__(parent)
        self.record_model = record_model
        self.rack_name = rack_name
        self.parent_widget = parent  # Reference to the parent HomeWidget
        self.current_page = 0
        self.items_per_page = 10  # 2x5 grid

        # This would come from your database in a real implementation
        # For now, we'll use dummy data
        self.reagents = self._get_dummy_reagents()

        self._setup_ui()

    def _get_dummy_reagents(self):
        """Return dummy reagent data for demonstration purposes"""
        # In a real implementation, you would query your database here
        # Example: return self.record_model.get_reagents_by_rack(self.rack_name)

        # Create dummy reagents (25 items to demonstrate pagination)
        dummy_reagents = []
        for i in range(1, 26):
            reagent = {
                "id": i,
                "name": f"Reagent {i}",
                "formula": f"Formula-{i}",
                "location": f"{self.rack_name}-{(i - 1) // 10 + 1}-{(i - 1) % 10 + 1}",  # Rack-Page-Position
                "quantity": f"{i * 10} mL",
                "expiry_date": "2025-12-31",
            }
            dummy_reagents.append(reagent)

        return dummy_reagents

    def _setup_ui(self):
        """Set up the UI components for the rack view"""
        main_layout = QVBoxLayout(self)

        # Title
        title_label = QLabel(f"{self.rack_name} - Reagent Management")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Add a divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(divider)
        main_layout.addSpacing(10)

        # Create a scrollable area for the reagent grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.grid_layout = QGridLayout(scroll_content)
        self.grid_layout.setSpacing(10)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

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

        main_layout.addLayout(nav_layout)
        main_layout.addSpacing(10)

        # Back button
        back_layout = QHBoxLayout()
        back_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.back_button = QPushButton("Back to Home")
        self.back_button.setMinimumHeight(40)
        self.back_button.setMinimumWidth(120)
        self.back_button.clicked.connect(self._go_back)
        back_layout.addWidget(self.back_button)

        main_layout.addLayout(back_layout)

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
            reagent_button = QPushButton(reagent["name"])
            reagent_button.setMinimumHeight(70)

            # Add additional info to the button
            button_text = (
                f"{reagent['name']}\n{reagent['formula']}\n{reagent['quantity']}"
            )
            reagent_button.setText(button_text)

            # Set style for reagent buttons
            reagent_button.setStyleSheet(
                "QPushButton { background-color: #e6f2ff; border: 2px solid #99ccff; "
                "border-radius: 5px; text-align: center; }"
                "QPushButton:hover { background-color: #cce6ff; }"
            )

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

    def _total_pages(self):
        """Calculate the total number of pages"""
        return (len(self.reagents) + self.items_per_page - 1) // self.items_per_page

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
        """View details of a specific reagent"""
        # Find the reagent by ID
        reagent = next((r for r in self.reagents if r["id"] == reagent_id), None)

        if reagent:
            # In a real application, you would navigate to a detailed view or show a dialog
            # For now, we'll just show a message box with reagent details
            details = (
                f"Reagent Details:\n\n"
                f"Name: {reagent['name']}\n"
                f"Formula: {reagent['formula']}\n"
                f"Location: {reagent['location']}\n"
                f"Quantity: {reagent['quantity']}\n"
                f"Expiry Date: {reagent['expiry_date']}"
            )

            QMessageBox.information(self, "Reagent Details", details)

    def _go_back(self):
        """Return to the home screen"""
        if self.parent_widget:
            self.parent_widget.show_home()
