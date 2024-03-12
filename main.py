import qdarktheme
import sys
from PyQt6.QtWidgets import QApplication
from MainWindow import MainWindow
# icons loading
import resource_rc

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # loads style file
    with open("style.qss", "r") as style_file:
        style_str = style_file.read()

    # sets style theme
    qdarktheme.setup_theme("light", custom_colors={'primary': '0061a4'}, additional_qss=style_str)

    # loads Main Window
    window = MainWindow()
    window.show()
    sys.exit(app.exec())