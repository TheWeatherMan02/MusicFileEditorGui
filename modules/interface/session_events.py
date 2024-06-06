from PyQt6.QtWidgets import QFileDialog

import os


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
    if directory_type == "image":
        from modules.dictionaries.file_types import Image_File_Extension
        file_extension_list = Image_File_Extension
    elif directory_type == "song":
        from modules.dictionaries.file_types import Audio_File_Extensions
        file_extension_list = Audio_File_Extensions
    else:
        print("!!! (error) unknown directory type: {0}".format(directory_type))
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


def le_or_dm_change(parent):
    print(type(parent))
    