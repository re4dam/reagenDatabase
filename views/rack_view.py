from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QMessageBox,
    QLabel,
    QHBoxLayout,
    QFrame,
    QScrollArea,
    QStackedLayout,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, pyqtSlot, QSize, QPropertyAnimation, QSequentialAnimationGroup, QParallelAnimationGroup, QEasingCurve, QPoint, QTimer
from PyQt6.QtGui import QPixmap, QFont, QIcon, QRegion, QPainterPath, QColor
from views.reagent_view import ReagentDetailPanel
from app_context import AppContext
from load_font import FontManager


class RackView(QWidget):
    def __init__(self, parent=None, storage_id=None):
        super().__init__(parent)
        self.parent_window = parent
        self.rack_viewmodel = None
        self.reagents = []
        self.current_page = 0
        self.items_per_page = 10
        self.storage_id = storage_id
        self.is_page_sliding = False
        self.current_slide_out_animation = None
        self.current_slide_in_animation = None

        self._current_detail_panel_came_from_search = (
            False  # Store context for ReagentDetailPanel
        )
        self.active_usage_report_view = (
            None  # To manage the active UsageReportView instance
        )

        # Create stacked layout
        self.main_stack = QStackedLayout()
        self._setup_rack_ui()
        self.mainAnimation()

        # Set main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(self.main_stack)

    def set_viewmodel(self, viewmodel):
        """Set the ViewModel for this view"""
        self.rack_viewmodel = viewmodel

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
    
    def mainAnimation(self):
        self.sequence = QParallelAnimationGroup(self)

        start_foreground_x, start_foreground_y, _, _, = self.scale_rect(89, 1220, 1742, 861)
        target_foreground_x, target_foreground_y, _, _, = self.scale_rect(89, 140, 1742, 861)
        foreground_animation = QPropertyAnimation(self.foreground, b"pos")
        foreground_animation.setDuration(750)
        foreground_animation.setStartValue(QPoint(start_foreground_x, start_foreground_y))
        foreground_animation.setEndValue(QPoint(target_foreground_x, target_foreground_y))
        foreground_animation.setEasingCurve(QEasingCurve.Type.OutBack)
        self.sequence.addAnimation(foreground_animation)

        scroll_content_effect_animation = QPropertyAnimation(self.scroll_content_effect, b"opacity")
        scroll_content_effect_animation.setDuration(500)
        scroll_content_effect_animation.setStartValue(0.0)
        scroll_content_effect_animation.setEndValue(1.0)
        scroll_content_effect_animation.setEasingCurve(QEasingCurve.Type.InQuad)
        self.sequence.addAnimation(scroll_content_effect_animation)

        start_add_reagen_button_x, start_add_reagen_button_y, _, _, = self.scale_rect(1722, 1945, 174, 174)
        target_add_reagen_button_x, target_add_reagen_button_y, _, _, = self.scale_rect(1722, 865, 174, 174)
        add_reagen_button_animation = QPropertyAnimation(self.add_reagent_button, b"pos")
        add_reagen_button_animation.setDuration(750)
        add_reagen_button_animation.setStartValue(QPoint(start_add_reagen_button_x, start_add_reagen_button_y))
        add_reagen_button_animation.setEndValue(QPoint(target_add_reagen_button_x, target_add_reagen_button_y))
        add_reagen_button_animation.setEasingCurve(QEasingCurve.Type.OutBack)
        self.sequence.addAnimation(add_reagen_button_animation)

        self.sequence.start()

    def _setup_rack_ui(self):
        """Set up the UI components for the rack view"""
        # Create rack panel
        self.rack_panel = QWidget()
        rack_layout = QVBoxLayout(self.rack_panel)
        rack_layout.setContentsMargins(0, 0, 0, 0)
        screen_size = AppContext.get_screen_resolution()

        # Create container widget for layering
        container = QWidget(self.rack_panel)
        container.setGeometry(0, 0, screen_size.width(), screen_size.height())
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        # Background layer - Lab image
        background_label = QLabel(container)
        background_label.setPixmap(
            QPixmap("assets/Rack/background.png")
        )  # Use your actual image path
        background_label.setScaledContents(True)
        background_label.setGeometry(0, 0, screen_size.width(), screen_size.height())
        background_label.lower()

        # Drop Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)
        shadow.setOffset(5, 7)
        shadow.setColor(QColor(0, 0, 0, 165))

        # Title
        title_label = QLabel(container)
        self.rack_title = title_label  # Will be updated when data loads
        title_label.setGeometry(0, 0, screen_size.width(), 132)
        title_label.setFont(
            FontManager.get_font("PlusJakartaSans-Regular", self.scale_style(60))
        )
        title_label.setStyleSheet("""
            QLabel{
                font-weight: bold;
                color: white;         
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title_label.setGraphicsEffect(shadow)
        title_label.raise_()

        # Foreground
        self.foreground = QLabel(container)
        self.foreground.setPixmap(
            QPixmap("assets/Rack/foreground.png")
        )  # Use your actual image path
        self.foreground.setScaledContents(True)
        self.foreground.setGeometry(*self.scale_rect(89, 140, 1742, 861))
        self.foreground.raise_()

        # Scrollable grid
        self.scroll_area = QScrollArea(container)
        self.scroll_content = QWidget()
        self.scroll_content_effect = QGraphicsOpacityEffect(self.scroll_content)
        self.scroll_content.setGraphicsEffect(self.scroll_content_effect)
        self.scroll_content_effect.setOpacity(0.0)
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setSpacing(15)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setGeometry(*self.scale_rect(99, 140, 1722, 861))
        self.scroll_area.setStyleSheet("border: none; background: transparent;")
        self.scroll_area.raise_()

        self.add_reagent_button = QPushButton(container)
        add_normal = QIcon("assets/Rack/add.png")
        add_hover = QIcon("assets/Rack/add_hover.png")
        self.add_reagent_button.setIcon(add_normal)
        self.add_reagent_button.setIconSize(QSize(*self.scale_icon(174, 174)))
        self.add_reagent_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
        """)
        self.add_reagent_button.setGeometry(*self.scale_rect(1722, 865, 174, 174))
        self.add_reagent_button.enterEvent = (
            lambda event: self.add_reagent_button.setIcon(add_hover)
        )
        self.add_reagent_button.leaveEvent = (
            lambda event: self.add_reagent_button.setIcon(add_normal)
        )
        self.add_reagent_button.clicked.connect(self._add_new_reagent)
        self.add_reagent_button.raise_()

        self.prev_button = QPushButton(container)
        icon_prev = QIcon("assets/Rack/back.png")
        self.prev_button.setIcon(icon_prev)
        self.prev_button.setIconSize(QSize(*self.scale_icon(57, 88)))
        self.prev_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        self.prev_button.clicked.connect(self._go_to_previous_page)
        self.prev_button.setGeometry(*self.scale_rect(13, 525, 57, 88))
        self.prev_button.raise_()

        self.page_label = QLabel(container)
        self.page_label.setFont(FontManager.get_font("PlusJakartaSans-Regular", 24))
        self.page_label.setStyleSheet("color: white;")
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_label.setFixedSize(QSize(*self.scale_icon(150, 150)))
        self.page_label.move(*self.scale_icon(895, 880))
        self.page_label.raise_()

        self.next_button = QPushButton(container)
        icon_next = QIcon("assets/Rack/next.png")
        self.next_button.setIcon(icon_next)
        self.next_button.setIconSize(QSize(*self.scale_icon(57, 88)))
        self.next_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        self.next_button.clicked.connect(self._go_to_next_page)
        self.next_button.setGeometry(*self.scale_rect(1848, 525, 57, 88))
        self.next_button.raise_()

        # Add circular back button in top-left corner
        self.back_button = QPushButton(container)
        back_normal = QIcon("assets/Rack/icon_back.png")
        back_hover = QIcon("assets/Rack/back_hover.png")
        self.back_button.setIcon(back_normal)
        self.back_button.setIconSize(QSize(*self.scale_icon(130, 130)))
        self.back_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        # Perubahan penting: Mengganti koneksi dari on_login_success ke _login
        self.back_button.setGeometry(*self.scale_rect(12, 12, 130, 130))
        self.back_button.enterEvent = lambda event: self.back_button.setIcon(back_hover)
        self.back_button.leaveEvent = lambda event: self.back_button.setIcon(
            back_normal
        )
        self.back_button.clicked.connect(self._go_back)
        self.back_button.raise_()

        rack_layout.addWidget(container)
        # Add rack panel to stack
        self.main_stack.addWidget(self.rack_panel)

    @pyqtSlot(list, str)
    def on_reagents_loaded(self, reagents, rack_name):
        """Handle loaded reagents data"""
        self.reagents = reagents
        self.rack_title.setText(f"{rack_name}")
        self.current_page = 0
        self._load_current_page()
    
    def _disable_navigation_during_slide(self):
        print("DEBUG: _disable_navigation_during_slide called")
        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(False)
        if hasattr(self, 'add_reagent_button'):
            self.add_reagent_button.setEnabled(False)
        
        # Nonaktifkan juga tombol reagen di grid
        for i in range(self.grid_layout.count()):
            widget_item = self.grid_layout.itemAt(i)
            if widget_item:
                widget = widget_item.widget()
                if widget:
                    widget.setEnabled(False)

    def _finish_page_slide(self):
        print("DEBUG: _finish_page_slide called")
        self.is_page_sliding = False # Reset flag SEGERA
        self._update_navigation_buttons() # Ini akan mengaktifkan prev/next sesuai kondisi
        if hasattr(self, 'add_reagent_button'):
            self.add_reagent_button.setEnabled(True)
        
        # Aktifkan kembali tombol reagen di grid
        for i in range(self.grid_layout.count()):
            widget_item = self.grid_layout.itemAt(i)
            if widget_item:
                widget = widget_item.widget()
                if widget:
                    widget.setEnabled(True)
        print("DEBUG: Navigation and reagent buttons state updated.")

    def _go_to_next_page(self):
        print(f"DEBUG: _go_to_next_page called. Current page: {self.current_page}, is_sliding: {self.is_page_sliding}, total_pages: {self._total_pages()}")
        if self.is_page_sliding or not (self.current_page < self._total_pages() - 1):
            print("DEBUG: Next page navigation aborted (sliding or at end).")
            return

        self.is_page_sliding = True
        self._disable_navigation_during_slide()

        scroll_width = self.scroll_area.width()
        print(f"DEBUG: Scroll area width for next page slide: {scroll_width}")
        if scroll_width <= 0:
            print("ERROR: Scroll area width is zero or negative! Aborting animation for next page.")
            self._finish_page_slide() # Coba pulihkan state UI
            return

        # Animasi geser keluar ke kiri
        slide_out_anim = QPropertyAnimation(self.scroll_content, b"pos", self) # Tambahkan self sebagai parent
        slide_out_anim.setDuration(750)
        slide_out_anim.setStartValue(self.scroll_content.pos()) # Ambil posisi saat ini (seharusnya 0,0)
        slide_out_anim.setEndValue(QPoint(-scroll_width, 0))
        slide_out_anim.setEasingCurve(QEasingCurve.Type.InOutBack)

        slide_out_anim.finished.connect(self._prepare_next_page_for_slide_in)
        print("DEBUG: Starting slide_out_anim for next page.")
        slide_out_anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped) # Hapus saat berhenti

    def _prepare_next_page_for_slide_in(self):
        print(f"DEBUG: [PREPARE_NEXT] Halaman saat ini sebelum increment: {self.current_page}")
        self.current_page += 1
        
        scroll_width = self.scroll_area.width()

        # 1. Pindahkan dulu ke posisi awal slide-in (kanan luar layar) SAAT MASIH INVISIBLE
        #    Ini penting agar saat _load_current_page, widget sudah di posisi yang benar
        #    jika ada kalkulasi layout internal yang bergantung pada posisi parent.
        self.scroll_content.move(scroll_width, self.scroll_content.pos().y())
        print(f"DEBUG: [PREPARE_NEXT] scroll_content dipindah ke {self.scroll_content.pos()} (sebelum load, masih invisible)")
        
        # 2. Sembunyikan scroll_content SEBELUM memuat item baru jika belum disembunyikan
        #    Ini untuk mencegah item-item baru tergambar prematur.
        self.scroll_content.setVisible(False)
        
        try:
            print("DEBUG: [PREPARE_NEXT] Memuat item halaman baru...")
            self._load_current_page() # Update konten dan label halaman
            print(f"DEBUG: [PREPARE_NEXT] Halaman {self.current_page + 1} dimuat. Label halaman: {self.page_label.text()}")
        except Exception as e:
            print(f"ERROR saat _load_current_page di _prepare_next_page_for_slide_in: {e}")
            # Pulihkan keadaan jika error
            self.scroll_content.move(0, self.scroll_content.pos().y()) 
            self.scroll_content.setVisible(True) 
            self._finish_page_slide() 
            return
            
        # 3. Setelah konten dimuat dan widget masih di posisi kanan luar layar,
        #    BARU buat dia visible.
        self.scroll_content.setVisible(True)
        print("DEBUG: [PREPARE_NEXT] scroll_content visible kembali di posisi slide-in (kanan luar layar).")

        # 4. Mulai animasi slide-in
        self.current_slide_in_animation = QPropertyAnimation(self.scroll_content, b"pos", self)
        self.current_slide_in_animation.setDuration(400) # Durasi slide-in yang sudah disesuaikan
        self.current_slide_in_animation.setStartValue(self.scroll_content.pos()) 
        self.current_slide_in_animation.setEndValue(QPoint(0, self.scroll_content.pos().y())) 
        self.current_slide_in_animation.setEasingCurve(QEasingCurve.Type.OutBack)

        try: self.current_slide_in_animation.finished.disconnect()
        except TypeError: pass
        self.current_slide_in_animation.finished.connect(self._finish_page_slide)
        
        print("DEBUG: [PREPARE_NEXT] Memulai animasi geser masuk...")
        self.current_slide_in_animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    def _go_to_previous_page(self):
        print(f"DEBUG: _go_to_previous_page called. Current page: {self.current_page}, is_sliding: {self.is_page_sliding}")
        if self.is_page_sliding or not (self.current_page > 0):
            print("DEBUG: Previous page navigation aborted (sliding or at start).")
            return

        self.is_page_sliding = True
        self._disable_navigation_during_slide()

        scroll_width = self.scroll_area.width()
        print(f"DEBUG: Scroll area width for previous page slide: {scroll_width}")
        if scroll_width <= 0:
            print("ERROR: Scroll area width is zero or negative! Aborting animation for previous page.")
            self._finish_page_slide() # Coba pulihkan state UI
            return

        # Animasi geser keluar ke kanan
        slide_out_anim = QPropertyAnimation(self.scroll_content, b"pos", self) # Tambahkan self sebagai parent
        slide_out_anim.setDuration(750)
        slide_out_anim.setStartValue(self.scroll_content.pos()) # Ambil posisi saat ini
        slide_out_anim.setEndValue(QPoint(scroll_width, 0))
        slide_out_anim.setEasingCurve(QEasingCurve.Type.InOutBack)

        slide_out_anim.finished.connect(self._prepare_prev_page_for_slide_in)
        print("DEBUG: Starting slide_out_anim for previous page.")
        slide_out_anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    def _prepare_prev_page_for_slide_in(self):
        print(f"DEBUG: [PREPARE_PREV] Halaman saat ini sebelum decrement: {self.current_page}")
        self.current_page -= 1

        scroll_width = self.scroll_area.width()

        # 1. Pindahkan dulu ke posisi awal slide-in (kiri luar layar) SAAT MASIH INVISIBLE
        self.scroll_content.move(-scroll_width, self.scroll_content.pos().y())
        print(f"DEBUG: [PREPARE_PREV] scroll_content dipindah ke {self.scroll_content.pos()} (sebelum load, masih invisible)")

        # 2. Sembunyikan scroll_content SEBELUM memuat item baru
        self.scroll_content.setVisible(False)

        try:
            print("DEBUG: [PREPARE_PREV] Memuat item halaman baru...")
            self._load_current_page()
            print(f"DEBUG: [PREPARE_PREV] Halaman {self.current_page + 1} dimuat. Label halaman: {self.page_label.text()}")
        except Exception as e:
            print(f"ERROR saat _load_current_page di _prepare_prev_page_for_slide_in: {e}")
            self.scroll_content.move(0, self.scroll_content.pos().y())
            self.scroll_content.setVisible(True)
            self._finish_page_slide()
            return
            
        # 3. Setelah konten dimuat dan widget masih di posisi kiri luar layar,
        #    BARU buat dia visible.
        self.scroll_content.setVisible(True)
        print("DEBUG: [PREPARE_PREV] scroll_content visible kembali di posisi slide-in (kiri luar layar).")

        # 4. Mulai animasi slide-in
        self.current_slide_in_animation = QPropertyAnimation(self.scroll_content, b"pos", self)
        self.current_slide_in_animation.setDuration(400) # Durasi slide-in yang sudah disesuaikan
        self.current_slide_in_animation.setStartValue(self.scroll_content.pos()) 
        self.current_slide_in_animation.setEndValue(QPoint(0, self.scroll_content.pos().y()))
        self.current_slide_in_animation.setEasingCurve(QEasingCurve.Type.OutBack)

        try: self.current_slide_in_animation.finished.disconnect()
        except TypeError: pass
        self.current_slide_in_animation.finished.connect(self._finish_page_slide)
        
        print("DEBUG: [PREPARE_PREV] Memulai animasi geser masuk...")
        self.current_slide_in_animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    def _load_current_page(self):
        """Load current page of reagents"""
        # Clear grid
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Load current page
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.reagents))

        for i in range(start_idx, end_idx):
            reagent = self.reagents[i]
            button = QPushButton()
            button.setMinimumHeight(70)
            button.setText(
                f"{reagent.get('Name')}\n{reagent.get('Wujud')}\nStock: {reagent.get('Stock')}"
            )
            button.setStyleSheet(
                self._get_button_style_for_hazard(reagent.get("Category_Hazard", "Low"))
            )
            button.clicked.connect(
                lambda checked, r_id=reagent["id"]: self._view_reagent_details(r_id)
            )

            relative_idx = i - start_idx
            self.grid_layout.addWidget(button, relative_idx // 5, relative_idx % 5)

        self.page_label.setText(f"{self.current_page + 1} / {self._total_pages()}")
        self._update_navigation_buttons()

    def _get_button_style_for_hazard(self, hazard_category):
        """Return button style based on hazard category"""
        if hazard_category in ["High", "Extreme"]:
            return "QPushButton { background-color: #ffcccc; border: 2px solid #ff6666; color: black;} QPushButton:hover { background-color: #ffaaaa; }"
        elif hazard_category == "Medium":
            return "QPushButton { background-color: #fff2cc; border: 2px solid #ffcc66; color: black;} QPushButton:hover { background-color: #ffebaa; }"
        else:
            return "QPushButton { background-color: #e6f2ff; border: 2px solid #99ccff; color: black;} QPushButton:hover { background-color: #cce6ff; }"

    def _total_pages(self):
        return max(
            1, (len(self.reagents) + self.items_per_page - 1) // self.items_per_page
        )

    def _update_navigation_buttons(self):
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < self._total_pages() - 1)

    def _view_reagent_details(self, reagent_id):
        if self.rack_viewmodel:
            self.rack_viewmodel.show_reagent_details(reagent_id)

    def _add_new_reagent(self):
        if self.rack_viewmodel:
            self.rack_viewmodel.add_new_reagent()

    def remove_self_from_parent_stack(self):
        """Removes this RackView instance from its parent's QStackedWidget and clears its cache."""
        if self.parent_window and hasattr(self.parent_window, "stacked_widget"):
            self.parent_window.stacked_widget.removeWidget(self)

            # Also remove the cached attribute from parent_window
            if self.storage_id is not None:  # Check if storage_id was set
                view_key = f"rack_view_{self.storage_id}"
                if hasattr(self.parent_window, view_key):
                    try:
                        delattr(self.parent_window, view_key)
                        print(
                            f"Cleared cache key {view_key} from {self.parent_window.__class__.__name__}"
                        )
                    except AttributeError:
                        print(
                            f"Warning: Could not delete attribute {view_key} from {self.parent_window.__class__.__name__}"
                        )
            else:
                print(
                    "Warning: RackView.storage_id not set, cannot clear cache attribute by key."
                )

            self.deleteLater()  # Schedule RackView for deletion
            print(
                f"RackView for storage_id {self.storage_id} removed from stack and scheduled for deletion."
            )

    def _go_back(self):  # This is for RackView's own "Back to Home" button
        if self.parent_window:
            # If RackView's parent is LoginView (came from search), show_home on LoginView should show HomeView
            # If RackView's parent is HomeView (came from home), show_home on HomeView shows its main panel
            if hasattr(self.parent_window, "show_home"):
                self.parent_window.show_home()
            # If RackView was on LoginView's stack, show_home should ideally remove it.
            # This might need further refinement in LoginView.show_home() if RackViews are not cleaned up.
            # However, for the specific user request, remove_self_from_parent_stack handles the cleanup.

    def show_rack_view(self):
        """Switch back to rack view from detail view"""
        self.main_stack.setCurrentWidget(self.rack_panel)
        if self.rack_viewmodel:
            self.rack_viewmodel.load_reagents()

    def show_usage_reports(
        self, reagent_id, reagent_name, came_from_search_context=False
    ):  # Accept new flag
        """Show the usage reports for a specific reagent."""
        # Store the context of how the ReagentDetailPanel that triggered this was opened
        self._current_detail_panel_came_from_search = came_from_search_context
        print(
            f"RackView: Stored came_from_search_context = {self._current_detail_panel_came_from_search}"
        )

        if self.rack_viewmodel:
            try:
                usage_model = self.rack_viewmodel.get_usage_model()
                identity_model = self.rack_viewmodel.get_identity_model()

                if not usage_model or not identity_model:
                    QMessageBox.warning(
                        self,
                        "Missing Models",
                        "Cannot access usage or identity models.",
                    )
                    return

                from views.usage_report_view import UsageReportView  # Import here
                main_stack_owner = self.parent_window  # This is LoginView or HomeView

                # Clean up any previously active usage report view shown by this RackView instance
                if self.active_usage_report_view is not None:
                    print(self.active_usage_report_view)
                    if hasattr(main_stack_owner, "stacked_widget"):
                        main_stack_owner.stacked_widget.removeWidget(
                            self.active_usage_report_view
                        )
                    self.active_usage_report_view.deleteLater()
                    self.active_usage_report_view = None

                # Create the new usage report view
                # The parent of UsageReportView is 'self' (RackView)
                self.active_usage_report_view = UsageReportView(
                    usage_model, identity_model, reagent_id, reagent_name, parent=self
                )

                # Connect signals for the new UsageReportView instance
                self.active_usage_report_view.back_clicked.connect(
                    lambda r_id=reagent_id: self._return_to_reagent_detail(r_id),
                )
                self.active_usage_report_view.add_report_clicked.connect(
                    self.show_new_usage_report
                )
                self.active_usage_report_view.edit_report_clicked.connect(
                    self.show_edit_usage_report
                )

                # Add and show the UsageReportView on the main application stack
                if hasattr(main_stack_owner, "stacked_widget"):
                    main_stack_owner.stacked_widget.addWidget(
                        self.active_usage_report_view
                    )
                    main_stack_owner.stacked_widget.setCurrentWidget(
                        self.active_usage_report_view
                    )
                    # ---- PEMANGGILAN ANIMASI MASUK untuk UsageReportView ----
                    if hasattr(self.active_usage_report_view, "mainAnimation"):
                        print("DEBUG: RackView - Scheduling mainAnimation for UsageReportView")
                        
                        def trigger_report_animation():
                            if self.active_usage_report_view and \
                            self.active_usage_report_view.isVisible() and \
                            main_stack_owner.stacked_widget.currentWidget() == self.active_usage_report_view:
                                print("DEBUG: Triggering mainAnimation for visible UsageReportView")
                                self.active_usage_report_view.mainAnimation()
                            else:
                                print("DEBUG: UsageReportView tidak valid/visible/current saat timer, animasi tidak dijalankan.")

                        QTimer.singleShot(50, trigger_report_animation)
                else:
                    QMessageBox.critical(
                        self,
                        "Error",
                        "No stacked_widget found in parent window for UsageReportView.",
                    )

            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to show usage reports: {str(e)}"
                )

    def show_new_usage_report(self, reagent_id, reagent_name):
        """Show panel to add a new usage report"""
        if self.rack_viewmodel:
            self.rack_viewmodel.show_new_usage_report(reagent_id, reagent_name)

    def show_edit_usage_report(self, report_id, reagent_id, reagent_name):
        """Show panel to edit an existing usage report"""
        if self.rack_viewmodel:
            self.rack_viewmodel.show_edit_usage_report(
                report_id, reagent_id, reagent_name
            )

    def _return_to_reagent_detail(self, reagent_id):
        """Handles back navigation from UsageReportView to ReagentDetailPanel."""
        main_stack_owner = self.parent_window  # LoginView or HomeView

        # Clean up the active UsageReportView from the main stack
        if self.active_usage_report_view is not None:
            if hasattr(main_stack_owner, "stacked_widget"):
                main_stack_owner.stacked_widget.removeWidget(
                    self.active_usage_report_view
                )
            self.active_usage_report_view.deleteLater()
            self.active_usage_report_view = None

        # Ensure RackView (self) is the current widget on its parent's stack
        if hasattr(main_stack_owner, "stacked_widget"):
            main_stack_owner.stacked_widget.setCurrentWidget(self)

        # Re-show the Reagent Detail Panel, passing the stored 'came_from_search' context
        if self.rack_viewmodel:
            print(
                f"RackView: Returning to RDP. Passing came_from_search = {self._current_detail_panel_came_from_search}"
            )
            self.rack_viewmodel.show_reagent_details(
                reagent_id, came_from_search=self._current_detail_panel_came_from_search
            )
