# views/usage_report_viewmodel.py
from PyQt6.QtCore import QObject, pyqtSignal
from datetime import datetime


class UsageReportViewModel(QObject):
    # Signal to notify view of data changes
    data_changed = pyqtSignal()

    def __init__(self, usage_model, identity_model):
        super().__init__()

        # Store models
        self.usage_model = usage_model
        self.identity_model = identity_model

        # Store state
        self.usage_reports = []

    def load_usage_data(self, reagent_id):
        """Load usage data for the specified reagent"""
        try:
            # Fetch the raw data from the model
            raw_reports = self.usage_model.get_by_identity(reagent_id)

            # Process the raw data into a view-friendly format
            self.usage_reports = []

            for report in raw_reports:
                # Format date
                date_used = report.get("Tanggal_Terpakai", "")
                formatted_date = date_used

                if date_used:
                    try:
                        date_obj = datetime.strptime(date_used, "%Y-%m-%d")
                        formatted_date = date_obj.strftime("%d %b %Y")
                    except:
                        pass  # Keep original format if parsing fails

                # Create processed report object
                processed_report = {
                    "id": report.get("id"),
                    "raw_date": date_used,
                    "formatted_date": formatted_date,
                    "amount_used": report.get("Jumlah_Terpakai", 0),
                    "user": report.get("User", ""),
                    "supporting_materials": report.get("Bahan_Pendukung", ""),
                    # Store all original data for potential future use
                    "raw_data": report,
                }

                self.usage_reports.append(processed_report)

            # Notify view that data has changed
            self.data_changed.emit()

            return True

        except Exception as e:
            print(f"Error loading usage data: {str(e)}")
            raise e

    def delete_report(self, report_id):
        """Delete a usage report"""
        try:
            # Call the model to perform the deletion
            success = self.usage_model.delete(report_id)

            if success:
                # Reload data after successful deletion
                # We could optimize by removing from local list instead of reloading
                self.load_usage_data(self._get_reagent_id_from_report(report_id))

            return success

        except Exception as e:
            print(f"Error deleting usage report: {str(e)}")
            raise e

    def _get_reagent_id_from_report(self, report_id):
        """Helper method to get reagent_id from a report"""
        for report in self.usage_reports:
            if report["id"] == report_id:
                # If we have the reagent_id in the raw data, return it
                if "reagent_id" in report["raw_data"]:
                    return report["raw_data"]["reagent_id"]

                # Otherwise search through all reports to find matching ID
                # This is a fallback mechanism
                for r in self.usage_reports:
                    if r["id"] == report_id:
                        return r["raw_data"].get("reagent_id")

        # If report not found, return None
        return None
