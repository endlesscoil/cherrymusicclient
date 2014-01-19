from .api import api
from .library import Playlist

class CherryMusicClient(object):
	def __init__(self):
		self.url = api.url = url
		self.playlists = []
		self.current_playlist = None

	def login(self, username, password):
		return api.login(username, password)

	def logout(self):
		api.logout()

	def load_playlists(self):
		playlists = api.show_playlists()

		for playlist in playlists:
			self.playlists.append(Playlist(playlist))

	def select_playlist(self, name):
		self.current_playlist = None

		for playlist in self.playlists:
			if playlist.title == name:
				self.current_playlist = playlist

		return self.current_playlist

	@property
	def url(self):
	    return self._url

	@url.setter
	def url(self, value):
	    self._url = value
	    api.url = value