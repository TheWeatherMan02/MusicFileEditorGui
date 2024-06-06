No_Selection = "None Selected"

Song_Metadata = {'title': No_Selection,
                 'artist': No_Selection,
                 'album': No_Selection,
                 'genre': No_Selection,
                 'track_number': No_Selection,
                 'release_date': No_Selection,
                 'cover_art': No_Selection,
                 'file_type': No_Selection
                 }

Directory_Template = {'directory_name': No_Selection,
                      'directory_type': No_Selection,
                      'files': {}  # format: {file name, file path}
                      }

Add_to_Directory = {'image_path': "",
                    'image_url': "",
                    'song_path': "",
                    'song_url': ""
                    }

# ####---------------------------------------------------------

Defaults = {'song_metadata': Song_Metadata,
            'directory_template': Directory_Template,
            'add_to_directory': Add_to_Directory
            }
