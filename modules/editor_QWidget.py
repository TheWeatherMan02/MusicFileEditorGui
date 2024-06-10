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
from modules.widgets.image_widget import ImageWidget
from modules.widgets.checkbox_widget import CheckboxWidget
from modules.widgets.communicator_class import Communicator
import modules.auxiliary_functions.layout_functions as layout
from modules.interface import session_events as se
from modules.dictionaries.dictionaries import Defaults
from modules.dictionaries.file_types import Audio_File_Extensions as extensions

import os
from PyQt6.QtCore import Qt
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

        print(f"image directory current file: {self.image_directory_dictionary['current_file']}")

    def _initialize_session_handles(self):
        # initialize directories
        self.image_directory_dictionary = copy.deepcopy(Defaults['directory_template'])
        self.image_directory_dictionary['directory_type'] = "image"
        self.song_directory_dictionary = copy.deepcopy(Defaults['directory_template'])
        self.song_directory_dictionary['directory_type'] = "song"

        self.song_metadata_dictionary = copy.deepcopy(Defaults['song_metadata'])

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
        # v_layout_select_directory_image.addWidget(self._build_get_current_cover_image())
        v_layout_select_directory_image.addWidget(self._build_add_image())
        main_layout.addLayout(v_layout_select_directory_image, 0, 0)

        # widgets for select song directory layer
        v_layout_select_directory_song = QVBoxLayout()
        v_layout_select_directory_song.addLayout(self._build_song_directory_select())
        v_layout_select_directory_song.addLayout(self._build_song_select())
        v_layout_select_directory_song.addWidget(self._build_add_song())
        main_layout.addLayout(v_layout_select_directory_song, 0, 1)

        # widgets for directory image layer
        v_layout_directory_image = QVBoxLayout()
        v_layout_directory_image.addWidget(self._build_directory_image())
        main_layout.addLayout(v_layout_directory_image, 1, 0)

        # widgets for current image layer
        v_layout_current_image = QVBoxLayout()
        v_layout_current_image.addWidget(self._build_current_image())
        main_layout.addLayout(v_layout_current_image, 1, 1)

        # widgets for save and exporting file to other file type
        v_layout_export_file = QVBoxLayout()
        v_layout_export_file.addLayout(self._build_export_song())
        v_layout_export_file.addWidget(self._build_save_settings())
        main_layout.addLayout(v_layout_export_file, 0, 2)

        # widgets for metadata layer
        v_layout_metadata_song = QVBoxLayout()
        v_layout_metadata_song.addWidget(self._build_metadata_checkbox())
        v_layout_metadata_song.addWidget(self._build_metadata_display())
        v_layout_metadata_song.addWidget(self._build_metadata_edit())
        main_layout.addLayout(v_layout_metadata_song, 1, 2)

        # building gui
        self.layout.addLayout(main_layout)

    def _build_image_directory_select(self):
        self.image_directory_lb = QLabel("Image Directory: ")
        bn_select_directory = ButtonWidget(self, "Change Directory", "select_directory", "image_directory")

        v_layout_image_directory = QVBoxLayout()
        v_layout_image_directory.addWidget(self.image_directory_lb)
        v_layout_image_directory.addWidget(bn_select_directory)

        file_name = "episode_1.jpeg"
        file_direc = "/Users/spencer/PycharmProjects/MusicFileEditorGui/modules/test_files"
        self.image_path = os.path.join(file_direc, file_name)

        return v_layout_image_directory

    def _build_directory_image(self):
        self.directory_image = ImageWidget(Defaults['default_image'], "Selected image")

        return self.directory_image

    def _build_current_image(self):
        self.current_image = ImageWidget(Defaults['default_image'], "Current song cover")

        return self.current_image

    def _build_image_select(self):
        label = QLabel("Select image from directory:")
        self.dm_image_directory_select = DropdownMenu(self,
                                                      [key for key in (self.image_directory_dictionary['files'].keys())],
                                                      "image_directory", "current_file", default_image=True)

        h_layout_image_select = layout.horizontal_layout([label, self.dm_image_directory_select])

        return h_layout_image_select

    def _build_add_image(self):
        group_box_add_image_to_directory = QGroupBox("Add image to selected directory")
        v_layout_group_box_add_image_to_directory = QGridLayout()

        bn_add_image_url = ButtonWidget(self, 'Add image from url:', "add_from_url", "image_directory")
        le_add_image_url = LineEditWidget(self, "image_directory", "add_url")
        v_layout_add_image_url = QVBoxLayout()
        v_layout_add_image_url.addWidget(bn_add_image_url)
        v_layout_add_image_url.addWidget(le_add_image_url)

        bn_add_image_path = ButtonWidget(self, 'Add image from path:', "add_from_path", "image_directory")
        le_add_image_path = LineEditWidget(self, "image_directory", "add_path")
        v_layout_add_image_path = QVBoxLayout()
        v_layout_add_image_path.addWidget(bn_add_image_path)
        v_layout_add_image_path.addWidget(le_add_image_path)

        v_layout_group_box_add_image_to_directory.addLayout(v_layout_add_image_url, 0, 0)
        v_layout_group_box_add_image_to_directory.addLayout(v_layout_add_image_path, 1, 0)

        group_box_add_image_to_directory.setLayout(v_layout_group_box_add_image_to_directory)

        return group_box_add_image_to_directory

    def _build_song_directory_select(self):
        self.song_directory_lb = QLabel("Song Directory: ")
        bn_select_directory = ButtonWidget(self, "Change Directory", "select_directory", "song_directory")

        v_layout_song_directory = QVBoxLayout()
        v_layout_song_directory.addWidget(self.song_directory_lb)
        v_layout_song_directory.addWidget(bn_select_directory)

        file_name = "system0.m4a"
        file_direc = "/Users/spencer/PycharmProjects/MusicFileEditorGui/modules/test_files"
        self.song_path = os.path.join(file_direc, file_name)

        return v_layout_song_directory

    def _build_song_select(self):
        label = QLabel("Select song from directory:")
        self.dm_song_directory_select = DropdownMenu(self,
                                                     [key for key in (self.song_directory_dictionary['files'].keys())],
                                                     "song_directory", "current_file")

        h_layout_song_select = layout.horizontal_layout([label, self.dm_song_directory_select])

        return h_layout_song_select

    def _build_save_settings(self):
        bn_save_settings = ButtonWidget(self, "save current changes to music file", "save_settings")
        return bn_save_settings

    def _build_metadata_checkbox(self):
        """
        This checkbox toggles filling line edits with current metadata
        """
        self.cb_edit_metadata_fill_le = CheckboxWidget("Fill edit lines with current metadata when selecting file",
                                                       self)
        return self.cb_edit_metadata_fill_le

    def _build_metadata_display(self):
        group_box_current_metadata = QGroupBox("Current Metadata")

        # header labels (these don't change)
        v_layout_group_box_current_metadata_headers = QVBoxLayout()
        lb_header_title = QLabel("Current title: ")
        lb_header_title.setAlignment(Qt.AlignmentFlag.AlignRight)
        v_layout_group_box_current_metadata_headers.addWidget(lb_header_title)

        lb_header_artist = QLabel("Current artist: ")
        lb_header_artist.setAlignment(Qt.AlignmentFlag.AlignRight)
        v_layout_group_box_current_metadata_headers.addWidget(lb_header_artist)

        lb_header_album = QLabel("Current album: ")
        lb_header_album.setAlignment(Qt.AlignmentFlag.AlignRight)
        v_layout_group_box_current_metadata_headers.addWidget(lb_header_album)

        lb_header_genre = QLabel("Current genre: ")
        lb_header_genre.setAlignment(Qt.AlignmentFlag.AlignRight)
        v_layout_group_box_current_metadata_headers.addWidget(lb_header_genre)

        lb_header_track_number = QLabel("Current track number: ")
        lb_header_track_number.setAlignment(Qt.AlignmentFlag.AlignRight)
        v_layout_group_box_current_metadata_headers.addWidget(lb_header_track_number)

        lb_header_year = QLabel("Current year: ")
        lb_header_year.setAlignment(Qt.AlignmentFlag.AlignRight)
        v_layout_group_box_current_metadata_headers.addWidget(lb_header_year)

        # content labels (will be updated during runtime)
        v_layout_group_box_current_metadata_content = QVBoxLayout()
        self.lb_current_title = QLabel(None)
        v_layout_group_box_current_metadata_content.addWidget(self.lb_current_title)

        self.lb_current_artist = QLabel(None)
        v_layout_group_box_current_metadata_content.addWidget(self.lb_current_artist)

        self.lb_current_album = QLabel(None)
        v_layout_group_box_current_metadata_content.addWidget(self.lb_current_album)

        self.lb_current_genre = QLabel(None)
        v_layout_group_box_current_metadata_content.addWidget(self.lb_current_genre)

        self.lb_current_track_number = QLabel(None)
        v_layout_group_box_current_metadata_content.addWidget(self.lb_current_track_number)

        self.lb_current_year = QLabel(None)
        v_layout_group_box_current_metadata_content.addWidget(self.lb_current_year)

        # add labels to group box
        v_layout_group_box_current_metadata = layout.horizontal_layout([v_layout_group_box_current_metadata_headers,
                                                                        v_layout_group_box_current_metadata_content])
        group_box_current_metadata.setLayout(v_layout_group_box_current_metadata)

        return group_box_current_metadata

    def _build_metadata_edit(self):
        group_box_edit_metadata = QGroupBox("Edit Metadata")
        h_layout_group_box_edit_metadata = QHBoxLayout()

        # labels
        v_layout_group_box_edit_metadata_lb = QVBoxLayout()

        lb_edit_title = QLabel("Edit title:")
        lb_edit_title.setAlignment(Qt.AlignmentFlag.AlignRight)
        v_layout_group_box_edit_metadata_lb.addWidget(lb_edit_title)

        lb_edit_artist = QLabel("Edit artist:")
        lb_edit_artist.setAlignment(Qt.AlignmentFlag.AlignRight)
        v_layout_group_box_edit_metadata_lb.addWidget(lb_edit_artist)

        lb_edit_album = QLabel("Edit album:")
        lb_edit_album.setAlignment(Qt.AlignmentFlag.AlignRight)
        v_layout_group_box_edit_metadata_lb.addWidget(lb_edit_album)

        lb_edit_genre = QLabel("Edit genre:")
        lb_edit_genre.setAlignment(Qt.AlignmentFlag.AlignRight)
        v_layout_group_box_edit_metadata_lb.addWidget(lb_edit_genre)

        lb_edit_track_number = QLabel("Edit track number:")
        lb_edit_track_number.setAlignment(Qt.AlignmentFlag.AlignRight)
        v_layout_group_box_edit_metadata_lb.addWidget(lb_edit_track_number)

        lb_edit_year = QLabel("Edit year:")
        lb_edit_year.setAlignment(Qt.AlignmentFlag.AlignRight)
        v_layout_group_box_edit_metadata_lb.addWidget(lb_edit_year)

        # line edits
        v_layout_group_box_edit_metadata_le = QVBoxLayout()

        self.le_metadata_title = LineEditWidget(self, 'song_metadata', 'title')
        v_layout_group_box_edit_metadata_le.addWidget(self.le_metadata_title)

        self.le_metadata_artist = LineEditWidget(self, 'song_metadata', 'artist')
        v_layout_group_box_edit_metadata_le.addWidget(self.le_metadata_artist)

        self.le_metadata_album = LineEditWidget(self, 'song_metadata', 'album')
        v_layout_group_box_edit_metadata_le.addWidget(self.le_metadata_album)

        self.le_metadata_genre = LineEditWidget(self, 'song_metadata', 'genre')
        v_layout_group_box_edit_metadata_le.addWidget(self.le_metadata_genre)

        self.le_metadata_track_number = LineEditWidget(self, 'song_metadata', 'track_number')
        v_layout_group_box_edit_metadata_le.addWidget(self.le_metadata_track_number)

        self.le_metadata_year = LineEditWidget(self, 'song_metadata', 'year')
        v_layout_group_box_edit_metadata_le.addWidget(self.le_metadata_year)

        h_layout_group_box_edit_metadata.addLayout(v_layout_group_box_edit_metadata_lb)
        h_layout_group_box_edit_metadata.addLayout(v_layout_group_box_edit_metadata_le)
        group_box_edit_metadata.setLayout(h_layout_group_box_edit_metadata)

        return group_box_edit_metadata

    def _build_add_song(self):
        group_box_add_song_to_directory = QGroupBox("Add song to selected directory")
        v_layout_group_box_add_song_to_directory = QGridLayout()

        bn_add_song_url = ButtonWidget(self, 'Add song from url:', "add_from_url", "song_directory")
        le_add_song_url = LineEditWidget(self, 'song_directory', 'add_url')
        v_layout_add_song_url = QVBoxLayout()
        v_layout_add_song_url.addWidget(bn_add_song_url)
        v_layout_add_song_url.addWidget(le_add_song_url)

        bn_add_song_path = ButtonWidget(self, 'Add song from path:', "add_from_path", "song_directory")
        le_add_song_path = LineEditWidget(self, 'song_directory', 'add_path')
        v_layout_add_song_path = QVBoxLayout()
        v_layout_add_song_path.addWidget(bn_add_song_path)
        v_layout_add_song_path.addWidget(le_add_song_path)

        v_layout_group_box_add_song_to_directory.addLayout(v_layout_add_song_url, 0, 0)
        v_layout_group_box_add_song_to_directory.addLayout(v_layout_add_song_path, 1, 0)

        group_box_add_song_to_directory.setLayout(v_layout_group_box_add_song_to_directory)

        return group_box_add_song_to_directory

    def _build_export_song(self):
        self.cb_copy_file_to_directory = CheckboxWidget("Save changes to a copy of the song", self)
        self.cb_move_to_directory = CheckboxWidget("Export song to different directory\n"
                                                   "(will be asked to choose when saving file)", self)

        self.lb_file_type = QLabel("Current file type: ")
        lb_export_file_type = QLabel("Export type:")
        self.dm_export_file_type = DropdownMenu(self, extensions, 'song_directory', 'export_type')
        self.cb_export_file = CheckboxWidget("Export song to selected file type", self)

        h_layout_export_file_to = layout.horizontal_layout([lb_export_file_type, self.dm_export_file_type])

        v_layout_export_song = QVBoxLayout()
        v_layout_export_song.addWidget(self.cb_export_file)
        v_layout_export_song.addWidget(self.cb_copy_file_to_directory)
        v_layout_export_song.addWidget(self.cb_move_to_directory)
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

        action = kwargs[kwargs_keylist[0]]  # if a signal is emitted, must always pass an action keyword argument as a string
        self.dictionary_arg = kwargs[kwargs_keylist[1]] if len(kwargs) > 1 else None
        self.return_value = args[0] if len(args) > 0 else None
        self.return_key = args[1] if len(args) > 1 else None

        method_name = action + "_action"
        do_action = getattr(self, method_name)
        do_action()

    def select_directory_action(self):
        directory_path, made_selection = se.select_directory()

        if made_selection:
            updated_files = se.get_files_from_directory(self.dictionary_arg, directory_path)

            # updating directories
            se.update_dictionary(self, 'directory_name', directory_path)
            se.update_dictionary(self, 'files', updated_files)

            # updating label
            label_name = self.dictionary_arg + "_lb"
            se.update_label(self, label_name, directory_path)

            # updating dropdown menu
            dropdown_name = "dm_" + self.dictionary_arg + "_select"
            se.update_dropdown(self, dropdown_name, [keys for keys in updated_files.keys()])
            print("Dropdown successfully updated")

        else:
            print("no changes made to song directory")

    def le_or_dm_change_action(self):
        print("Changing dictionary value:")
        print(f"\t{self.dictionary_arg}_dictionary[{self.return_key}] = {self.return_value}")
        print(f"New value type: {type(self.return_value)}\n")
        se.update_dictionary(self, self.return_key, self.return_value)

        # if song is being selected, call to update metadata tags
        if self.return_key == "current_file" and self.dictionary_arg == "song_directory":
            se.update_song_metadata(self)

            # update file type label in export section
            update_label = "lb_file_type"
            file_type = self.song_directory_dictionary[self.return_key].split(".")[-1]
            se.update_label(self, update_label, file_type)

            # update associated labels in the gui
            for key in self.song_metadata_dictionary:
                if key == 'cover_art':
                    metadata_image = self.song_metadata_dictionary[key]
                    # update song cover image
                    se.update_image(self, "current_image", metadata_image)

                else:
                    label_name = "lb_current_" + key
                    updated_text = self.song_metadata_dictionary[key]
                    se.update_label(self, label_name, updated_text)

                    # update line edit metadata with current metadata if metadata checkbox is checked
                    if self.cb_edit_metadata_fill_le.checkState() is Qt.CheckState.Checked:
                        line_edit_name = "le_metadata_" + key
                        updated_text = self.song_metadata_dictionary[key]
                        se.update_line_edit_text(self, line_edit_name, updated_text)

        # update image currently selected from image directory
        elif self.return_key == "current_file" and self.dictionary_arg == "image_directory":
            # check if image directory has default currently selected
            if self.return_value == "-- Default --":
                image_path = Defaults['default_image']
            else:
                image_path = os.path.join(self.image_directory_dictionary['directory_name'],
                                          self.image_directory_dictionary[self.return_key])
            # update selected image
            se.update_image(self, "directory_image", image_path)

    def save_settings_action(self):
        se.save_settings(self)
        # update metadata tags to reflect saved settings
        # update associated labels in the gui (make sure things updated
        for key in self.song_metadata_dictionary:
            if key == 'cover_art':
                metadata_image = self.song_metadata_dictionary[key]
                se.update_image(self, "current_image", metadata_image)  # update song cover image

            else:
                label_name = "lb_current_" + key
                updated_text = self.song_metadata_dictionary[key]
                se.update_label(self, label_name, updated_text)

    def add_from_url_action(self):
        self.ext_event()

    def add_from_path_action(self):
        self.ext_event()

    def ext_event(self):
        print("you made an event!")
