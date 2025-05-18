# app_context.py
from PyQt6.QtCore import QSize

class AppContext:
    screen_resolution: QSize = QSize(1280, 720)  # default

    @classmethod
    def set_screen_resolution(cls, size: QSize):
        cls.screen_resolution = size

    @classmethod
    def get_screen_resolution(cls) -> QSize:
        return cls.screen_resolution