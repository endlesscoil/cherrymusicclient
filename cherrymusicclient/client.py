from .api import api
from .library import Playlist

class CherryMusicClient(object):
	def __init__(self, url, username, password):
		self.url = api.url = url

		self.username = username
		self.password = password
		self.playlists = []

		self.login()

	def login(self):
		return api.login(self.username, self.password)

	def logout(self):
		api.logout()

	def load_playlists(self):
		playlists = api.show_playlists()

		for playlist in playlists:
			self.playlists.append(Playlist(playlist))