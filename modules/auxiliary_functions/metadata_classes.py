"""
This file contains classes used for getting and setting metadata for specific file types.

Classes are used so that a file's metadata can be accessed using its file type string found during runtime.

The classes are stored separately from the audio functions file to reduce clutter
"""
import os
import shutil
import filetype


class GetMetadata:
    def __init__(self, audio_file):
        self.audio_file = audio_file

        self.metadata = {}  # initializing metadata dictionary

    def get_mp3_metadata(self):
        from mutagen.id3 import ID3NoHeaderError
        from modules.dictionaries.metadata_keys import mp3_tags

        try:
            for key in mp3_tags:
                for tag in mp3_tags[key]:
                    if key == 'cover_art' and tag in self.audio_file:
                        cover_art = self.audio_file[tag].data
                        self.metadata.update({key: cover_art})
                        print(f"Found metadata for {key}")
                    elif tag in self.audio_file:
                        tag_metadata = self.audio_file[tag].text[0]
                        self.metadata.update({key: tag_metadata})
                        print(f"Found metadata for {key}")
                    else:
                        self.metadata.update({key: ""})
                        print(f"!!! (get_mp3_metadata) No value found for {key} in tags")

        except ID3NoHeaderError:
            print("!!! (get_mp3_metadata) No ID3 header found")

        except Exception as e:
            print("!!! (get_mp3_metadata) Exception occurred when getting mp3 metadata")
            print(f"Exception message: {e}")

        return self.metadata


class SaveMetadata:
    def __init__(self, audio_file, new_metadata, change_image, file_path, new_directory, no_header_found):
        self.audio_file = audio_file
        self.new_metadata = new_metadata
        self.change_image = change_image
        self.file_path = file_path
        self.new_directory = new_directory
        self.no_header_found = no_header_found

    def change_directory(self):
        destination_file = os.path.join(self.new_directory, os.path.basename(self.file_path))

        # move file to new directory
        shutil.move(str(self.file_path), str(destination_file))
        print(f"Moved {self.file_path} to {destination_file}")

    def save_mp3_metadata(self):
        from mutagen.id3 import TIT2, TPE1, TALB, TDRC, TYER, TCON, TRCK, APIC

        try:
            # add title
            self.audio_file.tags.add(TIT2(encoding=3, text=self.new_metadata['title']))
            print("!!! (save_mp3_metadata) Successfully added metadata tag for: 'title'")
            # add artist
            self.audio_file.tags.add(TPE1(encoding=3, text=self.new_metadata['artist']))
            print("!!! (save_mp3_metadata) Successfully added metadata tag for: 'artist'")
            # add album
            self.audio_file.tags.add(TPE1(encoding=3, text=self.new_metadata['artist']))
            print("!!! (save_mp3_metadata) Successfully added metadata tag for: 'artist'")
            # add year
            self.audio_file.tags.add(TALB(encoding=3, text=self.new_metadata['album']))
            print("!!! (save_mp3_metadata) Successfully added metadata tag for: 'album'")
            # add genre
            self.audio_file.tags.add(TDRC(encoding=3, text=self.new_metadata['year']))
            print("!!! (save_mp3_metadata) Successfully added metadata tag for: 'year-TDRC'")
            self.audio_file.tags.add(TYER(encoding=3, text=self.new_metadata['year']))
            print("!!! (save_mp3_metadata) Successfully added metadata tag for: 'year-TYER'")
            # add track number
            self.audio_file.tags.add(TCON(encoding=3, text=self.new_metadata['genre']))
            print("!!! (save_mp3_metadata) Successfully added metadata tag for: 'genre'")
            # add cover art
            self.audio_file.tags.add(TRCK(encoding=3, text=self.new_metadata['track_number']))
            print("!!! (save_mp3_metadata) Successfully added metadata tag for: 'track_number'")
            # only update cover art if the new art is not the default art
            if self.change_image is True:
                print("!!! (save_mp3_metadata) Getting ready to add metadata tag: 'cover_art'")
                # get the mime type of the image
                mime_type = filetype.guess_mime(self.new_metadata['cover_art'])
                with open(self.new_metadata['cover_art']) as img_file:
                    image_data = img_file.read()
                apic_frame = APIC(encoding=3, mime=mime_type, type=3, desc='Cover', data=image_data)
                self.audio_file.tags.delall('APIC')  # deletes existing image if there is one
                self.audio_file.tags.add(apic_frame)
                print("!!! (save_mp3_metadata) Successfully added metadata tag for: 'cover_art'")

            # save changes
            print("!!! (save_mp3_metadata) Getting ready to save metadata to file")
            if self.no_header_found is not None:
                self.audio_file.save()
            else:
                print("!!! (save_mp3_metadata) Saving data to new ID3 header")
                file_path = self.no_header_found
                self.audio_file.save(file_path)
            print("Metadata successfully changed")

            if self.new_directory != "":
                print("Moving file to new directory")
                self.change_directory()

        except Exception as e:
            print("!!! (save_mp3_metadata) Exception occurred when saving mp3 metadata")
            print(f"Exception message: {e}")
