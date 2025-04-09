import sys
from PyQt6.QtWidgets import QApplication
from models import user_model
from models.user_model import UserModel
from views.main_window import MainWindow
from models.database import DatabaseManager
from views.user_window import UserManagementWindow


def main():
    app = QApplication(sys.argv)

    # initialize database
    db = DatabaseManager("my_database.db")
    user_model = UserModel(db)

    # initialize main window
    window = UserManagementWindow(user_model)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
