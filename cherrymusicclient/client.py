import requests
import json

class InternalError(Exception):
	pass

class AuthorizationRequiredError(Exception):
	pass

class ForbiddenError(Exception):
	pass

class CherryMusicClient(object):
	def __init__(self, url):
		self._url = url
		self._session = requests.Session()

	def _login(self, username, password):
		r = self._session.post(self._url, data={ 'username': username, 'password': password, 'login': 'login' })
		#print r.text

		for c in r.cookies:
			print c

	def motd(self):
		r = self._call('getmotd')

		return (r['type'], r['data'])

	def search(self, search_string):
		r = self._call('search', searchstring=search_string)

	def listdir(self, directory=''):
		r = self._call('listdir', directory=directory)

	def downloadcheck(self, file_list):
		r = self._call('downloadcheck', filelist=file_list)

		return (r == 'ok', r)

	def getuseroptions(self):
		r = self._call('getuseroptions')

		return r

	def heartbeat(self):
		self._call('heartbeat')

	def setuseroption(self, key, val):
		r = self._call('setuseroption', optionkey=key, optionval=val)

		return (r == 'success', r)

	def setuseroptionfor(self, user_id, key, val):
		r = self._call('setuseroptionfor', userid=user_id, optionkey=key, optionval=val)

		return (r == 'success', r)

	# FIXME: broken?
	def fetchalbumarturls(self, search_term):
		r = self._call('fetchalbumarturls', searchterm=search_term)

		print r

	def compactlistdir(self, directory, filterstr=None):
		r = self._call('compactlistdir', directory=directory, filterstr=filterstr)

		return r

	def rememberplaylist(self, playlist):
		r = self._call('rememberplaylist', playlist=playlist)

	def saveplaylist(self, playlist, public, playlist_name, overwrite=False):
		r = self._call('saveplaylist', playlist=playlist, public=public, playlistname=playlist_name, overwrite=overwrite)

		print r

	def deleteplaylist(self, playlist_id):
		r = self._call('deleteplaylist', playlistid=playlist_id)

		return (r == 'success', r)

	def loadplaylist(self, playlist_id):
		r = self._call('loadplaylist', playlistid=playlist_id)

		return (r == 'success', r)

	def generaterandomplaylist(self):
		return self._call('generaterandomplaylist')

	def changeplaylist(self, playlist_id, attr, value):
		r = self._call('changeplaylist', plid=playlist_id, attribute=attr, value=value)

		return (r == 'success', r)

	def restoreplaylist(self):
		return self._call('restoreplaylist')

	def getplayables(self):
		""" DEPRECATED """
		raise NotImplementedError()

	def getuserlist(self):
		return self._call('getuserlist')

	def adduser(self, username, password, admin):
		r = ''
		ret = True

		try:
			r = self._call('adduser', username=username, password=password, isadmin=admin)
		except InternalError, err:
			ret = False

		return (ret, r)

	def userchangepassword(self, oldpassword, newpassword, username=''):
		r = self._call('userchangepassword', oldpassword=oldpassword, newpassword=newpassword, username=username)

		return (r == 'success', r)

	def userdelete(self, user_id):
		r = self._call('userdelete', userid=user_id)

		return (r == 'success', r)

	def showplaylists(self, sort='created', filter=''):
		r = self._call('showplaylists', sortby=sort, filterby=filter)

		return r

	def logout(self):
		self._call('logout')

	def downloadpls(self, playlist_id, hostaddr):
		r = self._call('downloadpls', plid=playlist_id, hostaddr=hostaddr, use_json=False)

		return r

	def downloadm3u(self, playlist_id, hostaddr):
		r = self._call('downloadm3u', plid=playlist_id, hostaddr=hostaddr, use_json=False)

		return r

	# NOTE: returns funky default info when path is not found.
	def getsonginfo(self, path):
		r = self._call('getsonginfo', path=path)

		return r

	def getencoders(self):
		r = self._call('getencoders')

		return r

	def getdecoders(self):
		r = self._call('getdecoders')

		return r

	def transcodingenabled(self):
		r = self._call('transcodingenabled')

		return bool(r)

	# NOTE: blocks.
	def updatedb(self):
		r = self._call('updatedb')

		return r

	def getconfiguration(self):
		r = self._call('getconfiguration')

		return r

	def _call(self, func, use_json=True, *args, **kwargs):
		data = { 'data': json.dumps(kwargs) }

		r = self._session.post('{0}/api/{1}'.format(self._url, func), data=data)
		print 'call', func, data, '->', r.status_code

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