# viewmodels/usage_report_viewmodel.py
from PyQt6.QtCore import QObject, pyqtSignal
from datetime import datetime

# IMPORTANT: You would need to install and import an Excel library
# For example:
# import openpyxl # Or from openpyxl import Workbook
# Or:
import xlsxwriter  # Using xlsxwriter as specified


class UsageReportViewModel(QObject):
    # Signal to notify view of data changes
    data_changed = pyqtSignal()
    # Add a new signal for export feedback
    export_finished = pyqtSignal(bool, str)  # success_status, message

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
            raw_reports = self.usage_model.get_by_identity(reagent_id)  #

            # Process the raw data into a view-friendly format
            self.usage_reports = []

            for report in raw_reports:
                # Format date
                date_used = report.get("Tanggal_Terpakai", "")  #
                formatted_date = date_used

                if date_used:
                    try:
                        date_obj = datetime.strptime(date_used, "%Y-%m-%d")
                        formatted_date = date_obj.strftime("%d %b %Y")
                    except ValueError:  # More specific exception
                        pass  # Keep original format if parsing fails

                # Create processed report object
                processed_report = {
                    "id": report.get("id"),  #
                    "raw_date": date_used,
                    "formatted_date": formatted_date,
                    "amount_used": report.get("Jumlah_Terpakai", 0),  #
                    "user": report.get("User", ""),  #
                    "supporting_materials": report.get("Bahan_Pendukung", ""),  #
                    # Store all original data for potential future use
                    "raw_data": report,
                }

                self.usage_reports.append(processed_report)

            # Notify view that data has changed
            self.data_changed.emit()

            return True

        except Exception as e:
            print(f"Error loading usage data: {str(e)}")
            # It's better to re-raise or handle appropriately
            # For now, emitting an error or logging might be suitable.
            # For simplicity, we'll let it propagate or return False
            return False

    def delete_report(self, report_id):
        """Delete a usage report"""
        try:
            # Get reagent_id before deleting the report
            reagent_id_to_reload = self._get_reagent_id_from_report_id(report_id)

            # Call the model to perform the deletion
            success = self.usage_model.delete(report_id)  #

            if success and reagent_id_to_reload is not None:
                # Reload data for the correct reagent_id after successful deletion
                self.load_usage_data(reagent_id_to_reload)
            elif not success:
                print(f"Failed to delete report_id: {report_id} from model.")
            elif reagent_id_to_reload is None:
                print(
                    f"Could not find reagent_id for report_id: {report_id} to reload."
                )

            return success

        except Exception as e:
            print(f"Error deleting usage report: {str(e)}")
            # Consider re-raising or returning a more informative error
            return False

    def _get_reagent_id_from_report_id(self, report_id_to_find):
        """Helper method to get reagent_id from a report ID by searching loaded reports"""
        # This method assumes self.usage_reports is populated with data for a *specific* reagent already.
        # If a report is deleted, we need its original id_identity to reload.
        # The current self.usage_reports might not contain the report if it's already deleted from DB
        # So, it's better to fetch the report from DB first to get its id_identity if not already in raw_data

        # Try finding it in already loaded reports (if not deleted from list yet)
        for report_detail in self.usage_reports:
            if report_detail["id"] == report_id_to_find:  #
                if "id_identity" in report_detail["raw_data"]:  #
                    return report_detail["raw_data"]["id_identity"]  #

        # If not found in current list (e.g. if list was cleared or report deleted),
        # try to fetch the specific report from DB to get its id_identity
        # This is a bit problematic as the report might already be deleted.
        # A better approach would be to ensure 'id_identity' is always part of the 'raw_data'
        # when reports are loaded.
        # For now, let's assume raw_data in self.usage_reports is sufficient.
        # Or, if deletion is complex, the View might need to pass reagent_id back for reload.

        # Fallback: If the `load_usage_data` is always called with the correct parent `reagent_id`,
        # then upon deletion, we can just use that parent `reagent_id` to reload.
        # The current implementation of `delete_report` reloads based on `_get_reagent_id_from_report`
        # which might fail if the report is already gone.

        # Let's refine _get_reagent_id_from_report to use the raw_data from the model directly if needed.
        # However, if the report is deleted from the DB, we can't get it.
        # Simplest for now: assume the `load_usage_data` will be called with the correct `reagent_id`
        # after a deletion. The view currently calls `self.refresh_data()` which uses `self.reagent_id`.

        # So, let's make _get_reagent_id_from_report simpler.
        # Actually, the current design where the view calls `refresh_data()` (which uses its stored `self.reagent_id`)
        # is fine after a deletion. The `_get_reagent_id_from_report` method is perhaps overcomplicated
        # if the view manages the current reagent_id context.

        # We'll keep it as a helper if other parts of the ViewModel need it.

        specific_report_data = self.usage_model.get_by_id(report_id_to_find)  #
        if specific_report_data and "id_identity" in specific_report_data:
            return specific_report_data["id_identity"]
        return None

    def export_usage_data_to_xlsx(self, reagent_id, file_path, reagent_name="Reagent"):
        """
        Exports usage data for a given reagent to an XLSX file using xlsxwriter.
        """
        try:
            # 1. Fetch or use already loaded data
            # Ensure fresh data if necessary, or use self.usage_reports if already loaded for reagent_id
            if not self.usage_reports or (
                self.usage_reports
                and self.usage_reports[0]["raw_data"].get("id_identity") != reagent_id
            ):
                self.load_usage_data(reagent_id)

            if not self.usage_reports:
                self.export_finished.emit(False, "No usage data available to export.")
                return

            # 2. Prepare data for Excel
            headers = ["Date Used", "Amount Used", "User", "Supporting Materials"]
            data_rows = []
            for report in self.usage_reports:
                data_rows.append(
                    [
                        report["formatted_date"],  #
                        report["amount_used"],  #
                        report["user"],  #
                        report["supporting_materials"],  #
                    ]
                )

            # 3. Write to XLSX using xlsxwriter
            # --- xlsxwriter Example ---
            workbook = xlsxwriter.Workbook(file_path)
            worksheet = workbook.add_worksheet(f"{reagent_name} Usage")  # Sheet name

            # Define formats
            bold_format = workbook.add_format({"bold": True})
            title_format = workbook.add_format(
                {"bold": True, "font_size": 14, "align": "center", "valign": "vcenter"}
            )
            header_format = workbook.add_format(
                {"bold": True, "bg_color": "#DDDDDD", "border": 1}
            )
            cell_format = workbook.add_format(
                {"border": 1}
            )  # Basic border for data cells

            # Write Reagent Name as a title in the sheet
            # Merge cells: first_row, first_col, last_row, last_col
            worksheet.merge_range(
                0,
                0,
                0,
                len(headers) - 1,
                f"Usage Report for: {reagent_name}",
                title_format,
            )
            worksheet.set_row(0, 30)  # Set title row height

            # Write headers (starting from row 2 to leave space after title)
            current_row = 2  # Start headers at row index 2 (3rd row in Excel)
            for col_num, header_text in enumerate(headers):
                worksheet.write(current_row, col_num, header_text, header_format)

            current_row += 1  # Move to the next row for data

            # Write data rows
            for row_data in data_rows:
                for col_num, cell_data in enumerate(row_data):
                    worksheet.write(current_row, col_num, cell_data, cell_format)
                current_row += 1

            # Adjust column widths (optional, but good for readability)
            # xlsxwriter sets width in character units.
            # A simple approach:
            col_widths = [
                15,
                15,
                25,
                30,
            ]  # Example widths for Date, Amount, User, Materials
            for i, width in enumerate(col_widths):
                if i < len(headers):  # Ensure we don't go out of bounds
                    worksheet.set_column(i, i, width)

            workbook.close()  # This saves the file
            # --- End xlsxwriter Example ---

            self.export_finished.emit(
                True, f"Report successfully exported to:\n{file_path}"
            )

        except Exception as e:
            error_message = f"An error occurred during export: {str(e)}"
            print(error_message)  # Log the full error for debugging
            self.export_finished.emit(False, error_message)
