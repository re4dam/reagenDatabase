# viewmodels/search_viewmodel.py
from PyQt6.QtCore import QObject, pyqtSignal


class SearchViewModel(QObject):
    """ViewModel for reagent search functionality"""

    # Define signals
    search_results = pyqtSignal(list)
    search_error = pyqtSignal(str)

    def __init__(
        self, identity_model, storage_model, usage_model=None, supporting_model=None
    ):
        super().__init__()
        self.identity_model = identity_model
        self.storage_model = storage_model
        self.usage_model = usage_model  # Add usage model reference
        self.supporting_model = (
            supporting_model  # Add supporting materials model reference
        )
        self.search_view = None
        self.rack_viewmodels = {}

    def create_search_view(self, parent_window):
        """Create and show the search view"""
        from views.search_view import SearchView

        if not parent_window:
            return False

        # Create the search view if it doesn't exist
        if (
            not hasattr(parent_window, "search_widget")
            or not parent_window.search_widget
        ):
            parent_window.search_widget = SearchView(parent_window)
            parent_window.stacked_widget.addWidget(parent_window.search_widget)

            # Set search view reference
            self.search_view = parent_window.search_widget
            self.search_view.set_viewmodel(self)

            # Connect signals
            self.search_results.connect(self.search_view.on_search_results)
            self.search_error.connect(self.search_view.on_search_error)

        # Switch to search widget
        parent_window.stacked_widget.setCurrentWidget(parent_window.search_widget)
        return True

    def search_reagents(self, search_term, search_field="All Fields"):
        """Search reagents based on term and field"""
        try:
            # Get all reagents from identity model
            all_reagents = self.identity_model.get_all()

            # Get storage information
            storage_info = {}
            all_storage = self.storage_model.get_all()
            for storage in all_storage:
                storage_info[storage.get("id")] = storage.get("Name")

            # Filter results
            search_term = search_term.lower()
            results = []

            for reagent in all_reagents:
                storage_id = reagent.get("id_storage")
                reagent["storage_name"] = storage_info.get(storage_id, "Unknown")

                if not search_term:
                    # If search term is empty, include all results
                    results.append(reagent)
                    continue

                # Filter based on search field
                if search_field == "All Fields":
                    # Search across multiple fields
                    searchable_fields = [
                        "Name",
                        "Description",
                        "Wujud",
                        "Category_Hazard",
                        "Sifat",
                    ]

                    # Check if search term appears in any searchable field
                    for field in searchable_fields:
                        field_value = str(reagent.get(field, "")).lower()
                        if search_term in field_value:
                            results.append(reagent)
                            break
                else:
                    # Search in specific field
                    field_value = str(reagent.get(search_field, "")).lower()
                    if search_term in field_value:
                        results.append(reagent)

            # Emit search results
            self.search_results.emit(results)

        except Exception as e:
            self.search_error.emit(f"Error searching reagents: {str(e)}")

    def view_reagent_details(self, reagent_id, storage_id):
        """Show details for the selected reagent from search"""
        if not self.search_view or not self.search_view.parent_window:
            return False

        # Get reagent and storage info
        reagent = self.identity_model.get_by_id(reagent_id)
        storage = self.storage_model.get_by_id(storage_id)

        if not reagent or not storage:
            return False

        storage_name = storage.get("Name", "Unknown")

        # Create reagent detail panel with search source
        from views.reagent_view import ReagentDetailPanel

        reagent_detail = ReagentDetailPanel(
            self.identity_model,
            reagent_id,
            storage_name,
            self.search_view,
            previous_view="search",  # Indicate this came from search
        )

        # Connect back signal to return to search
        reagent_detail.back_to_search_view.connect(self._return_to_search)

        # Add to stacked widget and show
        parent_window = self.search_view.parent_window
        parent_window.stacked_widget.addWidget(reagent_detail)
        parent_window.stacked_widget.setCurrentWidget(reagent_detail)

        return True

    def _return_to_search(self):
        """Return to search view"""
        if self.search_view and self.search_view.parent_window:
            parent_window = self.search_view.parent_window
            parent_window.stacked_widget.setCurrentWidget(self.search_view)
