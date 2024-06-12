from modules.auxiliary_functions import audio_functions as audio

import os
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import Qt, QByteArray
from PyQt6.QtGui import QPixmap


def select_directory():
    # flag for successful selection
    made_selection = False

    # initializing directory path
    directory_path = ""

    # create and open directory selection dialog
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.FileMode.Directory)
    dialog.setOption(QFileDialog.Option.ShowDirsOnly, on=True)

    if dialog.exec():
        try:
            # get the selected directory path
            directory_path = dialog.selectedFiles()[0]
            print("Selected directory:", directory_path)
            made_selection = True
        except Exception as e:
            print("!!! (error) Failure during selection process")
            print(f"Error type: {e}")
            made_selection = False

    if not made_selection:
        print("Exited without selecting a folder")
        directory_path = ""

    return directory_path, made_selection


def get_files_from_directory(directory_type, new_info_path):
    # initializing variables for name and files
    updated_files = {}

    # choosing file types to add
    if directory_type == "image_directory":
        from modules.dictionaries.file_types import Image_File_Extension
        file_extension_list = Image_File_Extension
    elif directory_type == "song_directory":
        from modules.dictionaries.file_types import Audio_File_Extensions
        file_extension_list = Audio_File_Extensions
    else:
        print("!!! (error) unknown file type: {0}".format(directory_type))
        file_extension_list = []

    # change path to new directory
    os.chdir(new_info_path)
    for root, dirs, files in os.walk("."):
        for filename in files:
            file_extension = os.path.splitext(filename)[1]
            if file_extension in file_extension_list:
                file_path = os.path.join(os.getcwd(), filename)
                updated_files.update({filename: file_path})

    return updated_files


def update_song_metadata(editor):
    file_directory = editor.song_directory_dictionary['directory_name']
    file_name = editor.song_directory_dictionary['current_file']
    file_path = os.path.join(file_directory, file_name)

    new_image = False

    if os.path.exists(file_path):
        try:
            print(file_path)
            # get the file type and metadata
            metadata, new_image = audio.get_file_metadata(file_path)

            # update metadata dictionary
            editor.song_metadata_dictionary.update(metadata)

        except TypeError as e:
            print("!!! (update_song_metadata) TypeError occurred while updating song metadata")
            print(f"Error message: \"{e}\"")

        except Exception as e:
            print("!!! (update_song_metadata) Error occurred while updating song metadata")
            print(f"Exception type: {e}")
    else:
        print("!!! (update_song_metadata) File path does not exist, no changes to metadata made")
        print(f"File path: {file_path}")

    return new_image


def update_song_metadata_labels(editor, new_image=False):
    for key in editor.song_metadata_dictionary:
        if key == 'cover_art':
            metadata_image = editor.song_metadata_dictionary[key]
            if new_image is True:
                # update song cover image
                update_image(editor, "current_image", metadata_image)
            elif new_image is False:
                # set image to default
                update_image(editor, "current_image", editor.default_image['image_path'])

        else:
            label_name = "lb_current_" + key
            updated_text = editor.song_metadata_dictionary[key]
            update_label(editor, label_name, updated_text)

            # update line edit metadata with current metadata if metadata checkbox is checked
            if editor.cb_edit_metadata_fill_le.checkState() is Qt.CheckState.Checked:
                line_edit_name = "le_metadata_" + key
                updated_text = editor.song_metadata_dictionary[key]
                update_line_edit_text(editor, line_edit_name, updated_text)


def update_label(editor, label_name, updated_text):
    label = getattr(editor, label_name)
    if "lb_current_" not in label_name:
        # only grabs the "<label header>:" text and not the other text
        label_header = label.text().split(":")[0] + ": "
        label.setText(label_header + str(updated_text))
    else:
        # labels for metadata have different format to accommodate right justification
        label.setText(updated_text)


def update_line_edit_text(editor, line_edit_name, updated_text):
    line_edit = getattr(editor, line_edit_name)
    line_edit.setText(updated_text)


def update_dropdown(editor, dropdown_name, updated_items):
    dropdown = getattr(editor, dropdown_name)
    dropdown.clear()
    if hasattr(dropdown, "default"):
        updated_items = dropdown.default + updated_items
    dropdown.addItems(updated_items)


def update_dictionary(editor, key, value):
    dictionary = getattr(editor, editor.dictionary_arg + "_dictionary")
    dictionary[key] = value


def update_image(editor, widget_name, new_image):
    image_widget = getattr(editor, widget_name)
    try:
        # checking if image is stored in bytes
        if isinstance(new_image, bytes):
            print("!!! (update image) new image is stored in byte format, converting to usable format")
            qbyte_array = QByteArray(new_image)
            new_pixmap = QPixmap()
            new_pixmap.loadFromData(qbyte_array)

        else:
            new_pixmap = QPixmap(new_image)

        # if pixmap is null, then update image will be cancelled
        if new_pixmap.isNull():
            print("!!! (update_image) New pixmap used to update image is null")
            print("\tCurrent song likely does not have contain a cover image")
            print("\tSetting current song cover to default image")

            new_pixmap = QPixmap(editor.default_image['image_path'])

        scaled_new_pixmap = new_pixmap.scaled(image_widget.image_label.size(),
                                              Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)

        image_widget.image_label.setPixmap(scaled_new_pixmap)
        # image_widget.image_label.resize(image_widget.size())  # this kinda messes up the size of the image

    except Exception as e:
        print("!!! (update image) Could not update image")
        print(f"Error type: {e}")


def save_settings(editor):
    file_directory = editor.song_directory_dictionary['directory_name']
    file_name = editor.song_directory_dictionary['current_file']
    file_path = os.path.join(file_directory, file_name)

    new_metadata = editor.song_metadata_dictionary

    # checking to see if image selected is the default. If it isn't will update the cover art to the selected image
    default_check = editor.dm_image_directory_select.currentText()
    if default_check != editor.default_image['image_label']:
        # update cover art to selected image
        image_directory = editor.image_directory_select['directory_name']
        image_name = editor.image_directory_dictionary['current_file']
        image_path = os.path.join(image_directory, image_name)
        new_metadata['cover_art'] = image_path
        change_image = True  # updating change image flag so program knows to change the cover art
    else:
        change_image = False

    print(f"new metadata: {new_metadata}")

    export_type_check_state = editor.cb_export_file.checkState()
    if export_type_check_state is Qt.CheckState.Checked:
        export_type = editor.song_directory_dictionary['export_type']
    else:
        export_type = None

    make_copy_check_state = editor.cb_copy_file_to_directory.checkState()
    if make_copy_check_state is Qt.CheckState.Checked:
        make_copy = True
    else:
        make_copy = False

    move_to_directory_check_state = editor.cb_move_to_directory.checkState()
    if move_to_directory_check_state is Qt.CheckState.Checked:
        move_to_directory = True
    else:
        move_to_directory = False

    audio.save_file_metadata(file_path, new_metadata, change_image, export_type, make_copy, move_to_directory)

    # TODO: does old metadata dictionary need to be updated?
