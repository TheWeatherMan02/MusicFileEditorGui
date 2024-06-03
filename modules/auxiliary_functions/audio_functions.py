from modules.dictionaries.file_types import Audio_File_Types

from mutagen import File


def identify_file_type(file_path):
    audio = File(file_path)
    if audio is None:
        print("Unknown file type.")
    else:
        print(f"File type: {audio.mime[0]}")  # first element is usually sufficient

    return audio.mime[0]


def get_file_metadata(file_path, file_type):
    if file_type in Audio_File_Types:
        if file_type == 'audio/mp4':
            from mutagen.mp4 import MP4

            try:
                audio = MP4(file_path)
                tags = audio.tags

                print(tags)

                title = tags.get('\xa9nam', ["Title tag not found."])[0]
                print(title)

            except Exception as e:
                return f"An error occurred while getting file metadata: {e}"

        elif file_type == 'audio/mp3':
            from mutagen.mp3 import MP3
            from mutagen.id3 import ID3, TIT2

            try:
                audio = MP3(file_path, ID3=ID3)
                id3_tags = audio.tags

                if TIT2 in id3_tags:
                    title = id3_tags[TIT2].text[0]
                    print(title)
                else:
                    print("could not find title for mp3 file")

            except Exception as e:
                return f"An error occurred while getting file metadata: {e}"

        else:
            print("! (File Type Error) file type \"{0}\" has not been integrated yet".format(file_type))

    else:
        print("! (File Type Error) file type \"{0}\" not found in main file type list".format(file_type))
