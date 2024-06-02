"""
This is the main file that will run the music editor gui
"""

from modules.editor_QWidget import EditorGui

import sys
from PyQt6.QtWidgets import QApplication


def main():
    # probably not going to be controlling this
    # using command line arguments
    app = QApplication(sys.argv)

    window = EditorGui()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
