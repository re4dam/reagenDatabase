from PyQt6.QtCore import QObject, pyqtSignal, QDate


class UsageEditViewModel(QObject):
    usage_loaded = pyqtSignal(dict, bool, int)  # usage_data, is_new, current_stock
    error = pyqtSignal(str)
    success = pyqtSignal(str)
    stock_warning = pyqtSignal(bool, str)  # show_warning, message

    def __init__(
        self, usage_model, identity_model, reagent_id, reagent_name, usage_id=None
    ):
        super().__init__()
        self.usage_model = usage_model
        self.identity_model = identity_model
        self.reagent_id = reagent_id
        self.reagent_name = reagent_name
        self.usage_id = usage_id
        self.is_new = usage_id is None
        self.original_amount = 0
        self.current_stock = 0
        self.usage_edit_view = None

    def create_usage_edit_view(self, parent_window):
        """Create and show the usage edit view"""
        from views.usage_edit_view import UsageEditView

        if not parent_window:
            return False

        # Always create a new widget instead of reusing
        self.usage_edit_view = UsageEditView(parent_window)
        parent_window.stacked_widget.addWidget(self.usage_edit_view)
        self.usage_edit_view.set_viewmodel(self)

        # connect the signals
        self.usage_loaded.connect(self.usage_edit_view.on_usage_loaded)
        self.error.connect(self.usage_edit_view.on_error)
        self.success.connect(self.usage_edit_view.on_success)
        self.stock_warning.connect(self.usage_edit_view.on_stock_warning)

        # old
        # if (
        #     not hasattr(parent_window, "usage_edit_widget")
        #     or not parent_window.usage_edit_widget
        # ):
        #     parent_window.usage_edit_widget = UsageEditView(parent_window)
        #     parent_window.stacked_widget.addWidget(parent_window.usage_edit_widget)
        #     self.usage_edit_view = parent_window.usage_edit_widget
        #     self.usage_edit_view.set_viewmodel(self)
        #     self.usage_loaded.connect(self.usage_edit_view.on_usage_loaded)
        #     self.error.connect(self.usage_edit_view.on_error)
        #     self.success.connect(self.usage_edit_view.on_success)
        #     self.stock_warning.connect(self.usage_edit_view.on_stock_warning)

        parent_window.stacked_widget.setCurrentWidget(self.usage_edit_view)
        self.load_usage()
        return True

    def load_usage(self):
        """Load usage data"""
        try:
            reagent = self.identity_model.get_by_id(self.reagent_id)
            self.current_stock = reagent.get("Stock", 0) if reagent else 0

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
                    self.current_stock,
                )
            else:
                usage = self.usage_model.get_by_id(self.usage_id)
                if usage:
                    self.original_amount = usage.get("Jumlah_Terpakai", 0)
                    usage["ReagentName"] = self.reagent_name
                    self.usage_loaded.emit(usage, False, self.current_stock)
                else:
                    self.error.emit("Usage report not found")
        except Exception as e:
            self.error.emit(f"Error loading usage data: {str(e)}")

    def check_stock_level(self, amount_used):
        """Check stock level against amount used"""
        net_change = (
            amount_used if self.is_new else (amount_used - self.original_amount)
        )

        if net_change > self.current_stock:
            self.stock_warning.emit(
                True,
                f"Warning: Amount exceeds current stock by {net_change - self.current_stock}",
            )
        else:
            self.stock_warning.emit(False, "")

    def save_usage(self, data):
        """Save usage data"""
        try:
            if not data["User"]:
                self.error.emit("Please enter a user name")
                return

            net_change = (
                data["Jumlah_Terpakai"]
                if self.is_new
                else (data["Jumlah_Terpakai"] - self.original_amount)
            )

            if net_change > self.current_stock:
                # Warn but allow saving
                pass

            if self.is_new:
                result = self.usage_model.create(
                    tanggal_terpakai=data["Tanggal_Terpakai"],
                    jumlah_terpakai=data["Jumlah_Terpakai"],
                    user=data["User"],
                    bahan_pendukung=data["Bahan_Pendukung"],
                    id_identity=self.reagent_id,
                )
                success_message = "Usage report added successfully"
            else:
                result = self.usage_model.update(
                    self.usage_id,
                    Tanggal_Terpakai=data["Tanggal_Terpakai"],
                    Jumlah_Terpakai=data["Jumlah_Terpakai"],
                    User=data["User"],
                    Bahan_Pendukung=data["Bahan_Pendukung"],
                )
                success_message = "Usage report updated successfully"

            if result:
                # Update stock
                new_stock = max(0, self.current_stock - net_change)
                self.identity_model.update(self.reagent_id, Stock=new_stock)

                self.success.emit(success_message)
                if self.usage_edit_view and self.usage_edit_view.parent_window:
                    parent = self.usage_edit_view.parent_window
                    if hasattr(parent, "show_usage_reports"):
                        parent.show_usage_reports(self.reagent_id, self.reagent_name)
                    # Remove the current view from the stack
                    parent.stacked_widget.removeWidget(self.usage_edit_view)
                    self.usage_edit_view.deleteLater()
                    self.usage_edit_view = None

                # wait a minute
                # if self.usage_edit_view.parent_window and hasattr(
                #     self.usage_edit_view.parent_window, "show_usage_reports"
                # ):
                #     self.usage_edit_view.parent_window.show_usage_reports(
                #         self.reagent_id, self.reagent_name
                #     )
            else:
                self.error.emit("Failed to save usage report")
        except Exception as e:
            self.error.emit(f"Error saving usage report: {str(e)}")

    def cancel(self):
        """Cancel edit"""
        if self.usage_edit_view and self.usage_edit_view.parent_window:
            parent = self.usage_edit_view.parent_window
            if hasattr(parent, "show_usage_reports"):
                parent.show_usage_reports(self.reagent_id, self.reagent_name)
            # Remove the current view from the stack
            parent.stacked_widget.removeWidget(self.usage_edit_view)
            self.usage_edit_view.deleteLater()
            self.usage_edit_view = None
