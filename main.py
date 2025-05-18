# main.py
import sys, os
from PyQt6.QtWidgets import QApplication
from app_context import AppContext
from load_font import FontManager

# Import views
from models import supporting_materials_model
from views.login_view import LoginView

# Import viewmodels
from viewmodels.login_viewmodel import LoginViewModel
from viewmodels.register_viewmodel import RegisterViewModel
from viewmodels.home_viewmodel import HomeViewModel

# Import models
from models.database import DatabaseManager
from models.user_model import UserModel
from models.record_model import RecordModel
from models.storage_model import StorageModel
from models.identity_model import IdentityModel
from models.usage_model import UsageModel
from models.supporting_materials_model import SupportingMaterialsModel

def main():
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    AppContext.set_screen_resolution(size)
    FontManager.load_fonts("assets/fonts")

    # Initialize database
    db = DatabaseManager("my_database.db")
    user_model = UserModel(db)
    record_model = RecordModel(db)
    storage_model = StorageModel(db)
    identity_model = IdentityModel(db)
    usage_model = UsageModel(db)
    supporting_materials_model = SupportingMaterialsModel(db)

    # Initialize ViewModels
    login_viewmodel = LoginViewModel(user_model)
    register_viewmodel = RegisterViewModel(user_model)
    home_viewmodel = HomeViewModel(
        record_model,
        user_model,
        storage_model,
        identity_model,
        usage_model,
        supporting_materials_model,
    )

    # Initialize the main Login view
    login_view = LoginView()

    # Connect ViewModels to the view
    login_view.setup_viewmodels(login_viewmodel, register_viewmodel, home_viewmodel)

    # Show the login window
    login_view.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
