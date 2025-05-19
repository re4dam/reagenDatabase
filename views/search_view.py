# views/search_view.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QComboBox,
)
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QIcon
from app_context import AppContext
from load_font import FontManager


class SearchView(QWidget):
    """View for searching reagents across all storage locations"""

    # Signal when user wants to view a reagent
    view_reagent_requested = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.search_viewmodel = None
        self.search_results = []

        self._setup_ui()

    def set_viewmodel(self, viewmodel):
        """Set the ViewModel for this view"""
        self.search_viewmodel = viewmodel
    
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

    def _setup_ui(self):
        self.screen_size = AppContext.get_screen_resolution()
        """Set up the UI components for search view"""
        self.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        background_label = QLabel(self)
        background_label.setPixmap(QPixmap("assets/Search/background.png"))  # Use your actual image path
        background_label.setScaledContents(True)
        background_label.setGeometry(*self.scale_rect(0, 0, 1920, 1080))

        search_bar_bg = QLabel(self)
        search_bar_bg.setPixmap(QPixmap("assets/Search/Searchbar.png"))  # Use your actual image path
        search_bar_bg.setScaledContents(True)
        search_bar_bg.setGeometry(*self.scale_rect(170, 42, 1731, 94))

        table_bg = QLabel(self)
        table_bg.setPixmap(QPixmap("assets/Search/searchtable.png"))  # Use your actual image path
        table_bg.setScaledContents(True)
        table_bg.setGeometry(*self.scale_rect(19, 170, 1882, 870))

        # Search bar layout
        search_bar = QWidget(self)
        search_bar.setGeometry(*self.scale_rect(170, 42, 1731, 94))
        search_controls = QHBoxLayout(search_bar)

        # Search field
        self.search_input = QLineEdit(search_bar)
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_input.setFont(FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(28)))
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_input.setStyleSheet(f"""padding-left: {self.scale_style(15)}px; color: black; border: none; background: transparent;""")
        self.search_input.textChanged.connect(self._perform_search)
        search_controls.addWidget(self.search_input)

        # Search by field dropdown
        self.search_field = QComboBox(search_bar)
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
        self.search_field.currentIndexChanged.connect(self._perform_search)
        search_controls.addWidget(self.search_field)

        # Clear button
        self.clear_button = QPushButton(search_bar)
        cancel = QIcon("assets/Search/icon_cancel.png")
        cancel_hover = QIcon("assets/Search/cancel_hover.png")
        self.clear_button.setIcon(cancel)
        self.clear_button.setIconSize(QSize(*self.scale_icon(65, 65)))
        self.clear_button.setStyleSheet(
            "border: none; background: transparent;"
        )
        self.clear_button.enterEvent = lambda event: self.clear_button.setIcon(cancel_hover)
        self.clear_button.leaveEvent = lambda event: self.clear_button.setIcon(cancel)
        self.clear_button.clicked.connect(self._clear_search)
        search_controls.addWidget(self.clear_button)

        # Results table
        self.results_table = QTableWidget(0, 5, self)  # 0 rows initially, 5 columns
        self.results_table.setHorizontalHeaderLabels(
            ["Name", "Storage", "Type", "Hazard", "Stock"]
        )
        self.results_table.setShowGrid(False)
        self.results_table.setStyleSheet(f"""
            QTableWidget {{
                background: transparent;
                border: none;
            }}
            QHeaderView{{
                background: rgba(0, 0, 0, 35);
                border: none;
                border-top-left-radius: {self.scale_style(25)}px;
                border-top-right-radius: {self.scale_style(25)}px; 
            }}
            QHeaderView::section {{
                background: transparent;
                border: none;
                font-family: Figtree;
                font-size: {self.scale_style(40)}px;
                font-weight: bold;
                padding-right: 30px;
            }}
            QTableWidget::item {{
                padding-left: {self.scale_style(10)}px;  /* isi menjauh dari header */
                padding-right: {self.scale_style(10)}px;  /* isi menjauh dari header */
                border-bottom: 1px solid #ccc;  /* hanya garis bawah antar baris */
            }}
            QTableWidget::item:selected {{
                color: white;
                background-color: #2d2d2d;
            }}
        """)
        self.results_table.setGeometry(*self.scale_rect(19, 170, 1882, 870))
        self.results_table.setFont(FontManager.get_font("Figtree-Regular", self.scale_style(24)))

        # Set table properties
        self.results_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.results_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        self.results_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        self.results_table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents
        )
        self.results_table.horizontalHeader().setSectionResizeMode(
            4, QHeaderView.ResizeMode.ResizeToContents
        )
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.verticalHeader().setDefaultSectionSize(self.scale_style(50))
        self.results_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.doubleClicked.connect(self._on_result_double_clicked)

        # Add a label for search instructions
        self.info_label = QLabel("Double-click on a reagent to view details")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Back button
        # Add circular back button in top-left corner
        self.back_button = QPushButton(self)
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

    def _perform_search(self):
        """Execute search based on current input"""
        if not self.search_viewmodel:
            return

        search_term = self.search_input.text().strip()
        search_field = self.search_field.currentText()

        # Don't search if term is too short (unless cleared)
        if len(search_term) < 2 and search_term != "":
            return

        self.search_viewmodel.search_reagents(search_term, search_field)

    def _clear_search(self):
        """Clear search input and results"""
        self.search_input.clear()
        self.results_table.setRowCount(0)
        self.search_results = []

    @pyqtSlot(list)
    def on_search_results(self, results):
        """Handle search results"""
        self.search_results = results
        self._update_results_table()

    @pyqtSlot(str)
    def on_search_error(self, error_message):
        """Handle search errors"""
        QMessageBox.warning(self, "Search Error", error_message)

    def _update_results_table(self):
        """Update the results table with current search results"""
        # Clear existing rows
        self.results_table.setRowCount(0)

        # Add new rows for results
        self.results_table.setRowCount(len(self.search_results))

        for row, reagent in enumerate(self.search_results):
            # Create items for each column
            name_item = QTableWidgetItem(reagent.get("Name", ""))
            storage_item = QTableWidgetItem(reagent.get("storage_name", ""))
            wujud_item = QTableWidgetItem(reagent.get("Wujud", ""))
            hazard_item = QTableWidgetItem(reagent.get("Category_Hazard", ""))
            stock_item = QTableWidgetItem(str(reagent.get("Stock", 0)))

            # Set row items
            self.results_table.setItem(row, 0, name_item)
            self.results_table.setItem(row, 1, storage_item)
            self.results_table.setItem(row, 2, wujud_item)
            self.results_table.setItem(row, 3, hazard_item)
            self.results_table.setItem(row, 4, stock_item)

            # Add hazard-based styling
            hazard_category = reagent.get("Category_Hazard", "Low")
            if hazard_category in ["High", "Extreme"]:
                for col in range(5):
                    self.results_table.item(row, col).setBackground(Qt.GlobalColor.red)
            elif hazard_category == "Medium":
                for col in range(5):
                    self.results_table.item(row, col).setBackground(
                        Qt.GlobalColor.yellow
                    )

    def _on_result_double_clicked(self):
        """Handle double-click on a search result"""
        selected_rows = self.results_table.selectedIndexes()
        if not selected_rows:
            return

        # Get the selected row
        row = selected_rows[0].row()

        # Get the reagent ID from the result
        if row < len(self.search_results):
            reagent_id = self.search_results[row].get("id")
            storage_id = self.search_results[row].get("id_storage")

            if reagent_id and self.search_viewmodel:
                self.search_viewmodel.view_reagent_details(reagent_id, storage_id)

    def _go_back(self):
        """Return to previous screen"""
        if self.parent_window:
            self.parent_window.show_home()

    def show_home(self):
        if hasattr(self.parent_window, "show_home"):
            self.parent_window.show_home()
