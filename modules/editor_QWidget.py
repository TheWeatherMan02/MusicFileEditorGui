"""
This File holds the class for the gui.

Will include build functions and interface event functions

Abbreviations:
    - bn: Button
    - dm: Dropdown Menu
    - lb: Label
    - le: Line Edit
"""

from modules.widgets.button_widget import ButtonWidget
from modules.widgets.line_edit_widget import LineEditWidget
from modules.widgets.dropdown_menu_widget import DropdownMenu

# from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel


class EditorGui(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music File Editor")
        # self.setGeometry(100, 100, 300, 200)

        container = QWidget()
        self.layout = QVBoxLayout(container)

        self._build_add_image_url()
        self._build_image_select()

        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def _build_cover_image(self):
        pass

    def _build_image_select(self):
        dm_image_select = DropdownMenu(["1", "2", "3"], self.ext_event)
        self.layout.addWidget((dm_image_select))

    def _build_add_image_url(self):
        bn_add_image = ButtonWidget('add img. from url', self.ext_event, self)
        self.layout.addWidget(bn_add_image)

        le_image_url = LineEditWidget(self.ext_event)
        self.layout.addWidget(le_image_url)

    def _build_song_select(self):
        pass

    def _build_metadata_display(self):
        pass

    def _build_metadata_edit(self):
        pass

    def _build_metadata_defaults(self):
        pass

    def ext_event(self):
        print("you made an event!")
