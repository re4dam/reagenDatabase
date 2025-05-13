from PyQt6.QtCore import QObject, pyqtSignal


class RackViewModel(QObject):
    reagents_loaded = pyqtSignal(list, str)  # reagents, rack_name

    def __init__(
        self,
        identity_model,
        storage_model,
        usage_model,
        supporting_materials_model,
        storage_id,
        storage_name,
    ):
        super().__init__()
        self.identity_model = identity_model
        self.storage_model = storage_model
        self.usage_model = usage_model
        self.supporting_materials_model = supporting_materials_model
        self.storage_id = storage_id
        self.storage_name = storage_name
        self.rack_view = None
        self.detail_viewmodel = None

    def get_usage_model(self):
        """Return the usage model instance"""
        return self.usage_model

    def get_identity_model(self):
        """Return the usage model instance"""
        return self.identity_model

    def create_rack_view(self, parent_window):
        """Create and show the rack view"""
        from views.rack_view import RackView

        # Check if we already have a view for this storage_id
        view_key = f"rack_view_{self.storage_id}"

        # Create a new view if one doesn't already exist for this storage
        if not hasattr(parent_window, view_key):
            # Create a new rack view
            new_rack_view = RackView(parent_window)

            # Add to stacked widget
            parent_window.stacked_widget.addWidget(new_rack_view)

            # Store the view with a unique key based on storage_id
            setattr(parent_window, view_key, new_rack_view)

            # Set up view model connection
            self.rack_view = new_rack_view
            self.rack_view.set_viewmodel(self)
            self.reagents_loaded.connect(self.rack_view.on_reagents_loaded)
            print("This first")
        else:
            # Get the existing view
            self.rack_view = getattr(parent_window, view_key)

            # Ensure view model is set correctly
            # (might be redundant but ensures connections are maintained)
            self.rack_view.set_viewmodel(self)
            print("This second")

        # Show the view
        parent_window.stacked_widget.setCurrentWidget(self.rack_view)

        # Refresh the data
        self.load_reagents()
        return True

    def load_reagents(self):
        """Load reagents for this storage location"""
        try:
            reagents = self.identity_model.get_by_storage(self.storage_id)
            self.reagents_loaded.emit(reagents if reagents else [], self.storage_name)
        except Exception as e:
            print(f"Error loading reagents: {str(e)}")

    def show_reagent_details(self, reagent_id):
        """Show details for a specific reagent"""
        if not self.rack_view:
            return False

        from viewmodels.reagent_viewmodel import ReagentViewModel
        from views.reagent_view import ReagentDetailPanel

        if not self.detail_viewmodel or self.detail_viewmodel.reagent_id != reagent_id:
            # This part looks like it has commented-out code.
            # I'm keeping the updated version below:
            self.detail_viewmodel = ReagentViewModel(
                self.identity_model, reagent_id, self.storage_name
            )

        detail_panel = ReagentDetailPanel(
            self.identity_model, reagent_id, self.storage_name, parent=self.rack_view
        )
        self.rack_view.main_stack.addWidget(detail_panel)
        self.rack_view.main_stack.setCurrentWidget(detail_panel)
        return True

    def add_new_reagent(self):
        """Handle adding a new reagent"""
        if not self.rack_view:
            return False

        from viewmodels.reagent_viewmodel import ReagentViewModel
        from views.reagent_view import ReagentDetailPanel

        print(self.storage_id)
        print(self.storage_name)

        self.detail_viewmodel = ReagentViewModel(
            self.identity_model,
            reagent_id=None,
            rack_name=self.storage_id,
        )

        detail_panel = ReagentDetailPanel(
            identity_model=self.identity_model,
            rack_name=self.storage_id,
            parent=self.rack_view,
        )
        self.rack_view.main_stack.addWidget(detail_panel)
        self.rack_view.main_stack.setCurrentWidget(detail_panel)
        return True

    def show_new_usage_report(self, reagent_id, reagent_name):
        """Show panel to add a new usage report"""
        if not self.rack_view:
            return False

        from viewmodels.usage_edit_viewmodel import UsageEditViewModel

        # Create viewmodel for new usage report
        usage_viewmodel = UsageEditViewModel(
            usage_model=self.usage_model,
            identity_model=self.identity_model,
            supporting_materials_model=self.supporting_materials_model,
            reagent_id=reagent_id,
            reagent_name=reagent_name,
            usage_id=None,  # None indicates new report
        )

        # Create and show the view
        return usage_viewmodel.create_usage_edit_view(self.rack_view.parent_window)

    def show_edit_usage_report(self, report_id, reagent_id, reagent_name):
        """Show panel to edit an existing usage report"""
        if not self.rack_view:
            return False

        from viewmodels.usage_edit_viewmodel import UsageEditViewModel

        # Create viewmodel for editing existing usage report
        usage_viewmodel = UsageEditViewModel(
            usage_model=self.usage_model,
            identity_model=self.identity_model,
            supporting_materials_model=self.supporting_materials_model,
            reagent_id=reagent_id,
            reagent_name=reagent_name,
            usage_id=report_id,  # Existing report ID
        )

        # Create and show the view
        return usage_viewmodel.create_usage_edit_view(self.rack_view.parent_window)
