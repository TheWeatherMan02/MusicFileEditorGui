"""
list of keys associated with file types in the same order as the song metadata
directory used locally in the editor
"""

mp3_tags = {'title': ["TIT2"],
            'artist': ["TPE1"],
            'album': ["TALB"],
            'year': ["TDRC", "TYER"],
            'genre': ["TCON"],
            'track_number': ["TRCK"],
            'cover_art': ["APIC:"]
            }

ogg_tags = {'title': "TITLE",
            'artist': "ARTIST",
            'album': "ALBUM",
            'year': "DATE",
            'genre': "GENRE",
            'track_number': "TRACKNUMBER",
            'cover_art': "METADATA_BLOCK_PICTURE"
            }
