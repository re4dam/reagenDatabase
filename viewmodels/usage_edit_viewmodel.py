# reagenDatabaseGUI/viewmodels/usage_edit_viewmodel.py
from PyQt6.QtCore import QObject, pyqtSignal, QDate

class UsageEditViewModel(QObject):
    usage_loaded = pyqtSignal(dict, bool, int, list)
    error = pyqtSignal(str)
    success = pyqtSignal(str)
    stock_warning = pyqtSignal(bool, str)

    def __init__(
        self,
        usage_model,
        identity_model,
        supporting_materials_model,
        reagent_id,
        reagent_name,
        usage_id=None,
    ):
        super().__init__()
        self.usage_model = usage_model
        self.identity_model = identity_model
        self.supporting_materials_model = supporting_materials_model
        self.reagent_id = reagent_id
        self.reagent_name = reagent_name
        self.usage_id = usage_id
        self.is_new = usage_id is None
        self.original_amount_used = 0  # Renamed for clarity
        self.current_stock_on_load = (
            0  # Store stock at the moment of loading the edit view
        )
        self.usage_edit_view = None

    def create_usage_edit_view(self, parent_window):
        from views.usage_edit_view import UsageEditView  # Local import

        if not parent_window:
            return False

        self.usage_edit_view = UsageEditView(parent_window)
        parent_window.stacked_widget.addWidget(self.usage_edit_view)
        self.usage_edit_view.set_viewmodel(self)

        self.usage_loaded.connect(self.usage_edit_view.on_usage_loaded)
        self.error.connect(self.usage_edit_view.on_error)
        self.success.connect(self.usage_edit_view.on_success)
        self.stock_warning.connect(self.usage_edit_view.on_stock_warning)

        # Connect amount_used_spin's valueChanged to check_stock_level
        if hasattr(self.usage_edit_view, "amount_used_spin"):
            self.usage_edit_view.amount_used_spin.valueChanged.connect(
                self.check_stock_level
            )

        parent_window.stacked_widget.setCurrentWidget(self.usage_edit_view)
        self.load_usage()
        return True

    def load_usage(self):
        try:
            reagent = self.identity_model.get_by_id(self.reagent_id)
            self.current_stock_on_load = reagent.get("Stock", 0) if reagent else 0
            supporting_materials = self.supporting_materials_model.get_all()

            if self.is_new:
                self.usage_loaded.emit(
                    {
                        "ReagentName": self.reagent_name,
                        "Tanggal_Terpakai": QDate.currentDate().toString("yyyy-MM-dd"),
                        "Jumlah_Terpakai": 1,
                        "User": "",
                        "Bahan_Pendukung": "",
                    },
                    True,
                    self.current_stock_on_load,
                    supporting_materials,
                )
                self.original_amount_used = 0  # For new reports, original is 0
            else:
                usage = self.usage_model.get_by_id(self.usage_id)
                if usage:
                    self.original_amount_used = usage.get("Jumlah_Terpakai", 0)
                    usage["ReagentName"] = self.reagent_name
                    self.usage_loaded.emit(
                        usage, False, self.current_stock_on_load, supporting_materials
                    )
                else:
                    self.error.emit("Usage report not found")
        except Exception as e:
            self.error.emit(f"Error loading usage data: {str(e)}")

    def check_stock_level(self, amount_input_from_spinbox):
        """Check stock level based on current input and original state."""
        # For a new report, any amount used reduces from current_stock_on_load
        # For an existing report, the change is (new_amount - original_amount_used)

        prospective_change = 0
        if self.is_new:
            prospective_change = amount_input_from_spinbox
        else:  # Editing existing
            prospective_change = amount_input_from_spinbox - self.original_amount_used

        prospective_remaining_stock = self.current_stock_on_load - prospective_change

        if prospective_remaining_stock < 0:
            self.stock_warning.emit(
                True,
                f"Warning: This usage would result in negative stock ({prospective_remaining_stock}). Current stock: {self.current_stock_on_load}.",
            )
        else:
            self.stock_warning.emit(False, "")

    def save_usage(self, data):
        try:
            if not data["User"]:
                self.error.emit("Please enter a user name.")
                return

            new_amount_used = data["Jumlah_Terpakai"]

            # --- Stock Adjustment Logic ---
            reagent_identity = self.identity_model.get_by_id(self.reagent_id)
            if not reagent_identity:
                self.error.emit(
                    f"Reagent with ID {self.reagent_id} not found. Cannot update stock."
                )
                return

            current_actual_stock = reagent_identity.get("Stock", 0)
            stock_after_save = 0

            if self.is_new:
                stock_after_save = current_actual_stock - new_amount_used
                success_message = "Usage report added and stock updated."
                db_action_successful = self.usage_model.create(
                    tanggal_terpakai=data["Tanggal_Terpakai"],
                    jumlah_terpakai=new_amount_used,
                    user=data["User"],
                    bahan_pendukung=data["Bahan_Pendukung"],
                    id_identity=self.reagent_id,
                )
            else:  # Editing existing report
                stock_change = new_amount_used - self.original_amount_used
                stock_after_save = current_actual_stock - stock_change
                success_message = "Usage report and stock updated."
                db_action_successful = self.usage_model.update(
                    self.usage_id,
                    Tanggal_Terpakai=data["Tanggal_Terpakai"],
                    Jumlah_Terpakai=new_amount_used,
                    User=data["User"],
                    Bahan_Pendukung=data["Bahan_Pendukung"],
                )

            if db_action_successful:
                # Ensure stock does not go below zero
                final_stock = max(0, stock_after_save)
                stock_updated = self.identity_model.update(
                    self.reagent_id, Stock=final_stock
                )

                if not stock_updated:
                    # This is a critical issue if stock fails to update after usage is logged.
                    # Consider how to handle this - maybe rollback usage log or flag for admin.
                    self.error.emit(
                        "Usage logged, but FAILED to update reagent stock. Please check manually."
                    )
                    return  # or proceed with caution

                # Update original_amount_used for next potential edit in this session
                self.original_amount_used = new_amount_used
                self.current_stock_on_load = final_stock  # Update our viewmodel's idea of stock for subsequent checks

                # Process supporting material
                supporting_material = data["Bahan_Pendukung"]
                if supporting_material:
                    self.supporting_materials_model.create(supporting_material)

                self.success.emit(success_message)

                # Navigation back
                if self.usage_edit_view and self.usage_edit_view.parent_window:
                    parent = self.usage_edit_view.parent_window
                    self._refresh_usage_reports_view(parent)  # Refresh the list view
                    if hasattr(parent, "show_usage_reports"):
                        parent.show_usage_reports(self.reagent_id, self.reagent_name)

                    parent.stacked_widget.removeWidget(self.usage_edit_view)
                    self.usage_edit_view.deleteLater()
                    self.usage_edit_view = None
            else:
                self.error.emit("Failed to save usage report to database.")
        except Exception as e:
            self.error.emit(f"Error saving usage report: {str(e)}")

    def _refresh_usage_reports_view(self, parent_window):
        if hasattr(parent_window, "stacked_widget"):
            for i in range(parent_window.stacked_widget.count()):
                widget = parent_window.stacked_widget.widget(i)
                # Check if it's the UsageReportView for the current reagent
                if (
                    widget.__class__.__name__ == "UsageReportView"
                    and hasattr(widget, "reagent_id")
                    and widget.reagent_id == self.reagent_id
                ):
                    if hasattr(widget, "refresh_data"):
                        widget.refresh_data()
                        break

    def cancel(self):
        if self.usage_edit_view and self.usage_edit_view.parent_window:
            parent = self.usage_edit_view.parent_window
            if hasattr(parent.stacked_widget.widget(2), "TransitionAnimation"):
                parent.stacked_widget.widget(2).TransitionAnimation()
            elif hasattr(parent.stacked_widget.widget(4), "TransitionAnimation"):
                parent.stacked_widget.widget(4).TransitionAnimation()
                
            # No need to refresh here as nothing changed
            if hasattr(parent, "show_usage_reports"):
                parent.show_usage_reports(self.reagent_id, self.reagent_name)

            parent.stacked_widget.removeWidget(self.usage_edit_view)
            self.usage_edit_view.deleteLater()
            self.usage_edit_view = None
