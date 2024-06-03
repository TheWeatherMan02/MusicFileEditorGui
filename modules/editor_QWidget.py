"""
This File holds the class for the gui.

Will include build functions and interface event functions

Abbreviations:
    - bn: Button
    - dm: Dropdown Menu
    - lb: Label
    - le: Line Edit
"""
import copy

from modules.widgets.button_widget import ButtonWidget
from modules.widgets.line_edit_widget import LineEditWidget
from modules.widgets.dropdown_menu_widget import DropdownMenu
import modules.auxiliary_functions.layout_functions as layout
from modules.interface import session_events as se
from modules.dictionaries.dictionaries import Directory_Template

import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QVBoxLayout, QLabel, QGroupBox


class EditorGui(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music File Editor")

        container = QWidget()
        self.layout = QVBoxLayout(container)

        self._initialize_session_handles()
        self._build_all()

        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def _initialize_session_handles(self):
        # initialize directories
        image_directory = Directory_Template
        image_directory['directory_type'] = "image"
        self.image_directory = copy.deepcopy(image_directory)
        # self.image_directory = copy.deepcopy(Directory_Template)
        # self.image_directory['directory_type'] = "image"
        self.song_directory = copy.deepcopy(Directory_Template)
        self.song_directory['directory_type'] = "song"

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

        # widgets for adding resources to current image directory
        v_layout_add_resources_image = QVBoxLayout()
        v_layout_add_resources_image.addWidget(self._build_add_image())
        main_layout.addLayout(v_layout_add_resources_image, 2, 0)

        # widgets for adding resources to current song directory
        v_layout_add_resources_song = QVBoxLayout()
        v_layout_add_resources_song.addWidget(self._build_add_song())
        main_layout.addLayout(v_layout_add_resources_song, 2, 1)

        # building gui
        self.layout.addLayout(main_layout)

    def _build_image_directory_select(self):
        label = QLabel("select path to image directory:")
        bn_select_directory = ButtonWidget("Directory: {0}".format(self.image_directory['directory_name']),
                                           lambda: self.preform_action("select_image_directory"), self)

        h_layout_image_directory = layout.horizontal_layout([label, bn_select_directory])

        file_name = "episode_1.jpeg"
        file_direc = "/Users/spencer/PycharmProjects/MusicFileEditorGui/modules/test_files"
        self.image_path = os.path.join(file_direc, file_name)

        return h_layout_image_directory

    def _build_get_current_cover_image(self):
        bn_get_current_cover_image = ButtonWidget("get current cover image",
                                                  self.ext_event, self)

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
        label = QLabel("select image from directory:")
        dm_image_select = DropdownMenu(["1", "2", "3"], self.ext_event)

        h_layout_image_select = layout.horizontal_layout([label, dm_image_select])

        return h_layout_image_select

    def _build_add_image(self):
        group_box_add_image_to_directory = QGroupBox("Add image to selected directory")
        v_layout_group_box_add_image_to_directory = QVBoxLayout()

        bn_add_image_url = ButtonWidget('add image from url:', self.ext_event, self)
        le_add_image_url = LineEditWidget(self.ext_event)
        h_layout_add_image_url = layout.horizontal_layout([bn_add_image_url,
                                                           le_add_image_url])
        v_layout_group_box_add_image_to_directory.addLayout(h_layout_add_image_url)

        bn_add_image_path = ButtonWidget('add image from path:', self.ext_event, self)
        le_add_image_path = LineEditWidget(self.ext_event)
        h_layout_add_image_path = layout.horizontal_layout([bn_add_image_path,
                                                            le_add_image_path])
        v_layout_group_box_add_image_to_directory.addLayout(h_layout_add_image_path)

        group_box_add_image_to_directory.setLayout(v_layout_group_box_add_image_to_directory)

        return group_box_add_image_to_directory

    def _build_song_directory_select(self):
        label = QLabel("select path to song directory:")
        bn_select_directory = ButtonWidget("Directory: {0}".format(self.song_directory['directory_name']),
                                           lambda: self.preform_action("select_song_directory"), self)

        h_layout_song_directory = layout.horizontal_layout([label, bn_select_directory])

        file_name = "system0.m4a"
        file_direc = "/Users/spencer/PycharmProjects/MusicFileEditorGui/modules/test_files"
        self.song_path = os.path.join(file_direc, file_name)

        return h_layout_song_directory

    def _build_song_select(self):
        label = QLabel("select song from directory:")
        dm_song_select = DropdownMenu(["1", "2", "3"], self.ext_event)

        h_layout_song_select = layout.horizontal_layout([label, dm_song_select])

        return h_layout_song_select

    def _build_save_settings(self):
        bn_save_settings = ButtonWidget("save current changes to music file", self.ext_event, self)

        return bn_save_settings

    def _build_metadata_display(self):
        group_box_current_metadata = QGroupBox("Current Metadata")
        v_layout_group_box_current_metadata = QVBoxLayout()

        lb_current_title = QLabel("current title: ")
        v_layout_group_box_current_metadata.addWidget(lb_current_title)

        lb_current_artist = QLabel("current artist: ")
        v_layout_group_box_current_metadata.addWidget(lb_current_artist)

        lb_current_album = QLabel("current album: ")
        v_layout_group_box_current_metadata.addWidget(lb_current_album)

        lb_current_genre = QLabel("current genre: ")
        v_layout_group_box_current_metadata.addWidget(lb_current_genre)

        lb_current_track_num = QLabel("current track number: ")
        v_layout_group_box_current_metadata.addWidget(lb_current_track_num)

        lb_current_release_date = QLabel("current release date: ")
        v_layout_group_box_current_metadata.addWidget(lb_current_release_date)

        group_box_current_metadata.setLayout(v_layout_group_box_current_metadata)

        return group_box_current_metadata

    def _build_metadata_edit(self):
        group_box_edit_metadata = QGroupBox("Edit Metadata")
        v_layout_group_box_edit_metadata = QVBoxLayout()

        lb_edit_title = QLabel("edit title:")
        le_edit_title = LineEditWidget(self.ext_event)
        h_layout_edit_title = layout.horizontal_layout([lb_edit_title, le_edit_title])
        v_layout_group_box_edit_metadata.addLayout(h_layout_edit_title)

        lb_edit_artist = QLabel("edit artist:")
        le_edit_artist = LineEditWidget(self.ext_event)
        h_layout_edit_artist = layout.horizontal_layout([lb_edit_artist, le_edit_artist])
        v_layout_group_box_edit_metadata.addLayout(h_layout_edit_artist)

        lb_edit_album = QLabel("edit album:")
        le_edit_album = LineEditWidget(self.ext_event)
        h_layout_edit_album = layout.horizontal_layout([lb_edit_album, le_edit_album])
        v_layout_group_box_edit_metadata.addLayout(h_layout_edit_album)

        lb_edit_genre = QLabel("edit genre:")
        le_edit_genre = LineEditWidget(self.ext_event)
        h_layout_edit_genre = layout.horizontal_layout([lb_edit_genre, le_edit_genre])
        v_layout_group_box_edit_metadata.addLayout(h_layout_edit_genre)

        lb_edit_track_num = QLabel("edit track number:")
        le_edit_track_num = LineEditWidget(self.ext_event)
        h_layout_edit_track_num = layout.horizontal_layout([lb_edit_track_num, le_edit_track_num])
        v_layout_group_box_edit_metadata.addLayout(h_layout_edit_track_num)

        lb_edit_release_date = QLabel("edit release date:")
        le_edit_release_date = LineEditWidget(self.ext_event)
        h_layout_edit_release_date = layout.horizontal_layout([lb_edit_release_date, le_edit_release_date])
        v_layout_group_box_edit_metadata.addLayout(h_layout_edit_release_date)

        group_box_edit_metadata.setLayout(v_layout_group_box_edit_metadata)

        return group_box_edit_metadata

    def _build_add_song(self):
        group_box_add_song_to_directory = QGroupBox("Add song to selected directory")
        v_layout_group_box_add_song_to_directory = QVBoxLayout()

        bn_add_song_url = ButtonWidget('add song from url:', self.ext_event, self)
        le_add_song_url = LineEditWidget(self.ext_event)
        h_layout_add_song_url = layout.horizontal_layout([bn_add_song_url,
                                                          le_add_song_url])
        v_layout_group_box_add_song_to_directory.addLayout(h_layout_add_song_url)

        bn_add_song_path = ButtonWidget('add song from path:', self.ext_event, self)
        le_add_song_path = LineEditWidget(self.ext_event)
        h_layout_add_song_path = layout.horizontal_layout([bn_add_song_path,
                                                           le_add_song_path])
        v_layout_group_box_add_song_to_directory.addLayout(h_layout_add_song_path)

        group_box_add_song_to_directory.setLayout(v_layout_group_box_add_song_to_directory)

        return group_box_add_song_to_directory

    def preform_action(self, action):
        """
        This method gets the name of an action and then runs it.

        :return:
        """
        method_name = action + "_action"
        do_action = getattr(self, method_name)
        do_action()

    def select_song_directory_action(self):
        song_directory_path, made_selection = se.select_directory()

        if made_selection:
            updated_files = se.get_files_from_directory(self.image_directory['directory_type'], song_directory_path)

            # updating directory
            self.image_directory['directory_name'] = song_directory_path
            self.image_directory['files'] = updated_files
            print("directory successfully updated")

        else:
            print("no changes made to song directory")

    def select_image_directory_action(self):
        image_directory_path, made_selection = se.select_directory()

        if made_selection:
            updated_files = se.get_files_from_directory(self.image_directory['directory_type'], image_directory_path)

            # updating directory
            self.image_directory['directory_name'] = image_directory_path
            self.image_directory['files'] = updated_files
            print("directory successfully updated")

        else:
            print("no changes made to image directory")

    def ext_event(self):
        print("you made an event!")
