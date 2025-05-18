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
    QGraphicsDropShadowEffect,
)
from PyQt6.QtCore import Qt, pyqtSlot, QSize
from PyQt6.QtGui import QPixmap, QFont, QIcon, QRegion, QPainterPath, QColor
from views.reagent_view import ReagentDetailPanel
from app_context import AppContext
from load_font import FontManager

class RackView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.rack_viewmodel = None
        self.reagents = []
        self.current_page = 0
        self.items_per_page = 10

        # Create stacked layout
        self.main_stack = QStackedLayout()
        self._setup_rack_ui()

        # Set main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(self.main_stack)

    def set_viewmodel(self, viewmodel):
        """Set the ViewModel for this view"""
        self.rack_viewmodel = viewmodel
    
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

    def _setup_rack_ui(self):
        """Set up the UI components for the rack view"""
        # Create rack panel
        self.rack_panel = QWidget()
        rack_layout = QVBoxLayout(self.rack_panel)
        rack_layout.setContentsMargins(0, 0, 0, 0)
        screen_size = AppContext.get_screen_resolution()
        
        # Create container widget for layering
        container = QWidget(self.rack_panel)
        container.setGeometry(0, 0, screen_size.width(), screen_size.height())
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        # Background layer - Lab image
        background_label = QLabel(container)
        background_label.setPixmap(QPixmap("assets/Rack/background.png"))  # Use your actual image path
        background_label.setScaledContents(True)
        background_label.setGeometry(0, 0, screen_size.width(), screen_size.height())
        background_label.lower()

        # Drop Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)
        shadow.setOffset(5, 7)
        shadow.setColor(QColor(0, 0, 0, 165))

        # Title
        title_label = QLabel(container)
        self.rack_title = title_label  # Will be updated when data loads
        title_label.setGeometry(0, 0, screen_size.width(), 132)
        title_label.setFont(FontManager.get_font("PlusJakartaSans-Regular", 60))
        title_label.setStyleSheet("""
            QLabel{
                font-weight: bold;
                color: white;         
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title_label.setGraphicsEffect(shadow)
        title_label.raise_()

        # Foreground
        foreground = QLabel(container)
        foreground.setPixmap(QPixmap("assets/Rack/foreground.png"))  # Use your actual image path
        foreground.setScaledContents(True)
        foreground.setGeometry(*self.scale_rect(89, 140, 1742, 861))
        foreground.raise_()

        # Scrollable grid
        scroll_area = QScrollArea(container)
        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setSpacing(10)
        scroll_area.setWidget(self.scroll_content)
        scroll_area.setWidgetResizable(True)
        scroll_area.setGeometry(*self.scale_rect(89, 140, 1742, 861))
        scroll_area.setStyleSheet("border: none; background: transparent;")
        scroll_area.raise_()

        self.add_reagent_button = QPushButton(container)
        add_normal = QIcon("assets/Rack/add.png")
        add_hover = QIcon("assets/Rack/add_hover.png")
        self.add_reagent_button.setIcon(add_normal)
        self.add_reagent_button.setIconSize(QSize(*self.scale_icon(174, 174)))
        self.add_reagent_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
        """)
        self.add_reagent_button.setGeometry(*self.scale_rect(1722, 865, 174, 174))
        self.add_reagent_button.enterEvent = lambda event: self.add_reagent_button.setIcon(add_hover)
        self.add_reagent_button.leaveEvent = lambda event: self.add_reagent_button.setIcon(add_normal)
        self.add_reagent_button.clicked.connect(self._add_new_reagent)
        self.add_reagent_button.raise_()

        self.prev_button = QPushButton(container)
        icon_prev = QIcon("assets/Rack/back.png")
        self.prev_button.setIcon(icon_prev)
        self.prev_button.setIconSize(QSize(*self.scale_icon(57, 88)))
        self.prev_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        self.prev_button.clicked.connect(self._go_to_previous_page)
        self.prev_button.setGeometry(*self.scale_rect(13, 525, 57, 88))
        self.prev_button.raise_()

        self.page_label = QLabel(container)
        self.page_label.setFont(FontManager.get_font("PlusJakartaSans-Regular", 28))
        self.page_label.setStyleSheet("font-weight: bold; color: white;")
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_label.setFixedSize(QSize(*self.scale_icon(150, 150)))
        self.page_label.move(940, 885)
        self.page_label.raise_()

        self.next_button = QPushButton(container)
        icon_next = QIcon("assets/Rack/next.png")
        self.next_button.setIcon(icon_next)
        self.next_button.setIconSize(QSize(*self.scale_icon(57, 88)))
        self.next_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        self.next_button.clicked.connect(self._go_to_next_page)
        self.next_button.setGeometry(*self.scale_rect(1848, 525, 57, 88))
        self.next_button.raise_()

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
        self.back_button.leaveEvent = lambda event: self.back_button.setIcon(back_normal)
        self.back_button.clicked.connect(self._go_back)
        self.back_button.raise_()

        rack_layout.addWidget(container)
        # Add rack panel to stack
        self.main_stack.addWidget(self.rack_panel)

    @pyqtSlot(list, str)
    def on_reagents_loaded(self, reagents, rack_name):
        """Handle loaded reagents data"""
        self.reagents = reagents
        self.rack_title.setText(f"{rack_name}")
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

        self.page_label.setText(f"{self.current_page + 1} / {self._total_pages()}")
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

    def _go_back(self):
        if self.parent_window:
            self.parent_window.show_home()

    def show_rack_view(self):
        """Switch back to rack view from detail view"""
        self.main_stack.setCurrentWidget(self.rack_panel)
        if self.rack_viewmodel:
            self.rack_viewmodel.load_reagents()

    def show_usage_reports(self, reagent_id, reagent_name):
        """Show the usage reports for a specific reagent"""
        if self.rack_viewmodel:
            try:
                # Get the models from the view model
                usage_model = self.rack_viewmodel.get_usage_model()
                identity_model = self.rack_viewmodel.get_identity_model()

                if not usage_model or not identity_model:
                    QMessageBox.warning(
                        self,
                        "Missing Models",
                        "Cannot access usage or identity models.",
                    )
                    return

                # Import here to avoid circular imports
                from views.usage_report_view import UsageReportView

                # Create the usage report view
                self.usage_report_view = UsageReportView(
                    usage_model, identity_model, reagent_id, reagent_name, self
                )

                # Connect signals
                self.usage_report_view.back_clicked.connect(
                    lambda: self._return_to_reagent_detail(reagent_id)
                )
                self.usage_report_view.add_report_clicked.connect(
                    self.show_new_usage_report
                )
                self.usage_report_view.edit_report_clicked.connect(
                    self.show_edit_usage_report
                )

                if hasattr(self.parent_window, "stacked_widget"):
                    self.parent_window.stacked_widget.addWidget(self.usage_report_view)
                    self.parent_window.stacked_widget.setCurrentWidget(
                        self.usage_report_view
                    )
                else:
                    QMessageBox.critical(
                        self, "Error", "No stacked_widget found in parent window."
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
        """Handles back navigation from UsageReportView to ReagentDetailPanel"""
        self._view_reagent_details(reagent_id)

        # Optionally clean up the usage report view from stack
        if self.usage_report_view:
            self.parent_window.stacked_widget.removeWidget(self.usage_report_view)
            self.usage_report_view.deleteLater()
            self.usage_report_view = None
