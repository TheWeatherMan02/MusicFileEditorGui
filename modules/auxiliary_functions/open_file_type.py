def open_mp3_file(file_path, write_to_file):
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3, ID3NoHeaderError

    file_type = "mp3"
    no_header_found = None

    while True:
        try:
            audio = MP3(file_path, ID3=ID3)
            break
        except ID3NoHeaderError:
            print("!!! (open_mp3_file) ID3NoHeaderError: no ID3 header detected in file")
            if write_to_file is True:  # want open file anyway because we will write new metadata to it
                print("Creating ID3 header")
                audio = ID3()
                no_header_found = file_path  # saving file if there is no header found requires a file path
                break

            else:  # since file has no metadata, can exit the function
                print("File contains no metadata, exiting loop")
                return None
        except Exception as e:
            print(f"!!! (open_mp3_file) Unexpected error occurred: {e}")
            return None

    return audio, file_type, no_header_found


def open_mp4_file(file_path):
    from mutagen.mp4 import MP4

    file_type = "mp4"

    try:
        audio = MP4(file_path)
    except Exception as e:
        print(f"!!! (open_mp4_file) Unexpected error occurred: {e}")
        return None

    return audio, file_type


def open_ogg_file(file_path):
    from mutagen.oggvorbis import OggVorbis, error as OggVorbisError

    file_type = "ogg"

    try:
        audio = OggVorbis(file_path)
    except OggVorbisError as e:
        print("!!! (open_ogg_file) Error opening ogg file")
        print(f"!!! (open_ogg_file) Error type: {e}")
        return None
    except Exception as e:
        print(f"!!! (open_ogg_file) Unexpected error occurred: {e}")
        return None

    return audio, file_type
