import sys
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow
from models.database import DatabaseManager


def main():
    app = QApplication(sys.argv)

    # initialize database
    db = DatabaseManager("my_database.db")

    # initialize main window
    window = MainWindow(db)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
