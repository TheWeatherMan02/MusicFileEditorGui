"""
This File holds the class for the gui.

Will include build functions and interface event functions

Abbreviations:
    - bn: Button
    - dm: Dropdown Menu
    - lb: Label
    - le: Line Edit
    - cb: Checkbox
"""
import copy

from modules.widgets.button_widget import ButtonWidget
from modules.widgets.line_edit_widget import LineEditWidget
from modules.widgets.dropdown_menu_widget import DropdownMenu
from modules.widgets.checkbox_widget import CheckboxWidget
from modules.widgets.communicator_class import Communicator
import modules.auxiliary_functions.layout_functions as layout
from modules.interface import session_events as se
from modules.dictionaries.dictionaries import Defaults
from modules.dictionaries.file_types import Audio_File_Extensions as extensions

import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox


class EditorGui(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music File Editor")

        # initializing communicator and connecting it to the preform_action method
        self.comm = Communicator()
        self.comm.my_signal.connect(self.preform_action)

        container = QWidget()
        self.layout = QVBoxLayout(container)

        self._initialize_session_handles()
        self._build_all()

        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def _initialize_session_handles(self):
        # initialize directories
        self.image_directory = copy.deepcopy(Defaults['directory_template'])
        self.image_directory['directory_type'] = "image"
        self.song_directory = copy.deepcopy(Defaults['directory_template'])
        self.song_directory['directory_type'] = "song"

        self.song_metadata = copy.deepcopy(Defaults['song_metadata'])

        self.return_value = None  # initializing return variables used during runtime
        self.return_key = None

    def _build_all(self):
        """
        This function sets the layout and builds the gui.

        The gui is divided into a grid layout.
        """
        main_layout = QGridLayout()

        # widgets for select image directory layer
        v_layout_select_directory_image = QVBoxLayout()
        v_layout_select_directory_image.addLayout(self._build_image_directory_select())
        v_layout_select_directory_image.addLayout(self._build_image_select())
        v_layout_select_directory_image.addWidget(self._build_get_current_cover_image())
        main_layout.addLayout(v_layout_select_directory_image, 0, 0)

        # widgets for select song directory layer
        v_layout_select_directory_song = QVBoxLayout()
        v_layout_select_directory_song.addLayout(self._build_song_directory_select())
        v_layout_select_directory_song.addLayout(self._build_song_select())
        v_layout_select_directory_song.addWidget(self._build_save_settings())
        main_layout.addLayout(v_layout_select_directory_song, 0, 1)

        # widgets for cover image layer
        v_layout_cover_image = QVBoxLayout()
        v_layout_cover_image.addWidget(self._build_cover_image())
        main_layout.addLayout(v_layout_cover_image, 1, 0)

        # widgets for metadata layer
        v_layout_metadata_song = QVBoxLayout()
        v_layout_metadata_song.addWidget(self._build_metadata_display())
        v_layout_metadata_song.addWidget(self._build_metadata_edit())
        main_layout.addLayout(v_layout_metadata_song, 1, 1)

        # widgets for exporting file to other file type
        v_layout_export_file = QVBoxLayout()
        v_layout_export_file.addLayout(self._build_export_song())
        main_layout.addLayout(v_layout_export_file, 0, 2)

        # widgets for adding resources to current directories
        v_layout_add_resources = QVBoxLayout()
        v_layout_add_resources.addWidget(self._build_add_image())
        v_layout_add_resources.addWidget(self._build_add_song())
        main_layout.addLayout(v_layout_add_resources, 1, 2)

        # building gui
        self.layout.addLayout(main_layout)

    def _build_image_directory_select(self):
        self.image_direc_lb = QLabel("Image Directory: ")
        bn_select_directory = ButtonWidget(self, "Change Directory", "select_directory", "image")

        v_layout_image_directory = QVBoxLayout()
        v_layout_image_directory.addWidget(self.image_direc_lb)
        v_layout_image_directory.addWidget(bn_select_directory)

        file_name = "episode_1.jpeg"
        file_direc = "/Users/spencer/PycharmProjects/MusicFileEditorGui/modules/test_files"
        self.image_path = os.path.join(file_direc, file_name)

        return v_layout_image_directory

    def _build_get_current_cover_image(self):
        bn_get_current_cover_image = ButtonWidget(self, "get current cover image", "show_cover_image")

        return bn_get_current_cover_image

    def _build_cover_image(self):
        image = QLabel(self)
        pixmap = QPixmap(self.image_path)

        if pixmap.isNull():
            print("!(image error) cover image failed to load")
            print("path to image: {0}".format(self.image_path))
            print("current working directory: {0}".format(os.getcwd()))
            return

        image.setPixmap(pixmap)
        image.resize(pixmap.width(), pixmap.height())

        return image

    def _build_image_select(self):
        label = QLabel("Select image from directory:")
        self.dm_image_select = DropdownMenu([key for key in (self.image_directory['files'].keys())], self)

        h_layout_image_select = layout.horizontal_layout([label, self.dm_image_select])

        return h_layout_image_select

    def _build_add_image(self):
        group_box_add_image_to_directory = QGroupBox("Add image to selected directory")
        v_layout_group_box_add_image_to_directory = QGridLayout()

        bn_add_image_url = ButtonWidget(self, 'Add image from url:', "add_from_url", "image")
        le_add_image_url = LineEditWidget(self)
        v_layout_add_image_url = QVBoxLayout()
        v_layout_add_image_url.addWidget(bn_add_image_url)
        v_layout_add_image_url.addWidget(le_add_image_url)

        bn_add_image_path = ButtonWidget(self, 'Add image from url:', "add_from_path", "image")
        le_add_image_path = LineEditWidget(self)
        v_layout_add_image_path = QVBoxLayout()
        v_layout_add_image_path.addWidget(bn_add_image_path)
        v_layout_add_image_path.addWidget(le_add_image_path)

        v_layout_group_box_add_image_to_directory.addLayout(v_layout_add_image_url, 0, 0)
        v_layout_group_box_add_image_to_directory.addLayout(v_layout_add_image_path, 1, 0)

        group_box_add_image_to_directory.setLayout(v_layout_group_box_add_image_to_directory)

        return group_box_add_image_to_directory

    def _build_song_directory_select(self):
        self.song_direc_lb = QLabel("Song Directory: ")
        bn_select_directory = ButtonWidget(self, "Change Directory", "select_directory", "song")

        v_layout_song_directory = QVBoxLayout()
        v_layout_song_directory.addWidget(self.song_direc_lb)
        v_layout_song_directory.addWidget(bn_select_directory)

        file_name = "system0.m4a"
        file_direc = "/Users/spencer/PycharmProjects/MusicFileEditorGui/modules/test_files"
        self.song_path = os.path.join(file_direc, file_name)

        return v_layout_song_directory

    def _build_song_select(self):
        label = QLabel("Select song from directory:")
        self.dm_song_select = DropdownMenu([key for key in (self.image_directory['files'].keys())], self)

        h_layout_song_select = layout.horizontal_layout([label, self.dm_song_select])

        return h_layout_song_select

    def _build_save_settings(self):
        bn_save_settings = ButtonWidget(self, "save current changes to music file", "save_settings")
        return bn_save_settings

    def _build_metadata_display(self):
        group_box_current_metadata = QGroupBox("Current Metadata")
        v_layout_group_box_current_metadata = QVBoxLayout()

        self.lb_current_title = QLabel("current title: ")
        v_layout_group_box_current_metadata.addWidget(self.lb_current_title)

        self.lb_current_artist = QLabel("current artist: ")
        v_layout_group_box_current_metadata.addWidget(self.lb_current_artist)

        self.lb_current_album = QLabel("current album: ")
        v_layout_group_box_current_metadata.addWidget(self.lb_current_album)

        self.lb_current_genre = QLabel("current genre: ")
        v_layout_group_box_current_metadata.addWidget(self.lb_current_genre)

        self.lb_current_track_num = QLabel("current track number: ")
        v_layout_group_box_current_metadata.addWidget(self.lb_current_track_num)

        self.lb_current_release_date = QLabel("current release date: ")
        v_layout_group_box_current_metadata.addWidget(self.lb_current_release_date)

        group_box_current_metadata.setLayout(v_layout_group_box_current_metadata)

        return group_box_current_metadata

    def _build_metadata_edit(self):
        group_box_edit_metadata = QGroupBox("Edit Metadata")
        h_layout_group_box_edit_metadata = QHBoxLayout()

        # labels
        v_layout_group_box_edit_metadata_lb = QVBoxLayout()
        v_layout_group_box_edit_metadata_lb.addWidget(QLabel("edit title:"))
        v_layout_group_box_edit_metadata_lb.addWidget(QLabel("edit artist:"))
        v_layout_group_box_edit_metadata_lb.addWidget(QLabel("edit album:"))
        v_layout_group_box_edit_metadata_lb.addWidget(QLabel("edit genre:"))
        v_layout_group_box_edit_metadata_lb.addWidget(QLabel("edit track number:"))
        v_layout_group_box_edit_metadata_lb.addWidget(QLabel("edit release date:"))

        # line edits
        v_layout_group_box_edit_metadata_le = QVBoxLayout()
        v_layout_group_box_edit_metadata_le.addWidget(LineEditWidget(self))
        v_layout_group_box_edit_metadata_le.addWidget(LineEditWidget(self))
        v_layout_group_box_edit_metadata_le.addWidget(LineEditWidget(self))
        v_layout_group_box_edit_metadata_le.addWidget(LineEditWidget(self))
        v_layout_group_box_edit_metadata_le.addWidget(LineEditWidget(self))
        v_layout_group_box_edit_metadata_le.addWidget(LineEditWidget(self))

        h_layout_group_box_edit_metadata.addLayout(v_layout_group_box_edit_metadata_lb)
        h_layout_group_box_edit_metadata.addLayout(v_layout_group_box_edit_metadata_le)
        group_box_edit_metadata.setLayout(h_layout_group_box_edit_metadata)

        return group_box_edit_metadata

    def _build_add_song(self):
        group_box_add_song_to_directory = QGroupBox("Add song to selected directory")
        v_layout_group_box_add_song_to_directory = QGridLayout()

        bn_add_song_url = ButtonWidget(self, 'Add song from url:', "add_from_url", "song")
        le_add_song_url = LineEditWidget(self)
        v_layout_add_song_url = QVBoxLayout()
        v_layout_add_song_url.addWidget(bn_add_song_url)
        v_layout_add_song_url.addWidget(le_add_song_url)

        bn_add_song_path = ButtonWidget(self, 'Add song from path:', "add_from_path", "song")
        le_add_song_path = LineEditWidget(self)
        v_layout_add_song_path = QVBoxLayout()
        v_layout_add_song_path.addWidget(bn_add_song_path)
        v_layout_add_song_path.addWidget(le_add_song_path)

        v_layout_group_box_add_song_to_directory.addLayout(v_layout_add_song_url, 0, 0)
        v_layout_group_box_add_song_to_directory.addLayout(v_layout_add_song_path, 1, 0)

        group_box_add_song_to_directory.setLayout(v_layout_group_box_add_song_to_directory)

        return group_box_add_song_to_directory

    def _build_export_song(self):
        self.lb_file_type = QLabel("Current file type: ")
        lb_export_file_to = QLabel("Export to:")
        self.dm_export_file_to = DropdownMenu(extensions, self)  # self.preform_action(action="le_or_dm_change"), self)
        self.cb_export_file = CheckboxWidget("Export song to selected file type", self)

        h_layout_export_file_to = layout.horizontal_layout([lb_export_file_to, self.dm_export_file_to])

        v_layout_export_song = QVBoxLayout()
        v_layout_export_song.addWidget(self.cb_export_file)
        v_layout_export_song.addWidget(self.lb_file_type)
        v_layout_export_song.addLayout(h_layout_export_file_to)

        return v_layout_export_song

    def preform_action(self, data):
        """
        This method gets the name of an action and then runs it.
        The order of the arguments must be past in a specific order

        :return:
        """
        args, kwargs = data
        kwargs_keylist = [key for key in kwargs.keys()]

        self.return_value = args[0] if len(args) > 0 else None
        self.return_key = args[1] if len(args) > 1 else None
        action = kwargs[kwargs_keylist[0]]  # if a signal is emitted, must always pass an action keyword argument as a string
        directory_type = kwargs[kwargs_keylist[1]] if len(kwargs) > 1 else None

        method_name = action + "_action"
        do_action = getattr(self, method_name)

        if directory_type is None:
            do_action()
        else:
            do_action(directory_type)

    def select_directory_action(self, directory_type):
        directory_path, made_selection = se.select_directory()

        if made_selection:
            updated_files = se.get_files_from_directory(directory_type, directory_path)

            # updating directory
            self.update_directory(directory_type, updated_files, directory_path)

            # updating label
            label_name = directory_type + "_direc_lb"
            self.update_label(label_name, directory_path)

            # updating dropdown menu
            dropdown_name = "dm_" + directory_type + "_select"
            self.update_dropdown(dropdown_name, [keys for keys in updated_files.keys()])
            print("directory successfully updated")

        else:
            print("no changes made to song directory")

    def le_or_dm_change_action(self):
        se.le_or_dm_change(self)

    def cb_change_action(self):
        self.ext_event()

    def save_settings_action(self):
        self.ext_event()

    def show_cover_image_action(self):
        self.ext_event()

    def add_from_url_action(self, directory_type):
        self.ext_event()

    def add_from_path_action(self, directory_type):
        self.ext_event()

    def update_label(self, label_name, updated_text):
        label = getattr(self, label_name)
        # only grabs the "<label header>:" text and not the other text
        label_header = label.text().split(":")[0] + ": "
        label.setText(label_header + str(updated_text))

    def update_dropdown(self, dropdown_name, updated_items):
        dropdown = getattr(self, dropdown_name)
        dropdown.clear()
        dropdown.addItems(updated_items)

    def update_directory(self, directory_type, files, path):
        directory = getattr(self, directory_type + "_directory")
        directory['directory_name'] = path
        directory['files'] = files

    def ext_event(self):
        print("you made an event!")
