from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QMessageBox,
    QLabel,
    QHBoxLayout,
    QFrame,
    QScrollArea,
    QStackedLayout,
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont
from views.reagent_view import ReagentDetailPanel


class RackView(QWidget):
    def __init__(self, parent=None, storage_id=None):
        super().__init__(parent)
        self.parent_window = parent
        self.rack_viewmodel = None
        self.reagents = []
        self.current_page = 0
        self.items_per_page = 10
        self.storage_id = storage_id

        self._current_detail_panel_came_from_search = (
            False  # Store context for ReagentDetailPanel
        )
        self._active_usage_report_view = (
            None  # To manage the active UsageReportView instance
        )

        # Create stacked layout
        self.main_stack = QStackedLayout()
        self._setup_rack_ui()

        # Set main layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(self.main_stack)

    def set_viewmodel(self, viewmodel):
        """Set the ViewModel for this view"""
        self.rack_viewmodel = viewmodel

    def _setup_rack_ui(self):
        """Set up the UI components for the rack view"""
        # Create rack panel
        self.rack_panel = QWidget()
        rack_layout = QVBoxLayout(self.rack_panel)

        # Title
        title_label = QLabel()
        self.rack_title = title_label  # Will be updated when data loads
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rack_layout.addWidget(title_label)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        rack_layout.addWidget(divider)
        rack_layout.addSpacing(10)

        # Add reagent button
        add_button_layout = QHBoxLayout()
        add_button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.add_reagent_button = QPushButton("+ Add New Reagent")
        self.add_reagent_button.setMinimumHeight(40)
        self.add_reagent_button.setMinimumWidth(150)
        self.add_reagent_button.setStyleSheet(
            "QPushButton { background-color: #ccffcc; border: 2px solid #66cc66; border-radius: 5px; font-weight: bold; }"
            "QPushButton:hover { background-color: #a3d9a3; }"
        )
        self.add_reagent_button.clicked.connect(self._add_new_reagent)
        add_button_layout.addWidget(self.add_reagent_button)
        rack_layout.addLayout(add_button_layout)
        rack_layout.addSpacing(10)

        # Scrollable grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setSpacing(10)
        scroll_area.setWidget(self.scroll_content)
        rack_layout.addWidget(scroll_area)

        # Navigation
        nav_layout = QHBoxLayout()
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.prev_button = QPushButton("◀ Previous")
        self.prev_button.setMinimumHeight(40)
        self.prev_button.clicked.connect(self._go_to_previous_page)
        nav_layout.addWidget(self.prev_button)

        self.page_label = QLabel("Page 1")
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_label.setMinimumWidth(100)
        nav_layout.addWidget(self.page_label)

        self.next_button = QPushButton("Next ▶")
        self.next_button.setMinimumHeight(40)
        self.next_button.clicked.connect(self._go_to_next_page)
        nav_layout.addWidget(self.next_button)
        rack_layout.addLayout(nav_layout)
        rack_layout.addSpacing(10)

        # Back button
        back_layout = QHBoxLayout()
        back_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.back_button = QPushButton("Back to Home")
        self.back_button.setMinimumHeight(40)
        self.back_button.setMinimumWidth(120)
        self.back_button.clicked.connect(self._go_back)
        back_layout.addWidget(self.back_button)
        rack_layout.addLayout(back_layout)

        # Add rack panel to stack
        self.main_stack.addWidget(self.rack_panel)

    @pyqtSlot(list, str)
    def on_reagents_loaded(self, reagents, rack_name):
        """Handle loaded reagents data"""
        self.reagents = reagents
        self.rack_title.setText(f"{rack_name} - Reagent Management")
        self.current_page = 0
        self._load_current_page()

    def _load_current_page(self):
        """Load current page of reagents"""
        # Clear grid
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Load current page
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.reagents))

        for i in range(start_idx, end_idx):
            reagent = self.reagents[i]
            button = QPushButton()
            button.setMinimumHeight(70)
            button.setText(
                f"{reagent.get('Name')}\n{reagent.get('Wujud')}\nStock: {reagent.get('Stock')}"
            )
            button.setStyleSheet(
                self._get_button_style_for_hazard(reagent.get("Category_Hazard", "Low"))
            )
            button.clicked.connect(
                lambda checked, r_id=reagent["id"]: self._view_reagent_details(r_id)
            )

            relative_idx = i - start_idx
            self.grid_layout.addWidget(button, relative_idx // 5, relative_idx % 5)

        self.page_label.setText(f"Page {self.current_page + 1}/{self._total_pages()}")
        self._update_navigation_buttons()

    def _get_button_style_for_hazard(self, hazard_category):
        """Return button style based on hazard category"""
        if hazard_category in ["High", "Extreme"]:
            return "QPushButton { background-color: #ffcccc; border: 2px solid #ff6666; } QPushButton:hover { background-color: #ffaaaa; }"
        elif hazard_category == "Medium":
            return "QPushButton { background-color: #fff2cc; border: 2px solid #ffcc66; } QPushButton:hover { background-color: #ffebaa; }"
        else:
            return "QPushButton { background-color: #e6f2ff; border: 2px solid #99ccff; } QPushButton:hover { background-color: #cce6ff; }"

    def _total_pages(self):
        return max(
            1, (len(self.reagents) + self.items_per_page - 1) // self.items_per_page
        )

    def _go_to_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._load_current_page()

    def _go_to_next_page(self):
        if self.current_page < self._total_pages() - 1:
            self.current_page += 1
            self._load_current_page()

    def _update_navigation_buttons(self):
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < self._total_pages() - 1)

    def _view_reagent_details(self, reagent_id):
        if self.rack_viewmodel:
            self.rack_viewmodel.show_reagent_details(reagent_id)

    def _add_new_reagent(self):
        if self.rack_viewmodel:
            self.rack_viewmodel.add_new_reagent()

    def remove_self_from_parent_stack(self):
        """Removes this RackView instance from its parent's QStackedWidget and clears its cache."""
        if self.parent_window and hasattr(self.parent_window, "stacked_widget"):
            self.parent_window.stacked_widget.removeWidget(self)

            # Also remove the cached attribute from parent_window
            if self.storage_id is not None:  # Check if storage_id was set
                view_key = f"rack_view_{self.storage_id}"
                if hasattr(self.parent_window, view_key):
                    try:
                        delattr(self.parent_window, view_key)
                        print(
                            f"Cleared cache key {view_key} from {self.parent_window.__class__.__name__}"
                        )
                    except AttributeError:
                        print(
                            f"Warning: Could not delete attribute {view_key} from {self.parent_window.__class__.__name__}"
                        )
            else:
                print(
                    "Warning: RackView.storage_id not set, cannot clear cache attribute by key."
                )

            self.deleteLater()  # Schedule RackView for deletion
            print(
                f"RackView for storage_id {self.storage_id} removed from stack and scheduled for deletion."
            )

    def _go_back(self):  # This is for RackView's own "Back to Home" button
        if self.parent_window:
            # If RackView's parent is LoginView (came from search), show_home on LoginView should show HomeView
            # If RackView's parent is HomeView (came from home), show_home on HomeView shows its main panel
            if hasattr(self.parent_window, "show_home"):
                self.parent_window.show_home()
            # If RackView was on LoginView's stack, show_home should ideally remove it.
            # This might need further refinement in LoginView.show_home() if RackViews are not cleaned up.
            # However, for the specific user request, remove_self_from_parent_stack handles the cleanup.

    def show_rack_view(self):
        """Switch back to rack view from detail view"""
        self.main_stack.setCurrentWidget(self.rack_panel)
        if self.rack_viewmodel:
            self.rack_viewmodel.load_reagents()

    def show_usage_reports(
        self, reagent_id, reagent_name, came_from_search_context=False
    ):  # Accept new flag
        """Show the usage reports for a specific reagent."""
        # Store the context of how the ReagentDetailPanel that triggered this was opened
        self._current_detail_panel_came_from_search = came_from_search_context
        print(
            f"RackView: Stored came_from_search_context = {self._current_detail_panel_came_from_search}"
        )

        if self.rack_viewmodel:
            try:
                usage_model = self.rack_viewmodel.get_usage_model()
                identity_model = self.rack_viewmodel.get_identity_model()

                if not usage_model or not identity_model:
                    QMessageBox.warning(
                        self,
                        "Missing Models",
                        "Cannot access usage or identity models.",
                    )
                    return

                from views.usage_report_view import UsageReportView  # Import here

                main_stack_owner = self.parent_window  # This is LoginView or HomeView

                # Clean up any previously active usage report view shown by this RackView instance
                if self._active_usage_report_view is not None:
                    if hasattr(main_stack_owner, "stacked_widget"):
                        main_stack_owner.stacked_widget.removeWidget(
                            self._active_usage_report_view
                        )
                    self._active_usage_report_view.deleteLater()
                    self._active_usage_report_view = None

                # Create the new usage report view
                # The parent of UsageReportView is 'self' (RackView)
                self._active_usage_report_view = UsageReportView(
                    usage_model, identity_model, reagent_id, reagent_name, parent=self
                )

                # Connect signals for the new UsageReportView instance
                self._active_usage_report_view.back_clicked.connect(
                    lambda r_id=reagent_id: self._return_to_reagent_detail(r_id)
                )
                self._active_usage_report_view.add_report_clicked.connect(
                    self.show_new_usage_report
                )
                self._active_usage_report_view.edit_report_clicked.connect(
                    self.show_edit_usage_report
                )

                # Add and show the UsageReportView on the main application stack
                if hasattr(main_stack_owner, "stacked_widget"):
                    main_stack_owner.stacked_widget.addWidget(
                        self._active_usage_report_view
                    )
                    main_stack_owner.stacked_widget.setCurrentWidget(
                        self._active_usage_report_view
                    )
                else:
                    QMessageBox.critical(
                        self,
                        "Error",
                        "No stacked_widget found in parent window for UsageReportView.",
                    )

            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to show usage reports: {str(e)}"
                )

    def show_new_usage_report(self, reagent_id, reagent_name):
        """Show panel to add a new usage report"""
        if self.rack_viewmodel:
            self.rack_viewmodel.show_new_usage_report(reagent_id, reagent_name)

    def show_edit_usage_report(self, report_id, reagent_id, reagent_name):
        """Show panel to edit an existing usage report"""
        if self.rack_viewmodel:
            self.rack_viewmodel.show_edit_usage_report(
                report_id, reagent_id, reagent_name
            )

    def _return_to_reagent_detail(self, reagent_id):
        """Handles back navigation from UsageReportView to ReagentDetailPanel."""
        main_stack_owner = self.parent_window  # LoginView or HomeView

        # Clean up the active UsageReportView from the main stack
        if self._active_usage_report_view is not None:
            if hasattr(main_stack_owner, "stacked_widget"):
                main_stack_owner.stacked_widget.removeWidget(
                    self._active_usage_report_view
                )
            self._active_usage_report_view.deleteLater()
            self._active_usage_report_view = None

        # Ensure RackView (self) is the current widget on its parent's stack
        if hasattr(main_stack_owner, "stacked_widget"):
            main_stack_owner.stacked_widget.setCurrentWidget(self)

        # Re-show the Reagent Detail Panel, passing the stored 'came_from_search' context
        if self.rack_viewmodel:
            print(
                f"RackView: Returning to RDP. Passing came_from_search = {self._current_detail_panel_came_from_search}"
            )
            self.rack_viewmodel.show_reagent_details(
                reagent_id, came_from_search=self._current_detail_panel_came_from_search
            )
