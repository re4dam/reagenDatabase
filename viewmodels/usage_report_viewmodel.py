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
                    except ValueError:  # More specific exception for parsing errors
                        pass  # Keep original format if parsing fails

                # Create processed report object
                processed_report = {
                    "id": report.get("id"),
                    "raw_date": date_used,
                    "formatted_date": formatted_date,
                    "amount_used": report.get("Jumlah_Terpakai", 0),
                    "user": report.get("User", ""),
                    "supporting_materials": report.get("Bahan_Pendukung", ""),
                    # Store all original data for potential future use, especially id_identity
                    "raw_data": report,
                }
                self.usage_reports.append(processed_report)

            # Notify view that data has changed
            self.data_changed.emit()
            return True

        except Exception as e:
            print(f"Error loading usage data: {str(e)}")
            # It's better to re-raise or handle appropriately by emitting an error signal
            # For now, returning False to indicate failure.
            return False

    def delete_report(self, report_id, current_reagent_id_for_reload):
        """Delete a usage report and adjust stock."""
        try:
            # Get the report details *before* deleting it to know the amount used and its reagent ID
            report_to_delete = self.usage_model.get_by_id(report_id)

            if not report_to_delete:
                print(f"Report ID {report_id} not found for deletion.")
                return False

            amount_in_deleted_report = report_to_delete.get("Jumlah_Terpakai", 0)
            reagent_id_of_deleted_report = report_to_delete.get("id_identity")

            # Proceed with deleting the report from the database
            success = self.usage_model.delete(report_id)

            if success:
                # If deletion was successful, adjust the stock
                if (
                    reagent_id_of_deleted_report is not None
                    and amount_in_deleted_report > 0
                ):
                    reagent_identity = self.identity_model.get_by_id(
                        reagent_id_of_deleted_report
                    )
                    if reagent_identity:
                        current_stock = reagent_identity.get("Stock", 0)
                        new_stock = current_stock + amount_in_deleted_report
                        self.identity_model.update(
                            reagent_id_of_deleted_report, Stock=new_stock
                        )
                        print(
                            f"Stock for reagent ID {reagent_id_of_deleted_report} updated to {new_stock} after deleting report ID {report_id}."
                        )
                    else:
                        print(
                            f"Could not find reagent identity for ID {reagent_id_of_deleted_report} to update stock."
                        )

                # Reload data for the current view context after successful deletion and stock update
                self.load_usage_data(current_reagent_id_for_reload)
                return True
            else:
                print(f"Failed to delete report_id: {report_id} from model.")
                return False

        except Exception as e:
            print(f"Error deleting usage report or updating stock: {str(e)}")
            return False

    def export_usage_data_to_xlsx(self, reagent_id, file_path, reagent_name="Reagent"):
        """
        Exports usage data for a given reagent to an XLSX file using xlsxwriter.
        """
        try:
            # Ensure data is loaded for the correct reagent
            # Check if current usage_reports are for the requested reagent_id
            needs_load = True
            if self.usage_reports:
                # Assuming raw_data contains id_identity
                first_report_reagent_id = self.usage_reports[0]["raw_data"].get(
                    "id_identity"
                )
                if first_report_reagent_id == reagent_id:
                    needs_load = False

            if needs_load:
                if not self.load_usage_data(
                    reagent_id
                ):  # load_usage_data now returns bool
                    self.export_finished.emit(False, "Failed to load data for export.")
                    return

            if not self.usage_reports:
                self.export_finished.emit(False, "No usage data available to export.")
                return

            headers = ["Date Used", "Amount Used", "User", "Supporting Materials"]
            data_rows = []
            for report in self.usage_reports:
                data_rows.append(
                    [
                        report["formatted_date"],
                        report["amount_used"],
                        report["user"],
                        report["supporting_materials"],
                    ]
                )

            workbook = xlsxwriter.Workbook(file_path)
            worksheet = workbook.add_worksheet(
                f"{reagent_name[:31]} Usage"
            )  # Sheet name limited to 31 chars

            title_format = workbook.add_format(
                {"bold": True, "font_size": 14, "align": "center", "valign": "vcenter"}
            )
            header_format = workbook.add_format(
                {"bold": True, "bg_color": "#DDDDDD", "border": 1, "align": "center"}
            )
            cell_format = workbook.add_format({"border": 1})
            date_format = workbook.add_format(
                {"num_format": "dd mmm yyyy", "border": 1}
            )  # For dates if raw dates are preferred

            worksheet.merge_range(
                0,
                0,
                0,
                len(headers) - 1,
                f"Usage Report for: {reagent_name}",
                title_format,
            )
            worksheet.set_row(0, 30)  # Set title row height

            current_row = 2
            for col_num, header_text in enumerate(headers):
                worksheet.write(current_row, col_num, header_text, header_format)

            current_row += 1
            for row_data in data_rows:
                for col_num, cell_data in enumerate(row_data):
                    # Could add specific formatting here, e.g., for dates or numbers
                    worksheet.write(current_row, col_num, cell_data, cell_format)
                current_row += 1

            col_widths = [15, 15, 30, 40]
            for i, width in enumerate(col_widths):
                if i < len(headers):
                    worksheet.set_column(i, i, width)

            workbook.close()
            self.export_finished.emit(
                True, f"Report successfully exported to:\n{file_path}"
            )

        except Exception as e:
            error_message = f"An error occurred during export: {str(e)}"
            print(error_message)
            self.export_finished.emit(False, error_message)
