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
    QGraphicsOpacityEffect,
)
from PyQt6.QtCore import pyqtSlot, QSize, QPropertyAnimation, QSequentialAnimationGroup, QParallelAnimationGroup, QEasingCurve, QPoint
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
        self.firstOpenAnimation()

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
    
    def scale_point(self, x, y):
        screen_size = AppContext.get_screen_resolution()
        scale_x = screen_size.width() / 1920
        scale_y = screen_size.height() / 1080
        return int(x * scale_x), int(y * scale_y)
    
    def scale_style(self, px):
        screen_size = AppContext.get_screen_resolution()
        scale_y = screen_size.height() / 1080
        return int(px * scale_y)
    
    def firstOpenAnimation(self):
        self.sequence = QSequentialAnimationGroup(self)

        self.bg_animation = QPropertyAnimation(self.background_label_effect, b"opacity")
        self.bg_animation.setDuration(500)
        self.bg_animation.setStartValue(0.0)
        self.bg_animation.setEndValue(1.0)
        self.bg_animation.setEasingCurve(QEasingCurve.Type.OutExpo)

        start_panel_x, start_panel_y, _, _, = self.scale_rect(54, 1102, 1812, 1012)
        target_panel_x, target_panel_y, _, _, = self.scale_rect(54, 22, 1812, 1012)
        self.panel_animation = QPropertyAnimation(self.panel_main, b"pos")
        self.panel_animation.setDuration(750)
        self.panel_animation.setStartValue(QPoint(start_panel_x, start_panel_y))
        self.panel_animation.setEndValue(QPoint(target_panel_x, target_panel_y))
        self.panel_animation.setEasingCurve(QEasingCurve.Type.OutBack)

        self.sequence.addAnimation(self.bg_animation)
        self.sequence.addAnimation(self.panel_animation)
        self.sequence.start()

    def OutTransition(self):
        self.sequence = QParallelAnimationGroup(self)

        self.bg_animation = QPropertyAnimation(self.background_label_effect, b"opacity")
        self.bg_animation.setDuration(750)
        self.bg_animation.setStartValue(0.0)
        self.bg_animation.setEndValue(1.0)
        self.bg_animation.setEasingCurve(QEasingCurve.Type.InExpo)

        start_prevpanel_x, start_prevpanel_y, _, _, = self.scale_rect(54, 22, 1812, 1012)
        target_prevpanel_x, target_prevpanel_y, _, _, = self.scale_rect(1974, 22, 1812, 1012)
        self.prevpanel_animation = QPropertyAnimation(self.prevpanel_label, b"pos")
        self.prevpanel_animation.setDuration(1500)
        self.prevpanel_animation.setStartValue(QPoint(start_prevpanel_x, start_prevpanel_y))
        self.prevpanel_animation.setEndValue(QPoint(target_prevpanel_x, target_prevpanel_y))
        self.prevpanel_animation.setEasingCurve(QEasingCurve.Type.InOutBack)

        start_panel_x, start_panel_y, _, _, = self.scale_rect(-1866, 22, 1812, 1012)
        target_panel_x, target_panel_y, _, _, = self.scale_rect(54, 22, 1812, 1012)
        self.panel_animation = QPropertyAnimation(self.panel_main, b"pos")
        self.panel_animation.setDuration(1500)
        self.panel_animation.setStartValue(QPoint(start_panel_x, start_panel_y))
        self.panel_animation.setEndValue(QPoint(target_panel_x, target_panel_y))
        self.panel_animation.setEasingCurve(QEasingCurve.Type.InOutBack)

        self.sequence.addAnimation(self.bg_animation)
        self.sequence.addAnimation(self.prevpanel_animation)
        self.sequence.addAnimation(self.panel_animation)
        self.sequence.start()

    def _setup_login_ui(self):
        """Set up the UI components for the login page"""
        # Parent layout of login_widget
        screen_size = AppContext.get_screen_resolution()
        print(screen_size.width(), screen_size.height())

        # Create container widget to allow layering
        container = QWidget(self.login_widget)
        container.setGeometry(0, 0, screen_size.width(), screen_size.height())
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        ## Elemen layer ##

        #Prev Background
        self.prevbackground_label = QLabel(container)
        self.prevbackground_label.setPixmap(QPixmap("assets/Login/Register_bg.png"))
        self.prevbackground_label.setScaledContents(True)
        self.prevbackground_label.setGeometry(0, 0, screen_size.width(), screen_size.height())
        self.prevbackground_label_effect = QGraphicsOpacityEffect(self.prevbackground_label)
        self.prevbackground_label.setGraphicsEffect(self.prevbackground_label_effect)
        self.prevbackground_label_effect.setOpacity(0.0)

        #Background
        self.background_label = QLabel(container)
        self.background_label.setPixmap(QPixmap("assets/login/Login.png"))
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, screen_size.width(), screen_size.height())
        self.background_label_effect = QGraphicsOpacityEffect(self.background_label)
        self.background_label.setGraphicsEffect(self.background_label_effect)
        self.background_label_effect.setOpacity(0.0)

        # Prev Foreground panel
        self.prevpanel_label = QLabel(container)
        self.prevpanel_label.setPixmap(QPixmap("assets/Login/register_panel.png"))
        self.prevpanel_label.setScaledContents(True)
        self.prevpanel_label.setGeometry(*self.scale_rect(54, 22, 1812, 1012))
        self.prevpanel_label_effect = QGraphicsOpacityEffect(self.prevpanel_label)
        self.prevpanel_label.setGraphicsEffect(self.prevpanel_label_effect)
        self.prevpanel_label_effect.setOpacity(0.0)

        self.panel_main = QWidget(container)
        self.panel_main.setGeometry(*self.scale_rect(54, 1102, 1812, 1012))

        # Foreground panel (main panel)
        panel_label = QLabel(self.panel_main)
        panel_label.setPixmap(QPixmap("assets/login/Login2.png"))
        panel_label.setScaledContents(True)
        panel_label.setGeometry(*self.scale_rect(0, 0, 1812, 1012))
        
        #Logo
        logo = QLabel(self.panel_main)
        logo.setPixmap(QPixmap("assets/logo.png"))
        logo.setScaledContents(True)
        logo.setGeometry(*self.scale_rect(31, 27, 673, 93))

        #Tulisan Login
        login_text = QLabel(self.panel_main)
        login_text.setPixmap(QPixmap("assets/login/LoginText.png"))
        login_text.setScaledContents(True)
        login_text.setGeometry(*self.scale_rect(343, 209, 211, 51))

        #Tulisan Selamat Datang
        Welcome = QLabel(self.panel_main)
        Welcome.setPixmap(QPixmap("assets/login/selamat_datang.png"))
        Welcome.setScaledContents(True)
        Welcome.setGeometry(*self.scale_rect(31, 329, 425, 52))

        #Username
        username = QLabel(self.panel_main)
        username.setPixmap(QPixmap("assets/login/username.png"))
        username.setScaledContents(True)
        username.setGeometry(*self.scale_rect(31, 422, 174, 28))
        
        self.username_input = QLineEdit(self.panel_main)
        self.username_input.setPlaceholderText("Masukkan username")
        self.username_input.setStyleSheet(f"""
            QLineEdit {{
                color: black;
                border: 1px solid #ccc;
                border-radius: {self.scale_style(35)}px;
                padding-left: {self.scale_style(24)}px;
                padding-right: {self.scale_style(24)}px;
                padding-bottom: {self.scale_style(3)}px;
                font-size: {self.scale_style(32)}px;
                background-color: white;
            }}
            QLineEdit:focus {{
                border: 1px solid #007BFF;
            }}
        """)
        self.username_input.setGeometry(*self.scale_rect(31, 470, 843, 74))

        #Password
        password = QLabel(self.panel_main)
        password.setPixmap(QPixmap("assets/login/password.png"))
        password.setScaledContents(True)
        password.setGeometry(*self.scale_rect(31, 586, 169, 29))

        self.password_input = QLineEdit(self.panel_main)
        self.password_input.setPlaceholderText("Masukkan password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                color: black;
                border: 1px solid #ccc;
                border-radius: {self.scale_style(35)}px;
                padding-left: {self.scale_style(24)}px;
                padding-right: {self.scale_style(65)}px;
                padding-bottom: {self.scale_style(3)}px;
                font-size: {self.scale_style(32)}px;
                background-color: white;
            }}
            QLineEdit:focus {{
                border: 1px solid #007BFF;
            }}
        """)
        self.password_input.setGeometry(*self.scale_rect(31, 639, 843, 74))

        self.toggle_password_btn = QPushButton(self.panel_main)
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
        self.toggle_password_btn.setGeometry(*self.scale_rect(814, 657, 40, 40))

        # Register
        register = QPushButton(self.panel_main)
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
        register.setGeometry(*self.scale_rect(446, 729, 420, 26))
        register.enterEvent = lambda event: register.setIcon(icon_hover)
        register.leaveEvent = lambda event: register.setIcon(icon_normal)
        register.clicked.connect(self._show_register)

        #Login
        login_toggle = QPushButton(self.panel_main)
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
        login_toggle.setGeometry(*self.scale_rect(80, 917, 745, 68))
        login_toggle.enterEvent = lambda event: login_toggle.setIcon(login_hover)
        login_toggle.leaveEvent = lambda event: login_toggle.setIcon(login_normal)
        login_toggle.clicked.connect(self._login)
    
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

    @pyqtSlot(int)
    def on_login_success(self, user_id):
        self.panel_main.setGeometry(*self.scale_rect(-1866, 22, 1812, 1012))
        """Handle successful login"""
        try:
            # Set the user ID in the home viewmodel
            if self.home_viewmodel:
                self.home_viewmodel.set_current_user_id(user_id)

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
        self.panel_main.setGeometry(*self.scale_rect(-1866, 22, 1812, 1012))
        self.prevbackground_label_effect.setOpacity(1.0)
        self.prevpanel_label_effect.setOpacity(1.0)

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
        
        self.prevpanel_label.setGeometry(*self.scale_rect(54, 22, 1812, 1012))
        self.OutTransition()

        # Switch to login widget
        self.stacked_widget.setCurrentWidget(self.login_widget)

    def show_login_from_home(self):
        """Switch back to the login widget"""
        # Reset window title and size for login view
        self.setWindowTitle("SiMaLab")

        # Clear sensitive data
        self.username_input.clear()
        self.password_input.clear()
        
        self.panel_main.setGeometry(*self.scale_rect(54, 1102, 1812, 1012))
        self.firstOpenAnimation()

        # Switch to login widget
        self.stacked_widget.setCurrentWidget(self.login_widget)
    
    def show_home(self):
        """Switch to the home widget if it exists"""
        if self.home_widget and self.stacked_widget:
            self.stacked_widget.setCurrentWidget(self.home_widget)