# Updated ReagentViewModel with proper parameter case handling

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
        self.temp_image_data = None

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
        # Convert rack name to storage ID
        reagent_data["id_storage"] = self._get_storage_id_from_rack_name()
        # print("Saving reagent data " + str(reagent_data))

        try:
            if self.is_new:
                # Create new reagent - convert parameter names to lowercase
                lowercase_data = self._convert_keys_to_lowercase(reagent_data)
                result = self.identity_model.create(**lowercase_data)

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

    def _convert_keys_to_lowercase(self, data_dict):
        """
        Convert dictionary keys to lowercase for compatibility with model methods

        Args:
            data_dict: Dictionary with mixed-case keys

        Returns:
            dict: Dictionary with lowercase keys
        """
        # Define mapping between capitalized DB column names and lowercase model parameters
        key_mapping = {
            "Name": "name",
            "Description": "description",
            "Wujud": "wujud",
            "Stock": "stock",
            "Massa": "massa",
            "Tanggal_Expire": "tanggal_expire",
            "Category_Hazard": "category_hazard",
            "Sifat": "sifat",
            "Tanggal_Produksi": "tanggal_produksi",
            "Tanggal_Pembelian": "tanggal_pembelian",
            "SDS": "sds",
            "id_storage": "id_storage",
            "Image": "image",
        }

        result = {}
        for key, value in data_dict.items():
            if key in key_mapping:
                result[key_mapping[key]] = value
            else:
                # Keep the key as is if not in mapping
                result[key] = value

        return result

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
            # Extract storage ID from specific rack name patterns
            storage_map = {"Lemari 1": 1, "Lemari 2": 2, "Lemari 3": 3, "Lemari 4": 4}

            # Exact match first
            if self.rack_name in storage_map:
                return storage_map[self.rack_name]

            # If no exact match, try to extract number
            match = re.search(r"Lemari\s*(\d+)", self.rack_name)
            if match:
                lemari_num = int(match.group(1))
                if 1 <= lemari_num <= 4:
                    return lemari_num

            # Fallback to default
            return 1
        except:
            return 1

    def update_image(self, image_data):
        """
        Set image data to be saved with the reagent

        Args:
            image_data: Binary image data
        """
        self.temp_image_data = image_data

        # If we're updating an existing reagent and not in edit mode (direct image update)
        if not self.is_new and not self.edit_mode and self.reagent_id:
            try:
                result = self.identity_model.update_image(self.reagent_id, image_data)
                if result:
                    # Update original data with new image
                    if self.original_data:
                        self.original_data["Image"] = image_data
                    return True, "Image updated successfully"
                else:
                    return False, "Failed to update image"
            except Exception as e:
                return False, f"Error updating image: {str(e)}"

        return True, "Image will be saved with reagent data"

    def get_image(self):
        """
        Get the image data for this reagent

        Returns:
            bytes: Image data if available, None otherwise
        """
        # If we have temp image data, use that
        if hasattr(self, "temp_image_data") and self.temp_image_data:
            return self.temp_image_data

        # Otherwise, if we have an existing reagent, fetch from model
        if not self.is_new and self.reagent_id:
            if "Image" in self.original_data and self.original_data["Image"]:
                return self.original_data["Image"]
            else:
                # Fetch directly from database in case it wasn't loaded with initial data
                return self.identity_model.get_image(self.reagent_id)

        return None
