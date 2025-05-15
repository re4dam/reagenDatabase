# viewmodels/home_viewmodel.py
from PyQt6.QtCore import QObject, pyqtSignal


class HomeViewModel(QObject):
    """ViewModel for home screen functionality"""

    # Define signals
    storage_data_loaded = pyqtSignal(list)
    storage_error = pyqtSignal(str)
    user_data_loaded = pyqtSignal(dict)

    def __init__(
        self,
        record_model,
        user_model,
        storage_model,
        identity_model,
        usage_model,
        supporting_materials_model,
    ):
        super().__init__()
        self.record_model = record_model
        self.user_model = user_model
        self.storage_model = storage_model
        self.identity_model = identity_model
        self.usage_model = usage_model
        self.supporting_materials_model = supporting_materials_model
        self.home_view = None
        self.search_viewmodel = None
        self.rack_viewmodels = {}
        self.current_user_id = None
        self.current_user_data = None

    def create_home_view(self, parent_window):
        """Create and show the home view"""
        from views.home_view import HomeView

        if not parent_window:
            return False

        # Create the home view if it doesn't exist
        if not hasattr(parent_window, "home_widget") or not parent_window.home_widget:
            parent_window.home_widget = HomeView(parent_window)
            parent_window.stacked_widget.addWidget(parent_window.home_widget)

            # Set home view reference
            self.home_view = parent_window.home_widget
            self.home_view.set_viewmodel(self)

            # Connect signals
            self.storage_data_loaded.connect(self.home_view.on_storage_data_loaded)
            self.storage_error.connect(self.home_view.on_storage_error)
            self.user_data_loaded.connect(self.home_view.set_user_data)

            # Load initial data
            self.load_storage_data()

        # If current_user_id is set, load the user data
        if self.current_user_id:
            print(f"Loading data for user ID: {self.current_user_id}")
            self.load_current_user()

        # Switch to home widget
        parent_window.stacked_widget.setCurrentWidget(parent_window.home_widget)
        return True

    def set_current_user_id(self, user_id):
        """Set the current user ID and load the user data"""
        print(f"Setting current user ID to: {user_id}")
        self.current_user_id = user_id
        # We'll wait to load the user data until the home view is created
        # This ensures the signals are properly connected first

    def load_current_user(self):
        """Load the current user's data from the database"""
        print(f"Loading user data for ID: {self.current_user_id}")
        if not self.current_user_id or not self.user_model:
            print("Current user ID or user model is None")
            return None

        try:
            user_data = self.user_model.get_by_id(self.current_user_id)
            if user_data:
                print(f"User data loaded successfully: {user_data}")
                self.current_user_data = user_data
                # Emit signal to update the view with the user data
                self.user_data_loaded.emit(user_data)
                return user_data
            else:
                print(f"No user found with ID: {self.current_user_id}")
        except Exception as e:
            print(f"Error loading user data: {str(e)}")
        return None

    def get_current_user(self):
        """Get the current user's data"""
        # Return cached data if available
        if self.current_user_data:
            return self.current_user_data

        # Try to load if not cached
        return self.load_current_user()

    def load_storage_data(self):
        """Load storage data from the database"""
        try:
            storage_data = self.storage_model.get_all()
            self.storage_data_loaded.emit(storage_data if storage_data else [])
        except Exception as e:
            self.storage_error.emit(f"Error getting storage data: {str(e)}")

    def show_search(self):
        """Show the search view"""
        if not self.home_view or not self.home_view.parent_window:
            return False

        # Initialize search viewmodel if needed
        if not self.search_viewmodel:
            from viewmodels.search_viewmodel import SearchViewModel

            self.search_viewmodel = SearchViewModel(
                self.identity_model,
                self.storage_model,
                self.usage_model,
                self.supporting_materials_model,
            )

        return self.search_viewmodel.create_search_view(self.home_view.parent_window)

    def show_rack(self, storage_id, storage_name):
        """Show a specific rack view"""
        if not self.home_view:
            return False

        # Initialize rack viewmodel if needed
        from viewmodels.rack_viewmodel import RackViewModel

        self.rack_viewmodels[storage_id] = RackViewModel(
            self.identity_model,
            self.storage_model,
            self.usage_model,
            self.supporting_materials_model,
            storage_id,
            storage_name,
        )

        return self.rack_viewmodels[storage_id].create_rack_view(self.home_view)

    def logout(self):
        """Logout the current user"""
        if self.home_view and self.home_view.parent_window:
            # Clear the current user data
            self.current_user_id = None
            self.current_user_data = None

            # Return to login screen
            self.home_view.parent_window.show_login()
            return True
        return False
