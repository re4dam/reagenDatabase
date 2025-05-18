# views/login_view.py
from PyQt6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
from PyQt6.QtCore import pyqtSlot, QSize
from PyQt6.QtGui import QPixmap, QIcon
from app_context import AppContext

class LoginView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SiMaLab")
        self.showMaximized()

        # Will be set through setup method
        self.login_viewmodel = None
        self.home_viewmodel = None

        # Create a stacked widget to manage different views
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create the login widget
        self.login_widget = QWidget()
        self._setup_login_ui()

        # Add login widget to stacked widget
        self.stacked_widget.addWidget(self.login_widget)

        # Initialize other widgets as None
        self.register_widget = None
        self.home_widget = None

    def setup_viewmodels(
        self, login_viewmodel, register_viewmodel=None, home_viewmodel=None
    ):
        """Connect to the viewmodels"""
        self.login_viewmodel = login_viewmodel
        self.register_viewmodel = register_viewmodel
        self.home_viewmodel = home_viewmodel

        # Connect signals from viewmodels
        if self.login_viewmodel:
            self.login_viewmodel.login_succeeded.connect(self.on_login_success)
            self.login_viewmodel.login_failed.connect(self.on_login_failed)

    def scale_rect(self, x, y, w, h):
        screen_size = AppContext.get_screen_resolution()
        scale_x = screen_size.width() / 1920
        scale_y = screen_size.height() / 1080
        return int(x * scale_x), int(y * scale_y), int(w * scale_x), int(h * scale_y)
    
    def scale_icon(self, w, h):
        screen_size = AppContext.get_screen_resolution()
        scale_x = screen_size.width() / 1920
        scale_y = screen_size.height() / 1080
        return int(w * scale_x), int(h * scale_y)
    
    def scale_style(self, px):
        screen_size = AppContext.get_screen_resolution()
        scale_y = screen_size.height() / 1080
        return int(px * scale_y)
    
    def _setup_login_ui(self):
        """Set up the UI components for the login page"""
        # Parent layout of login_widget
        layout = QVBoxLayout(self.login_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        screen_size = AppContext.get_screen_resolution()
        print(screen_size.width(), screen_size.height())

        # Create container widget to allow layering
        container = QWidget(self.login_widget)
        container.setGeometry(0, 0, screen_size.width(), screen_size.height())
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        ## Elemen layer ##
        #Background
        background_label = QLabel(container)
        background_label.setPixmap(QPixmap("assets/login/Login.png"))
        background_label.setScaledContents(True)
        background_label.setGeometry(0, 0, screen_size.width(), screen_size.height())

        # Foreground panel (main panel)
        panel_label = QLabel(container)
        panel_label.setPixmap(QPixmap("assets/login/Login2.png"))
        panel_label.setScaledContents(True)
        panel_label.setGeometry(*self.scale_rect(54, 23, 1812, 1012))
        panel_label.raise_()  # put it on top of background
        
        #Logo
        logo = QLabel(container)
        logo.setPixmap(QPixmap("assets/logo.png"))
        logo.setScaledContents(True)
        logo.setGeometry(*self.scale_rect(85, 50, 673, 93))
        logo.raise_()

        #Tulisan Login
        login_text = QLabel(container)
        login_text.setPixmap(QPixmap("assets/login/LoginText.png"))
        login_text.setScaledContents(True)
        login_text.setGeometry(*self.scale_rect(397, 232, 211, 51))
        login_text.raise_()

        #Tulisan Selamat Datang
        Welcome = QLabel(container)
        Welcome.setPixmap(QPixmap("assets/login/selamat_datang.png"))
        Welcome.setScaledContents(True)
        Welcome.setGeometry(*self.scale_rect(85, 352, 425, 52))
        Welcome.raise_()

        #Username
        username = QLabel(container)
        username.setPixmap(QPixmap("assets/login/username.png"))
        username.setScaledContents(True)
        username.setGeometry(*self.scale_rect(85, 445, 174, 28))
        username.raise_()
        
        self.username_input = QLineEdit(container)
        self.username_input.setPlaceholderText("Masukkan username")
        self.username_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid #ccc;
                border-radius: {self.scale_style(35)}px;
                padding-left: {self.scale_style(24)}px;
                padding-bottom: {self.scale_style(3)}px;
                font-size: {self.scale_style(32)}px;
                background-color: white;
            }}
            QLineEdit:focus {{
                border: 1px solid #007BFF;
            }}
        """)
        self.username_input.setGeometry(*self.scale_rect(85, 493, 843, 74))
        self.username_input.raise_()

        #Password
        password = QLabel(container)
        password.setPixmap(QPixmap("assets/login/password.png"))
        password.setScaledContents(True)
        password.setGeometry(*self.scale_rect(85, 609, 169, 29))
        password.raise_()

        self.password_input = QLineEdit(container)
        self.password_input.setPlaceholderText("Masukkan password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid #ccc;
                border-radius: {self.scale_style(35)}px;
                padding-left: {self.scale_style(24)}px;
                padding-bottom: {self.scale_style(3)}px;
                font-size: {self.scale_style(32)}px;
                background-color: white;
            }}
            QLineEdit:focus {{
                border: 1px solid #007BFF;
            }}
        """)
        self.password_input.setGeometry(*self.scale_rect(85, 662, 843, 74))
        self.password_input.raise_()

        self.toggle_password_btn = QPushButton(container)
        eye_icon = QIcon("assets/Login/icon_eye.png")
        self.toggle_password_btn.setIcon(eye_icon)
        self.toggle_password_btn.setIconSize(QSize(*self.scale_icon(40, 40)))
        self.toggle_password_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        self.toggle_password_btn.clicked.connect(self.eyeClicked)
        self.toggle_password_btn.setGeometry(*self.scale_rect(868, 680, 40, 40))
        self.toggle_password_btn.raise_()

        # Register
        register = QPushButton(container)
        icon_normal = QIcon("assets/Login/register.png")
        icon_hover = QIcon("assets/Login/register2.png")
        register.setIcon(icon_normal)
        register.setIconSize(QSize(*self.scale_icon(420, 26)))  # Ukuran ikon/gambar
        register.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        register.setGeometry(*self.scale_rect(500, 752, 420, 26))
        register.enterEvent = lambda event: register.setIcon(icon_hover)
        register.leaveEvent = lambda event: register.setIcon(icon_normal)
        register.clicked.connect(self._show_register)
        register.raise_()

        #Login
        login_toggle = QPushButton(container)
        login_normal = QIcon("assets/Login/LoginButton.png")
        login_hover = QIcon("assets/Login/LoginButtonHover.png")
        login_toggle.setIcon(login_normal)
        login_toggle.setIconSize(QSize(*self.scale_icon(745, 68)))
        login_toggle.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        # Perubahan penting: Mengganti koneksi dari on_login_success ke _login
        login_toggle.setGeometry(*self.scale_rect(134, 940, 745, 68))
        login_toggle.enterEvent = lambda event: login_toggle.setIcon(login_hover)
        login_toggle.leaveEvent = lambda event: login_toggle.setIcon(login_normal)
        login_toggle.clicked.connect(self._login)
        login_toggle.raise_()

        ## Elemen layer ##

        # Tambah widget ke layout utama
        layout.addWidget(container)
    
    def eyeClicked(self):
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.toggle_password_btn.setIcon(QIcon("assets/Login/icon_eye2.png"))
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.toggle_password_btn.setIcon(QIcon("assets/Login/icon_eye.png"))
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
    def _login(self):
        """Handle login button click"""
        if not self.login_viewmodel:
            QMessageBox.critical(self, "Error", "ViewModel not initialized")
            return

        username = self.username_input.text()
        password = self.password_input.text()

        # Validasi input sederhana
        if not username or not password:
            QMessageBox.warning(self, "Login Failed", "Username dan password tidak boleh kosong")
            return

        # Gunakan ViewModel untuk autentikasi
        self.login_viewmodel.authenticate(username, password)

    @pyqtSlot()
    def on_login_success(self):
        """Handle successful login"""
        try:
            # Switch to home view
            if self.home_viewmodel and self.home_viewmodel.create_home_view(self):
                # Set window title and size appropriate for main application
                self.setWindowTitle("SiMaLab")
            else:
                QMessageBox.warning(self, "Error", "Could not open home view")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open home view: {str(e)}")

    @pyqtSlot(str)
    def on_login_failed(self, message):
        """Handle failed login"""
        QMessageBox.warning(self, "Login Failed", message)

    def _show_register(self):
        """Show the register widget"""
        if self.register_viewmodel:
            self.register_viewmodel.show_register_view(self)

    def show_login(self):
        """Switch back to the login widget"""
        # Reset window title and size for login view
        self.setWindowTitle("SiMaLab")

        # Clear sensitive data
        self.username_input.clear()
        self.password_input.clear()

        # Switch to login widget
        self.stacked_widget.setCurrentWidget(self.login_widget)
    
    def show_home(self):
        """Switch to the home widget if it exists"""
        if self.home_widget and self.stacked_widget:
            self.stacked_widget.setCurrentWidget(self.home_widget)