# views/search_view.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QComboBox,
)
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal


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

    def _setup_ui(self):
        """Set up the UI components for search view"""
        main_layout = QVBoxLayout(self)

        # Title
        title_label = QLabel("Search Reagents")
        title_font = QLabel().font()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(divider)
        main_layout.addSpacing(15)

        # Search controls
        search_controls = QHBoxLayout()

        # Search field
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_input.setMinimumHeight(40)
        self.search_input.textChanged.connect(self._perform_search)
        search_controls.addWidget(self.search_input, 3)

        # Search by field dropdown
        self.search_field = QComboBox()
        self.search_field.setMinimumHeight(40)
        self.search_field.addItems(
            ["All Fields", "Name", "Description", "Wujud", "Category_Hazard", "Sifat"]
        )
        self.search_field.currentIndexChanged.connect(self._perform_search)
        search_controls.addWidget(self.search_field, 1)

        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.setMinimumHeight(40)
        self.clear_button.clicked.connect(self._clear_search)
        search_controls.addWidget(self.clear_button)

        main_layout.addLayout(search_controls)
        main_layout.addSpacing(15)

        # Results table
        self.results_table = QTableWidget(0, 5)  # 0 rows initially, 5 columns
        self.results_table.setHorizontalHeaderLabels(
            ["Name", "Storage", "Type", "Hazard", "Stock"]
        )

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
        self.results_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.doubleClicked.connect(self._on_result_double_clicked)

        # Add a label for search instructions
        self.info_label = QLabel("Double-click on a reagent to view details")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.info_label)

        main_layout.addWidget(self.results_table)

        # Back button
        back_layout = QHBoxLayout()
        back_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.back_button = QPushButton("Back")
        self.back_button.setMinimumHeight(40)
        self.back_button.setMinimumWidth(100)
        self.back_button.clicked.connect(self._go_back)
        back_layout.addWidget(self.back_button)

        main_layout.addLayout(back_layout)

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
