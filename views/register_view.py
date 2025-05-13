# views/register_view.py
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtCore import pyqtSlot, QSize
from PyQt6.QtGui import QPixmap, QIcon


class RegisterView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent  # Store reference to parent
        self.register_viewmodel = None
        self._setup_ui()

    def set_viewmodel(self, viewmodel):
        """Set the ViewModel for this view"""
        self.register_viewmodel = viewmodel
        
        # Connect signals from viewmodel
        if self.register_viewmodel:
            self.register_viewmodel.registration_succeeded.connect(self.on_registration_success)
            self.register_viewmodel.registration_failed.connect(self.on_registration_failed)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create container widget to allow layering
        container = QWidget(self)
        container.setFixedSize(1920, 1080)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        ## Elemen layer ##
        #Background
        background_label = QLabel(container)
        background_label.setPixmap(QPixmap("assets/Register/Register.png"))
        background_label.setScaledContents(True)
        background_label.setGeometry(0, 0, 1920, 1080)

        # Foreground panel (main panel)
        panel_label = QLabel(container)
        panel_label.setPixmap(QPixmap("assets/Register/Register2.png"))
        panel_label.setScaledContents(True)
        panel_label.setGeometry(54, 23, 1812, 1012)
        panel_label.raise_()  # put it on top of background

        #Logo
        logo = QLabel(container)
        logo.setPixmap(QPixmap("assets/logo.png"))
        logo.setScaledContents(True)
        logo.setGeometry(85, 50, 673, 93)
        logo.raise_()

        #Tulisan Register
        register_text = QLabel(container)
        register_text.setPixmap(QPixmap("assets/Register/RegisterText.png"))
        register_text.setScaledContents(True)
        register_text.setGeometry(1248, 70, 325, 51)
        register_text.raise_()

        #First Name
        firstname = QLabel(container)
        firstname.setPixmap(QPixmap("assets/Register/firstname.png"))
        firstname.setScaledContents(True)
        firstname.setGeometry(995, 195, 183, 28)
        firstname.raise_()
        
        self.firstname_input = QLineEdit(container)
        self.firstname_input.setPlaceholderText("First Name")
        self.firstname_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 35px;
                padding-left: 24px;
                padding-bottom: 3px;
                font-size: 32px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #007BFF;
            }
        """)
        self.firstname_input.setGeometry(995, 248, 843, 74)
        self.firstname_input.raise_()

        #Last Name
        lastname = QLabel(container)
        lastname.setPixmap(QPixmap("assets/Register/lastname.png"))
        lastname.setScaledContents(True)
        lastname.setGeometry(995, 358, 180, 28)
        lastname.raise_()
        
        self.lastname_input = QLineEdit(container)
        self.lastname_input.setPlaceholderText("Last Name")
        self.lastname_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 35px;
                padding-left: 24px;
                padding-bottom: 3px;
                font-size: 32px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #007BFF;
            }
        """)
        self.lastname_input.setGeometry(995, 407, 843, 74)
        self.lastname_input.raise_()

        #Username
        username = QLabel(container)
        username.setPixmap(QPixmap("assets/login/username.png"))
        username.setScaledContents(True)
        username.setGeometry(995, 513, 174, 28)
        username.raise_()
        
        self.username_input = QLineEdit(container)
        self.username_input.setPlaceholderText("Masukkan username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 35px;
                padding-left: 24px;
                padding-bottom: 3px;
                font-size: 32px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #007BFF;
            }
        """)
        self.username_input.setGeometry(995, 560, 843, 74)
        self.username_input.raise_()

        #Password
        password = QLabel(container)
        password.setPixmap(QPixmap("assets/login/password.png"))
        password.setScaledContents(True)
        password.setGeometry(995, 668, 169, 29)
        password.raise_()

        self.password_input = QLineEdit(container)
        self.password_input.setPlaceholderText("Masukkan password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 35px;
                padding-left: 24px;
                padding-bottom: 3px;
                font-size: 32px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #007BFF;
            }
        """)
        self.password_input.setGeometry(995, 715, 843, 74)
        self.password_input.raise_()

        self.toggle_password_btn = QPushButton(container)
        eye_icon = QIcon("assets/Login/icon_eye.png")
        self.toggle_password_btn.setIcon(eye_icon)
        self.toggle_password_btn.setIconSize(QSize(40, 40))
        self.toggle_password_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        self.toggle_password_btn.clicked.connect(self.eyeClicked)
        self.toggle_password_btn.setGeometry(1778, 732, 40, 40)
        self.toggle_password_btn.raise_()

        # Kembali ke Login
        back_to_login = QPushButton(container)
        back_to_login.setIconSize(QSize(463, 26))
        back_to_login.setStyleSheet("""
            QPushButton {
                border: none;
                background-image: url(assets/Register/Login.png);
                background-color: transparent;
            }
            QPushButton:hover {
                border: none;
                background-image: url(assets/Register/LoginHover.png);
                background-color: transparent;
            }
        """)
        back_to_login.clicked.connect(self._back_to_login)
        back_to_login.setGeometry(1369, 806, 463, 26)
        back_to_login.raise_()

        # Tombol Register
        register_button = QPushButton(container)
        register_button.setIconSize(QSize(745, 68))
        register_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-image: url(assets/Register/RegisterButton.png);
                background-color: transparent;
            }
            QPushButton:hover {
                border: none;
                background-image: url(assets/Register/RegisterButtonHover.png);
                background-color: transparent;
            }
        """)
        # Ubah koneksi ke fungsi _register
        register_button.clicked.connect(self._register)
        register_button.setGeometry(1044, 940, 745, 68)
        register_button.raise_()

        ## Elemen layer ##

        # Tambah widget ke layout utama
        main_layout.addWidget(container)

    def eyeClicked(self):
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.toggle_password_btn.setIcon(QIcon("assets/Login/icon_eye2.png"))
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.toggle_password_btn.setIcon(QIcon("assets/Login/icon_eye.png"))
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def _register(self):
        """Handle register button click"""
        if not self.register_viewmodel:
            QMessageBox.critical(self, "Error", "ViewModel not initialized")
            return

        # Ambil data dari input fields
        first_name = self.firstname_input.text()
        last_name = self.lastname_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        # Validasi input
        if not first_name or not last_name or not username or not password:
            QMessageBox.warning(self, "Registration Error", "Semua field harus diisi")
            return

        # Pada kode asli menggunakan email, tapi UI kita tidak memiliki email field
        # Jadi kita sesuaikan dengan mengirimkan first_name dan last_name sebagai pengganti email
        self.register_viewmodel.register_user(username, first_name, last_name, password)

    @pyqtSlot()
    def on_registration_success(self):
        """Handle successful registration"""
        QMessageBox.information(
            self, "Success", "Registrasi berhasil. Anda sekarang dapat login."
        )
        self._back_to_login()

    @pyqtSlot(str)
    def on_registration_failed(self, message):
        """Handle failed registration"""
        QMessageBox.warning(self, "Registration Error", message)

    def _back_to_login(self):
        """Return to login window"""
        if hasattr(self.parent_window, "show_login"):
            self.parent_window.show_login()