import requests
import json

class InternalError(Exception):
	pass

class AuthorizationRequiredError(Exception):
	pass

class ForbiddenError(Exception):
	pass

class CherryMusicAPI(object):
	def __init__(self, url):
		self.url = url
		self.logged_in = False

		self._session = requests.Session()

	#### System-y things ####
	def login(self, username, password):
		r = self._session.post(self.url, data={ 'username': username, 'password': password, 'login': 'login' })

		# NOTE: No real way to check login results, so we'll just attempt to grab the motd.

		self.logged_in = True
		try:
			self.motd()
		except AuthorizationRequiredError:
			self.logged_in = False

		return self.logged_in

	def logout(self):
		self._call('logout')

	def heartbeat(self):
		self._call('heartbeat')

	def motd(self):
		r = self._call('getmotd')

		return (r['type'], r['data'])

	def get_encoders(self):
		r = self._call('getencoders')

		return r

	def get_decoders(self):
		r = self._call('getdecoders')

		return r

	def transcoding_enabled(self):
		r = self._call('transcodingenabled')

		return bool(r)

	# NOTE: blocks.
	def update_db(self):
		r = self._call('updatedb')

		return r

	def get_configuration(self):
		r = self._call('getconfiguration')

		return r

	# FIXME: broken?
	def fetch_album_art_urls(self, search_term):
		r = self._call('fetchalbumarturls', searchterm=search_term)

		print r

	#### Playlist things ####
	def search(self, search_string):
		r = self._call('search', searchstring=search_string)

	def list_directories(self, directory='', compact=False, filter=None):
		kwargs = dict(directory=directory)

		fn = 'listdir'
		if compact:
			fn, kwargs['filterstr'] = 'compactlistdir', filter

		return self._call(fn, **kwargs)

	def show_playlists(self, sort='created', filter=''):
		r = self._call('showplaylists', sortby=sort, filterby=filter)

		return r

	def remember_playlist(self, playlist=[]):
		r = self._call('rememberplaylist', playlist=playlist)

	def restore_playlist(self):
		return self._call('restoreplaylist')

	def save_playlist(self, playlist, public, playlist_name, overwrite=False):
		r = self._call('saveplaylist', playlist=playlist, public=public, playlistname=playlist_name, overwrite=overwrite)

		print r

	def delete_playlist(self, playlist_id):
		r = self._call('deleteplaylist', playlistid=playlist_id)

		return (r == 'success', r)

	def load_playlist(self, playlist_id):
		r = self._call('loadplaylist', playlistid=playlist_id)

		return r

	def random_playlist(self):
		return self._call('generaterandomplaylist')

	def change_playlist(self, playlist_id, attr, value):
		r = self._call('changeplaylist', plid=playlist_id, attribute=attr, value=value)

		return (r == 'success', r)

	def download_playlist(self, playlist_id, hostaddr, type='pls'):
		if type == 'pls':
			fn = 'downloadpls'
		elif type == 'm3u':
			fn = 'downloadm3u'
		else:
			raise NotImplementedError('Invalid type: {0}'.format(type))

		r = self._call(fn, plid=playlist_id, hostaddr=hostaddr, use_json=False)

		return r

	# NOTE: returns funky default info when path is not found.
	def get_song_info(self, path):
		r = self._call('getsonginfo', path=path)

		# NOTE: this api call is... "special".
		r = json.loads(r)

		return r

	def check_download(self, file_list):
		r = self._call('downloadcheck', filelist=file_list)

		return (r == 'ok', r)

	#### User administration things ####
	def get_user_options(self):
		r = self._call('getuseroptions')

		return r

	def set_user_option(self, key, val, user_id=None):
		kwargs = dict(optionkey=key, optionval=val)

		fn = 'setuseroption'
		if user_id is not None:
			fn, kwargs['userid'] = 'setuseroptionfor', user_id

		r = self._call(fn, **kwargs)

		return (r == 'success', r)

	def get_user_list(self):
		return self._call('getuserlist')

	def add_user(self, username, password, admin):
		r, ret = '', True

		try:
			r = self._call('adduser', username=username, password=password, isadmin=admin)
		except InternalError, err:
			ret = False

		return (ret, r)

	def delete_user(self, user_id):
		r = self._call('userdelete', userid=user_id)

		return (r == 'success', r)

	def change_user_password(self, oldpassword, newpassword, username=''):
		r = self._call('userchangepassword', oldpassword=oldpassword, newpassword=newpassword, username=username)

		return (r == 'success', r)

	#### Utility ####
	def get_playables(self):
		""" DEPRECATED """
		raise NotImplementedError()

	def _call(self, func, use_json=True, *args, **kwargs):
		if not self.logged_in:
			raise AuthorizationRequiredError('You must login before making API calls.')

		data = { 'data': json.dumps(kwargs) }
		r = self._session.post('{0}/api/{1}'.format(self.url, func), data=data)

		ret = None
		if r.status_code == 500:
			raise InternalError(r.text)
		elif r.status_code == 401:
			raise AuthorizationRequiredError()
		elif r.status_code == 403:
			raise ForbiddenError()
		elif r.status_code == 200:
			if use_json:
				ret = json.loads(r.text)
				ret = ret['data']
			else:
				ret = r.text

		return ret

api = CherryMusicAPI(None)