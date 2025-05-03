# main.py
import sys
from PyQt6.QtWidgets import QApplication

# Import views
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


# def main():
#     app = QApplication(sys.argv)
#
#     # Initialize database
#     db = DatabaseManager("my_database.db")
#     user_model = UserModel(db)
#     record_model = RecordModel(db)
#     storage_model = StorageModel(db)
#     identity_model = IdentityModel(db)
#     usage_model = UsageModel(db)
#
#     # You can log in with these test credentials:
#     # Username: admin, Password: admin123
#     # Username: user1, Password: password123
#     # Username: inactive, Password: test (this account is deactivated)
#
#     # Initialize login window with required models
#     login_window = LoginWindow(user_model)
#     login_window.setup_models(
#         record_model, user_model, storage_model, identity_model, usage_model
#     )  # Make sure login window has both models
#     login_window.show()
#
#     sys.exit(app.exec())


def main():
    app = QApplication(sys.argv)

    # Initialize database
    db = DatabaseManager("my_database.db")
    user_model = UserModel(db)
    record_model = RecordModel(db)
    storage_model = StorageModel(db)
    identity_model = IdentityModel(db)
    usage_model = UsageModel(db)

    # You can log in with these test credentials:
    # Username: admin, Password: admin123
    # Username: user1, Password: password123
    # Username: inactive, Password: test (this account is deactivated)

    # Initialize ViewModels
    login_viewmodel = LoginViewModel(user_model)
    register_viewmodel = RegisterViewModel(user_model)
    home_viewmodel = HomeViewModel(
        record_model, user_model, storage_model, identity_model, usage_model
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
