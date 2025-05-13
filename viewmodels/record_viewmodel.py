from PyQt6.QtCore import QObject, pyqtSignal


class RecordViewModel(QObject):
    records_loaded = pyqtSignal(list)
    record_error = pyqtSignal(str)
    record_success = pyqtSignal(str)

    def __init__(self, record_model):
        super().__init__()
        self.record_model = record_model
        self.record_view = None

    def create_record_view(self, parent_window):
        """Create and show the record view"""
        from views.record_view import RecordView

        if not parent_window:
            return False

        if (
            not hasattr(parent_window, "record_widget")
            or not parent_window.record_widget
        ):
            parent_window.record_widget = RecordView(parent_window)
            parent_window.stacked_widget.addWidget(parent_window.record_widget)
            self.record_view = parent_window.record_widget
            self.record_view.set_viewmodel(self)
            self.records_loaded.connect(self.record_view.on_records_loaded)
            self.record_error.connect(self.record_view.on_record_error)
            self.record_success.connect(self.record_view.on_record_success)

        parent_window.stacked_widget.setCurrentWidget(parent_window.record_widget)
        self.load_records()
        return True

    def load_records(self):
        """Load records from database"""
        try:
            records = self.record_model.get_all()
            self.records_loaded.emit(records if records else [])
        except Exception as e:
            self.record_error.emit(f"Error loading records: {str(e)}")

    def add_record(self, name, description):
        """Add a new record"""
        if not name or not description:
            self.record_error.emit("Name and description are required")
            return

        try:
            record_id = self.record_model.create_record(name, description)
            if record_id:
                self.record_success.emit("Record added successfully!")
            else:
                self.record_error.emit("Failed to add record")
        except Exception as e:
            self.record_error.emit(f"Error adding record: {str(e)}")

    def update_record(self, record_id, name, description):
        """Update existing record"""
        if not name or not description:
            self.record_error.emit("Name and description are required")
            return

        try:
            success = self.record_model.update_record(record_id, name, description)
            if success:
                self.record_success.emit("Record updated successfully!")
            else:
                self.record_error.emit("Failed to update record")
        except Exception as e:
            self.record_error.emit(f"Error updating record: {str(e)}")

    def delete_record(self, record_id):
        """Delete a record"""
        try:
            success = self.record_model.delete_record(record_id)
            if success:
                self.record_success.emit("Record deleted successfully!")
            else:
                self.record_error.emit("Failed to delete record")
        except Exception as e:
            self.record_error.emit(f"Error deleting record: {str(e)}")
