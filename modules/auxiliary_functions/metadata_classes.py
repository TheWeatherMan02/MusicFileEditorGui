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

    def get_ogg_metadata(self):
        from modules.dictionaries.metadata_keys import ogg_tags
        from mutagen.oggvorbis import error as OggVorbisError

        try:
            for key in ogg_tags:
                tag = ogg_tags[key]
                if key == 'cover_art' and tag in self.audio_file:
                    import base64
                    import struct
                    # make a dictionary to hold all the image data

                    image_dictionary = {}

                    # get and decode data
                    encoded_picture_data = self.audio_file[tag][0]
                    picture_data = base64.b16decode(encoded_picture_data)

                    offset = 0  # parsing data using an offset to keep track of position in data

                    image_dictionary['picture_type'] = struct.unpack('>I', picture_data[offset:offset+4])
                    offset += 4

                    mime_type_length = struct.unpack('>I', picture_data[offset:offset+4])
                    offset += 4

                    image_dictionary['mime_type'] = picture_data[offset:offset+mime_type_length].decode('ascii')
                    offset += mime_type_length

                    description_length, = struct.unpack('>I', picture_data[offset:offset+4])
                    offset += 4

                    image_dictionary['description'] = picture_data[offset:offset+description_length].decode('utf-8')
                    offset += description_length

                    # skipping width, height, color depth, and number of colors (4 bytes each)
                    offset += 4 * 4

                    image_data_length = struct.unpack('>I', picture_data[offset:offset+4])
                    offset += 4

                    # image data is now in raw binary form (could save by writing to file)
                    image_dictionary['image_data'] = picture_data[offset:offset+image_data_length]

                    self.metadata = image_dictionary['image_data']
                    print(f"Found metadata for {tag}")

                elif tag in self.audio_file:
                    tag_metadata = self.audio_file[key]
                    self.metadata.update({key: tag_metadata})
                    print(f"Found metadata for {tag}")
                else:
                    self.metadata.update({key: ""})
                    print(f"!!! (get_ogg_metadata) No value found for {key} in tags")

        except OggVorbisError:
            print("!!! (get_ogg_metadata) OggVorbisError occurred, check file type or header may be corrupted")
        except Exception as e:
            print(f"!!! (get_ogg_metadata) Unexpected error occurred {e}")


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

    def save_ogg_metadata(self):
        from modules.dictionaries.metadata_keys import ogg_tags
        from mutagen.oggvorbis import error as OggVorbisError

        try:
            for key in ogg_tags:
                tag = ogg_tags[key]
                if key == 'cover_art' and self.change_image is True:
                    import base64
                    import struct

                    # getting file mime type
                    mime_type = filetype.guess_mime(self.new_metadata['cover_art'])
                    with open(self.new_metadata['cover_art'], "rb") as image_file:
                        image_data = image_file.read()

                    picture_data = (
                            struct.pack('>I', 3) +  # Picture type: 3 = Front Cover
                            struct.pack('>I', len(mime_type)) + mime_type.encode('ascii') +  # MIME type
                            struct.pack('>I', len("")) + b"" +  # Description
                            struct.pack('>I', 0) +  # Width (optional)
                            struct.pack('>I', 0) +  # Height (optional)
                            struct.pack('>I', 0) +  # Color depth (optional)
                            struct.pack('>I', 0) +  # Number of colors (optional)
                            struct.pack('>I', len(image_data)) + image_data  # Image data
                    )

                    picture_data_base64 = base64.b64encode(picture_data).decode('ascii')

                    # add tag to ogg file
                    self.audio_file[tag] = [picture_data_base64]
                    print(f"!!! (save_ogg_metadata) Successfully added metadata tag for: '{key}'")

                else:
                    self.audio_file[tag] = self.new_metadata[key]
                    print(f"!!! (save_ogg_metadata) Successfully added metadata tag for: '{key}'")

            # saving changes to file
            self.audio_file.save()
            print("Metadata successfully changed")

            if self.new_directory != "":
                print("Moving file to new directory")
                self.change_directory()

        except OggVorbisError:
            print("!!! (save_ogg_metadata) OggVorbisError occurred, check file type or header may be corrupted")
        except Exception as e:
            print(f"!!! (save_ogg_metadata) Unexpected error occurred {e}")
