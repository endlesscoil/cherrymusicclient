import logging
import urllib

from .api import api
from .decorators import get_track_info

class Playlist(object):
    def __init__(self, data):
        self.log = logging.getLogger(self.__class__.__name__)

        self.id = data['plid']
        self.title = data['title']
        self.owner = data['owner']
        self.created_on = data['created']
        self.public = data['public']

        self.tracks = []
        self.current_track = -1

        self.load()

    def load(self):
        playlist = api.load_playlist(self.id)
        for track in playlist:
            self.tracks.append(Track(track))

    def save(self):
        pass

    def next_song(self):
        next_index = self.current_track + 1
        if next_index > len(self.tracks) - 1:
            return None

        self.current_track = next_index
        return self.tracks[next_index]


class Track(object):
    def __init__(self, data, force_info=False):
        self.log = logging.getLogger(self.__class__.__name__)

        self.path = data['path']
        self.urlpath = data['urlpath']
        self.label = data['label']
        self.type = data['type']

        self._album = ''
        self._track_number = -1
        self._title = ''
        self._artist = ''
        self._length = -1
        self._retrieved_song_info = False

        if force_info:
            self.get_info()

    def get_info(self):
        info = api.get_song_info(urllib.unquote(self.urlpath))

        self.album = info['album']
        self.track_number = info['track']
        self.title = info['title']
        self.artist = info['artist']
        self.length = info['length']

        self._retrieved_song_info = True

    @property
    @get_track_info
    def artist(self):
        return self._artist

    @artist.setter
    def artist(self, value):
        self._artist = value

    @property
    @get_track_info
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    @get_track_info
    def album(self):
        return self._album

    @album.setter
    def album(self, value):
        self._album = value

    @property
    @get_track_info
    def track_number(self):
        return self._track_number

    @track_number.setter
    def track_number(self, value):
        self._track_number = value

    @property
    @get_track_info
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value