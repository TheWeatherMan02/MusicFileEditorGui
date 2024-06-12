import os

Song_Metadata = {'title': "",
                 'artist': "",
                 'album': "",
                 'year': "",
                 'genre': "",
                 'track_number': "",
                 'cover_art': ""
                 }

Directory_Template = {'directory_name': "",
                      'directory_type': "",
                      'files': {},  # format: {file name, file path}
                      'current_file': "",
                      'export_type': "",  # only used in the song directory
                      'add_path': "",
                      'add_url': ""
                      }

# TODO: make proper default image
Default_Image = {'image_path': os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_files", "episode_1.jpeg"),
                 'image_label': "-- Default --"
                 }

# ####---------------------------------------------------------

Defaults = {'song_metadata': Song_Metadata,
            'directory_template': Directory_Template,
            'default_image': Default_Image
            }
