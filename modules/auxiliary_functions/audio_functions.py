import os.path

from modules.dictionaries.file_types import Audio_File_Types
from modules.auxiliary_functions import metadata_classes

from mutagen import File
from pydub import AudioSegment


def identify_file_type(file_path):
    audio = File(file_path)
    if audio is None:
        print("Unknown file type.")
    else:
        print(f"File type: {audio.mime[0]}")  # first element is usually sufficient

    return audio.mime[0]


def open_file(file_path, write_to_file=False):
    """
    This function searches if the file type is listed in the audio file tags.
    If it is listed in the tags the function will import the associated modules and attempt to open the file.

    Each file type contains a while loop. This loop tries to ensure that the file contains the header tag
    that holds the file data. If it does, the loop is broken manually and the program continues on.
    If the file does not contain a header, a no header exception specific to the file type is raised and
    the program creates the header tag as well as a flag indicating a tag was created before continuing.

    This feature is only necessary for writing metadata to a file, so it is controlled for using the argument
    "write_to_file". If this is false, the program will instead stop trying to open the file since it does not have any
    metadata in it.

    :param file_path:
    :return:
    """
    # getting file type and then importing the right modules
    audio_mime_type = identify_file_type(file_path)

    if audio_mime_type in Audio_File_Types:
        no_header_found = None  # initializing no header found tag
        try:
            if audio_mime_type == 'audio/mp4':
                from mutagen.mp4 import MP4
                file_type = "mp4"
                audio = MP4(file_path)

            elif audio_mime_type == 'audio/mp3':
                from mutagen.mp3 import MP3
                from mutagen.id3 import ID3, ID3NoHeaderError
                file_type = "mp3"
                while True:
                    try:
                        audio = MP3(file_path, ID3=ID3)
                        break
                    except ID3NoHeaderError:
                        print("!!! (open_file) no ID3 header detected in file")
                        if write_to_file is True:  # want open file anyway because we will write new metadata to it
                            print("Creating ID3 header")
                            audio = ID3()
                            no_header_found = file_path  # saving file if there is no header found requires a file path
                            break

                        else:  # since file has no metadata, can exit the function
                            print("File contains no metadata, exiting loop")
                            return None
            else:
                print("!!! (open_file) File type \"{0}\" has not been integrated yet".format(audio_mime_type))
                return None

        except Exception as e:
            print(f"!!! (open_file) Error occurred while opening file of type {audio_mime_type}")
            print(f"Exception type: {e}")

        else:
            # this code activates if no exceptions are encountered in the try block above
            # the no_header_found flag is only used when writing data to audio file
            return audio, file_type, no_header_found, audio_mime_type

    else:
        print("!!! (open_file) File type \"{0}\" not found in main file type list".format(audio_mime_type))
        return None


def get_file_metadata(file_path):
    metadata = {}  # initializing metadata dictionary
    audio, file_type, _, _ = open_file(file_path)

    if audio is None:
        print("returning to main function without opening file in path:")
        print(f"\t{file_path}")
    else:
        metadata_class = metadata_classes.GetMetadata(audio)

        file_metadata = getattr(metadata_class, "get_" + file_type + "_metadata")()
        metadata.update(file_metadata)

    return metadata


def save_file_metadata(file_path, new_metadata, change_image, export_type, make_copy, move_to_directory):
    # TODO: clean this function up into other functions to make this nicer (you can access functions in this file just
    #       by calling their name, see uses of open_file)
    audio, file_type, no_header_found, audio_mime_type = open_file(file_path)

    if export_type is not None:
        # need to export to another file type without changing the metadata in the original audio file
        file_root, _ = os.path.splitext(file_path)
        output_file_path = file_root + os.sep + export_type

        # check the mime type so the file can be exported
        if audio_mime_type == 'audio/mp3':
            audio_export = AudioSegment.from_mp3(file_path)
        else:
            # this will stop the save file metadata function
            raise ValueError(f"!!! (save_file_metadata) Unsupported audio format cannot be exported: {audio_mime_type}")

        # exporting the audio file
        audio_export.export(output_file_path, format=export_type)
        print(f"File converted and saved as {output_file_path}")

        # cleaning up variables
        del audio, file_type, no_header_found, audio_mime_type, file_path

        # opening new exported file
        file_path = output_file_path
        audio, file_type, no_header_found, _ = open_file(file_path)

    elif make_copy is True:
        file_root, file_extension = os.path.splitext(file_path)
        file_path = file_root + "(copy)" + file_extension  # renaming file path to copy file path

        # create the duplicate file
        audio.save(file_path)

        # clean up original audio variables
        del audio, file_type, no_header_found

        # open duplicate file to edit
        audio, file_type, no_header_found, _ = open_file(file_path)

    if move_to_directory is True:
        from modules.interface.session_events import select_directory
        new_directory, made_selection = select_directory()

        while made_selection is False:
            user_choice = input("!!! (save_file_metadata) No directory selected to move file to.\n"
                                "Do you still want to move the file to another directory ([y]/n): ")
            if user_choice == "Y" or user_choice == "y":
                new_directory, made_selection = select_directory()
            elif user_choice == "N" or user_choice == "n":
                print("You have decided not to move the file to another location")
                made_selection = True
            else:
                print(f"!!! (save_file_metadata) {user_choice} is an invalid input, please choose again.\n")
    else:
        new_directory = ""  # keeping the argument for no directory selected the same as in the select directory method

    if audio is None:
        print("returning to main function without opening file in path:")
        print(f"\t{file_path}")
    else:
        metadata_class = metadata_classes.SaveMetadata(audio, new_metadata, change_image, file_path, new_directory, no_header_found)

        save_metadata = getattr(metadata_class, "save_" + file_type + "_metadata")
        save_metadata()


if __name__ == "__main__":
    song_path = "/Users/spencer/PycharmProjects/MusicFileEditorGui/modules/test_files/01_Main_Theme.mp3"
    # song_metadata = get_mp3_metadata(song_path)
