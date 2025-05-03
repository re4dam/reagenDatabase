# viewmodels/home_viewmodel.py
from PyQt6.QtCore import QObject, pyqtSignal


class HomeViewModel(QObject):
    """ViewModel for home screen functionality"""

    # Define signals
    storage_data_loaded = pyqtSignal(list)
    storage_error = pyqtSignal(str)

    def __init__(
        self, record_model, user_model, storage_model, identity_model, usage_model
    ):
        super().__init__()
        self.record_model = record_model
        self.user_model = user_model
        self.storage_model = storage_model
        self.identity_model = identity_model
        self.usage_model = usage_model
        self.home_view = None
        self.record_viewmodel = None
        self.user_viewmodel = None
        self.rack_viewmodels = {}

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

            # Load initial data
            self.load_storage_data()

        # Switch to home widget
        parent_window.stacked_widget.setCurrentWidget(parent_window.home_widget)
        return True

    def load_storage_data(self):
        """Load storage data from the database"""
        try:
            storage_data = self.storage_model.get_all()
            self.storage_data_loaded.emit(storage_data if storage_data else [])
        except Exception as e:
            self.storage_error.emit(f"Error getting storage data: {str(e)}")

    def show_record_manager(self):
        """Show the record manager view"""
        if not self.home_view:
            return False

        # Initialize record viewmodel if needed
        if not self.record_viewmodel:
            from viewmodels.record_viewmodel import RecordViewModel

            self.record_viewmodel = RecordViewModel(self.record_model)

        return self.record_viewmodel.create_record_view(self.home_view)

    def show_user_management(self):
        """Show the user management view"""
        if not self.home_view:
            return False

        # Initialize user viewmodel if needed
        if not self.user_viewmodel:
            from viewmodels.user_viewmodel import UserViewModel

            self.user_viewmodel = UserViewModel(self.user_model)

        return self.user_viewmodel.create_user_view(self.home_view)

    def show_rack(self, storage_id, storage_name):
        """Show a specific rack view"""
        if not self.home_view:
            return False

        # Initialize rack viewmodel if needed
        # if storage_id not in self.rack_viewmodels:
        from viewmodels.rack_viewmodel import RackViewModel

        self.rack_viewmodels[storage_id] = RackViewModel(
            self.identity_model,
            self.storage_model,
            self.usage_model,
            storage_id,
            storage_name,
        )

        return self.rack_viewmodels[storage_id].create_rack_view(self.home_view)

    def view_reagent_details(self, reagent_id):
        """Logic to display reagent details screen"""
        # This would be implemented to coordinate with your navigation service
        # or controller to display the reagent details screen
        pass

    def show_new_usage_report(self, reagent_id, reagent_name):
        """Logic to display new usage report screen"""
        # This would be implemented to coordinate with your navigation service
        # or controller to display the new usage report screen
        pass

    def show_edit_usage_report(self, report_id, reagent_id, reagent_name):
        """Logic to display edit usage report screen"""
        # This would be implemented to coordinate with your navigation service
        # or controller to display the edit usage report screen
        pass

    def logout(self):
        """Logout the current user"""
        if self.home_view and self.home_view.parent_window:
            self.home_view.parent_window.show_login()
            return True
        return False
