from .api import api

class Playlist(object):
	def __init__(self, data):
		self.id = data['plid']
		self.title = data['title']
		self.owner = data['owner']
		self.created_on = data['created']
		self.public = data['public']

		self.tracks = []

		self.load()

	def load(self):
		playlist = api.load_playlist(self.id)
		for track in playlist:
			self.tracks.append(Track(track))

	def save(self):
		pass

class Track(object):
	def __init__(self, data):
		self.path = data['path']
		self.urlpath = data['urlpath']
		self.label = data['label']
		self.type = data['type']

		self.album = ''
		self.track_number = -1
		self.title = ''
		self.artist = ''
		self.length = -1

		self.get_info()

	def get_info(self):
		info = api.get_song_info(self.path)
		
		self.album = info['album']
		self.track_number = info['track']
		self.title = info['title']
		self.artist = info['artist']
		self.length = info['length']