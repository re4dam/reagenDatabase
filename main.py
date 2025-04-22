import sys
from PyQt6.QtWidgets import QApplication
from models.record_model import RecordModel
from models.user_model import UserModel
from models.database import DatabaseManager
from views.login_window import LoginWindow


def main():
    app = QApplication(sys.argv)

    # Initialize database
    db = DatabaseManager("my_database.db")
    user_model = UserModel(db)
    record_model = RecordModel(db)

    # You can log in with these test credentials:
    # Username: admin, Password: admin123
    # Username: user1, Password: password123
    # Username: inactive, Password: test (this account is deactivated)

    # Initialize login window with required models
    login_window = LoginWindow(user_model)
    login_window.setup_models(
        record_model, user_model
    )  # Make sure login window has both models
    login_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
