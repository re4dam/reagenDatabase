import os
from PyQt6.QtGui import QFontDatabase, QFont

class FontManager:
    loaded_fonts = {}

    @staticmethod
    def load_fonts(folder):
        for font_file in os.listdir(folder):
            if font_file.endswith((".ttf", ".otf")):
                font_path = os.path.join(folder, font_file)
                font_id = QFontDatabase.addApplicationFont(font_path)

                if font_id == -1:
                    print(f"❌ Gagal memuat font: {font_file}")
                    continue

                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    alias = os.path.splitext(font_file)[0]  # tanpa ekstensi
                    FontManager.loaded_fonts[alias] = families[0]
                    print(f"✓ {alias} → {families[0]}")
                else:
                    print(f"⚠️ Tidak ditemukan family untuk font: {font_file}")

    @staticmethod
    def get_font(alias: str, size: int) -> QFont:
        family = FontManager.loaded_fonts.get(alias)
        if family:
            return QFont(family, size)
        else:
            print(f"⚠️ Font alias '{alias}' belum dimuat.")
            return QFont()  # fallback