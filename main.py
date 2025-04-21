import sys
from PyQt6.QtWidgets import QApplication
from models.record_model import RecordModel
from models.user_model import UserModel
from models.database import DatabaseManager
from views.home_window import HomeWindow


def main():
    app = QApplication(sys.argv)

    # Initialize database
    db = DatabaseManager("my_database.db")
    user_model = UserModel(db)
    record_model = RecordModel(db)

    # Initialize home window
    home_window = HomeWindow()
    home_window.setup_models(record_model, user_model)
    home_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
