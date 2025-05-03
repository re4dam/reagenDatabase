# viewmodels/reagent_viewmodel.py
import re


class ReagentViewModel:
    """
    ViewModel that handles business logic for reagent operations.
    This mediates between the View (ReagentDetailPanel) and the Model (identity_model).
    """

    def __init__(self, identity_model, reagent_id=None, rack_name=None):
        """
        Initialize the ViewModel with model and data references

        Args:
            identity_model: The data model for reagent operations
            reagent_id: ID of existing reagent (None for new reagent)
            rack_name: Name of the rack where reagent is stored
        """
        self.identity_model = identity_model
        self.reagent_id = reagent_id
        self.rack_name = rack_name
        self.is_new = reagent_id is None
        self.edit_mode = self.is_new  # Edit mode enabled by default for new reagents

        print("This is ", self.rack_name)

        # Load existing reagent data if applicable
        self.original_data = {}
        if not self.is_new and self.reagent_id:
            self._load_data()

    def _load_data(self):
        """Load data for an existing reagent"""
        reagent = self.identity_model.get_by_id(self.reagent_id)
        # Store original data for cancel functionality
        self.original_data = reagent.copy() if reagent else {}

    def get_reagent_data(self):
        """Return the current reagent data"""
        return self.original_data

    def toggle_edit_mode(self):
        """Toggle between view and edit modes"""
        self.edit_mode = not self.edit_mode

    def save_reagent(self, reagent_data):
        """
        Save reagent data to the model

        Args:
            reagent_data: Dictionary containing reagent form data

        Returns:
            tuple: (success_bool, message_string)
        """
        # Add storage ID to the data
        # reagent_data["id_storage"] = self._get_storage_id_from_rack_name()
        reagent_data["id_storage"] = self.rack_name
        print("Testing for once ", self.rack_name)
        print("Testing for twice ", reagent_data["id_storage"])

        try:
            if self.is_new:
                # Create new reagent
                result = self.identity_model.create(**reagent_data)

                if result and isinstance(result, int):
                    self.reagent_id = result
                    self.is_new = False
                    self.original_data = reagent_data.copy()
                    return True, "New reagent added successfully"
                else:
                    return False, "Failed to create reagent"
            else:
                # Update existing reagent
                result = self.identity_model.update(self.reagent_id, **reagent_data)

                if result:
                    # Exit edit mode and update original data
                    self.edit_mode = False
                    self.original_data = reagent_data.copy()
                    return True, "Reagent updated successfully"
                else:
                    return False, "Failed to update reagent"

        except Exception as e:
            return False, f"Error: {str(e)}"

    def delete_reagent(self):
        """
        Delete the current reagent

        Returns:
            tuple: (success_bool, message_string)
        """
        if not self.reagent_id:
            return False, "No reagent to delete"

        try:
            result = self.identity_model.delete(self.reagent_id)

            if result:
                return True, "Reagent deleted successfully"
            else:
                return False, "Failed to delete reagent"

        except Exception as e:
            return False, f"Error: {str(e)}"

    def cancel_edit(self):
        """Cancel editing and revert to original state"""
        # Just exit edit mode, the view will reload the original data
        self.edit_mode = False

    def _get_storage_id_from_rack_name(self):
        """
        Get storage ID from rack name

        Returns:
            int: Storage ID derived from rack name
        """
        if not self.rack_name:
            return 1

        try:
            # Extract any numeric part from the rack name
            match = re.search(r"\d+", self.rack_name)
            if match:
                return int(match.group())
            else:
                return 1
        except:
            return 1
