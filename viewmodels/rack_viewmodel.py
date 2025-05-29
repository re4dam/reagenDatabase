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
        self.rack_view = None  # This will hold the RackView QWidget instance
        self.detail_viewmodel = None

    def get_usage_model(self):
        """Return the usage model instance"""
        return self.usage_model

    def get_identity_model(self):
        """Return the usage model instance"""
        return self.identity_model

    def create_rack_view(self, parent_window):
        """Create and show the rack view.
        parent_window can be HomeView or LoginView.
        """
        from views.rack_view import RackView

        view_key = f"rack_view_{self.storage_id}"
        # created_new_view = False # We don't strictly need this flag for the connection logic anymore

        if not hasattr(parent_window, view_key):
            print(
                f"No attribute {view_key} on {parent_window.__class__.__name__}. Creating new RackView."
            )
            new_rack_view = RackView(parent=parent_window, storage_id=self.storage_id)
            parent_window.stacked_widget.addWidget(new_rack_view)
            setattr(parent_window, view_key, new_rack_view)
            self.rack_view = new_rack_view
            # created_new_view = True
        else:
            print(
                f"Attribute {view_key} found on {parent_window.__class__.__name__}. Reusing."
            )
            self.rack_view = getattr(parent_window, view_key)

        if self.rack_view is None:
            print(
                f"ERROR: self.rack_view is None for {view_key} on {parent_window.__class__.__name__}. Recreating as a fallback."
            )
            new_rack_view = RackView(parent=parent_window, storage_id=self.storage_id)
            parent_window.stacked_widget.addWidget(new_rack_view)
            setattr(parent_window, view_key, new_rack_view)
            self.rack_view = new_rack_view
            # created_new_view = True

        self.rack_view.set_viewmodel(self)

        # Ensure the signal is connected (or reconnected) correctly without duplicates.
        try:
            # Attempt to disconnect first to prevent multiple connections to the same slot.
            self.reagents_loaded.disconnect(self.rack_view.on_reagents_loaded)
            print(
                f"Disconnected reagents_loaded from {self.rack_view.on_reagents_loaded} for {view_key}"
            )
        except TypeError:  # This exception occurs if the slot was not connected.
            print(
                f"No prior connection or already disconnected for reagents_loaded for {view_key}"
            )
            pass  # It's fine, just means it wasn't connected before.

        self.reagents_loaded.connect(self.rack_view.on_reagents_loaded)
        print(
            f"Connected reagents_loaded to {self.rack_view.on_reagents_loaded} for {view_key}"
        )

        try:
            parent_window.stacked_widget.setCurrentWidget(self.rack_view)
        except RuntimeError as e:
            print(
                f"RuntimeError setting current widget to {self.rack_view} for key {view_key}: {e}"
            )
            if hasattr(parent_window, view_key):
                # If the cached view is problematic, remove it from cache and try creating again.
                delattr(parent_window, view_key)
            print("Re-attempting create_rack_view due to RuntimeError.")
            # Recursive call must have a clear exit or different logic to avoid infinite loop.
            # For now, if it fails here, it might indicate a deeper issue with widget lifecycle.
            # A simple re-attempt might work if the state causing the error is transient.
            return self.create_rack_view(parent_window)

        self.load_reagents()
        return True

    def load_reagents(self):
        """Load reagents for this storage location"""
        try:
            reagents = self.identity_model.get_by_storage(self.storage_id)
            self.reagents_loaded.emit(reagents if reagents else [], self.storage_name)
        except Exception as e:
            print(f"Error loading reagents: {str(e)}")

    def show_reagent_details(self, reagent_id, came_from_search=False):
        if not self.rack_view:
            print(
                "Error: RackViewModel.rack_view is not set or invalid before showing details."
            )
            return False

        from viewmodels.reagent_viewmodel import ReagentViewModel
        from views.reagent_view import ReagentDetailPanel

        # Create/Recreate the ReagentDetailPanel with the correct 'came_from_search' status
        detail_panel = ReagentDetailPanel(
            identity_model=self.identity_model,
            reagent_id=reagent_id,
            rack_name=self.storage_name,
            parent=self.rack_view,  # Parent for ReagentDetailPanel is the RackView QWidget
            came_from_search=came_from_search,  # Pass the flag
        )
        # Add ReagentDetailPanel to the RackView's internal stack
        # It's important that if a detail_panel already exists for this reagent_id in the stack,
        # it's either removed or updated. Adding multiple identical panels can be an issue.
        # A simple approach is to clear other detail panels or ensure only one is active.
        # For now, assuming addWidget handles replacement or stack navigation correctly,
        # or that previous instances are removed.

        # Clear previous widgets in main_stack except for the rack_panel itself if it's there
        # to prevent multiple detail panels from accumulating.
        if (
            self.rack_view
            and hasattr(self.rack_view, "main_stack")
            and hasattr(self.rack_view, "rack_panel")
        ):
            while (
                self.rack_view.main_stack.count() > 1
            ):  # Assuming rack_panel is at index 0
                widget_to_remove = self.rack_view.main_stack.widget(1)
                if (
                    widget_to_remove != self.rack_view.rack_panel
                ):  # Do not remove the base rack panel
                    self.rack_view.main_stack.removeWidget(widget_to_remove)
                    widget_to_remove.deleteLater()
                else:  # Should not happen if rack_panel is index 0
                    break

        self.rack_view.main_stack.addWidget(detail_panel)
        self.rack_view.main_stack.setCurrentWidget(detail_panel)
        return True

    def add_new_reagent(self):
        if not self.rack_view:
            print(
                "Error: RackViewModel.rack_view is not set or invalid before adding new reagent."
            )
            return False

        from viewmodels.reagent_viewmodel import ReagentViewModel
        from views.reagent_view import ReagentDetailPanel

        # Create ReagentViewModel for a new reagent
        # For a new reagent, reagent_id is None.
        # The rack_name here should be self.storage_name for consistency with ReagentViewModel's expectation
        self.detail_viewmodel = (
            ReagentViewModel(  # This seems to be an attribute of RackViewModel
                self.identity_model,
                reagent_id=None,
                rack_name=self.storage_name,  # Use storage_name
            )
        )

        detail_panel = ReagentDetailPanel(
            identity_model=self.identity_model,
            reagent_id=None,  # Explicitly None for new reagent
            rack_name=self.storage_name,  # Pass storage_name
            parent=self.rack_view,
            came_from_search=False,  # New reagent is not from search context in this method
        )
        self.rack_view.main_stack.addWidget(detail_panel)
        self.rack_view.main_stack.setCurrentWidget(detail_panel)
        return True

    def show_new_usage_report(self, reagent_id, reagent_name):
        """Show panel to add a new usage report"""
        if (
            not self.rack_view or not self.rack_view.parent_window
        ):  # parent_window of RackView
            return False

        from viewmodels.usage_edit_viewmodel import UsageEditViewModel

        usage_viewmodel = UsageEditViewModel(
            usage_model=self.usage_model,
            identity_model=self.identity_model,
            supporting_materials_model=self.supporting_materials_model,
            reagent_id=reagent_id,
            reagent_name=reagent_name,
            usage_id=None,
        )
        return usage_viewmodel.create_usage_edit_view(self.rack_view.parent_window)

    def show_edit_usage_report(self, report_id, reagent_id, reagent_name):
        """Show panel to edit an existing usage report"""
        if not self.rack_view or not self.rack_view.parent_window:
            return False

        from viewmodels.usage_edit_viewmodel import UsageEditViewModel

        usage_viewmodel = UsageEditViewModel(
            usage_model=self.usage_model,
            identity_model=self.identity_model,
            supporting_materials_model=self.supporting_materials_model,
            reagent_id=reagent_id,
            reagent_name=reagent_name,
            usage_id=report_id,
        )
        return usage_viewmodel.create_usage_edit_view(self.rack_view.parent_window)
