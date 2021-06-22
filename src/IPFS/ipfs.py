"""

	Copyright Sikkema Software B.V. 2021 - All rights Reserved

	You may not copy, reproduce, distribute, modify or create 
	derivative works sell or offer it for sale or use such content
	to construct any kind of database or disclose the source without
	explicit permission of the copyright holder. You may not alter
	or remove any copyright or other notices from copies of the content. 
	For permission to use the content please contact sikkemasoftware@gmailcom

	All content and data is provided on an as is basis. The copyright holder
	makes no claisms to the accuracy, complentness, currentness, suistainability
	or validity of the code and information and will not be liable for any
	errors, omissions, or delays in this information or any losses, injuries
	or damages arising from the use of this software. 

"""


import time
import os, os.path
import sys
from gevent import monkey
monkey.patch_all(subprocess=True)

if __name__=="__main__":
	print(os.getcwd())
	sys.path.append(os.path.join(os.getcwd(), ".."))


import re
import threading
import requests, grequests
import json
import io
from datetime import datetime, timedelta
from IPFS.IPFSConst import IPFSConst
from Util.Const import Const
from Util.Config import Config
from Util.Log import Log

class IPFSGateway(object):
	def __init__(self, config):
		self.m_config = config
		IPFSGateway.BASE_URL	= config[IPFSConst.CONFIG_SERVER_URL].format(**{'port': config[IPFSConst.CONFIG_SERVER_PORT]})

	def execute_sync(self, command, args, file_data, callback):
		if callback is None:
			callback = lambda x: 1
		if (isinstance(args, type([]))):
			#Log.debug(args)
			url_args = '?' + "&".join(["{0:s}={1:s}".format(key, value) for (key, value) in args])
		else:
			url_args = '?' + "&".join(["{0:s}={1:s}".format(key, value) for key, value in args.items()])
		url = IPFSGateway.BASE_URL+command+url_args
		#Log.debug('Execute', url, command, callback)
		if not(file_data is None):
			headers = {'Content-type' : 'multipart/form-data'}
			#headers = {'Content-type' : 'text/plain;charset=UTF-8'}

			url+'&arg='+str(file_data['file_name'])
			req = requests.post(url, files={'files': io.StringIO(file_data['content'])})
			callback(req.json())
		else:
			headers = {'Content-type' : 'application/x-www-form-urlencoded'}
			Log.info(url)
			req = requests.post(url, data=None, headers=headers)
			Log.info(req)
			Log.info(dir(req))
			Log.info(req.text)
			Log.info(json.loads(req.text))
			Log.info(req.json())
			callback(json.loads(req.text))
			#job = grequests.send(req, grequests.Pool(1))

	def execute(self, command, args, file_data, callback):
		if callback is None:
			callback = lambda x: 1
		if (isinstance(args, type([]))):
			#Log.debug(args)
			url_args = '?' + "&".join(["{0:s}={1:s}".format(key, value) for (key, value) in args])
		else:
			url_args = '?' + "&".join(["{0:s}={1:s}".format(key, value) for key, value in args.items()])
		url = IPFSGateway.BASE_URL+command+url_args
		Log.info('Execute', url, command, callback)
		#Log.debug('Execute', url, command, callback)
		if not(file_data is None):
			headers = {'Content-type' : 'multipart/form-data'}
			#headers = {'Content-type' : 'text/plain;charset=UTF-8'}

			url+'&arg='+str(file_data['file_name'])
			req = grequests.post(url, files={'files': io.StringIO(file_data['content'])}, callback=callback)
		else:
			headers = {'Content-type': 'application/x-www-form-urlencoded'}
			Log.info("IPFS - execute", command, args, file_data, callback)
			req = grequests.post(url, data=None, headers=headers, callback=callback)
			Log.info(req)
		if not (req):
			Log.info("Invalid request")
		else:
			job = grequests.send(req, grequests.Pool(1))
			Log.info(job)

	def getHash(self, file_name, file_data):
		args = {'arg': file_name, 'onlyhash': 'true'}
		files = {'file_name': str(file_name), 'content': json.dumps(file_data)}
		data = self.execute_sync('add', args, files, None)
		Log.info(data)
		if 'Hash' in data:
			return data['Hash']
		return ""

	def publish(self, channel, data):
		self.execute('pubsub/pub', [('arg', channel), ('arg', str(data)+'\n')], None, None)

	def subscribe(self, channel):
		self.execute('pubsub/sub', {'arg': channel, 'discover':'True'}, None, None)

	def unsubscribe(self, channel):
		self.execute('pubsub/cancel', {'arg': channel}, None, None)
			
	def setPin(self, filename, callback):
		self.execute("pin/add", {"arg": filename}, None, callback)

	def retrieveDocumentFromHash(self, hash, callback):
		self.execute_sync("cat", {"arg": hash}, None, callback)
		
	def retrieveDocument(self, filename, callback):
		self.execute("files/read", {"arg": filename}, None, callback)

	def exists(self, path, callback):
		self.execute('files/ls', {'arg': path}, None, callback)

	def createDir(self, path):
		self.execute('files/mkdir', {'arg': path}, None, None)
		self.setPin(path, None)

	def setup(self):
		self.createDir('/bywire')
		self.createDir('/bywire/indices')
		self.createDir('/bywire/data')
		self.exists('/bywire', lambda x: Log.info("Setup - exists /bywire", x))
	
	def storeDocument(self, file_name, file_data, callback):
		cmd = "files/write"
		args = {'arg': file_name, 'create': 'true'}
		files = {'file_name': str(file_name), 'content': json.dumps(file_data)}
		self.execute(cmd, args, files, callback)
		self.setPin(file_name, None)
		cmd = "files/stat"
		args = {'arg': file_name}
		self.execute(cmd, args, None, callback)

	def updateDocument(self, file_name, file_data, callback):
		cmd = "files/write"
		args = {'arg': file_name}
		files = {'file_name': str(file_name), 'content': json.dumps(file_data)}

		self.execute(cmd, args, files, callback)
		self.setPin(file_name, None)

	def connect(self, peer_id):
		cmd = "swarm/connect"
		args = {'arg': peer_id}
		self.execute(cmd, args, None, callback)


		
def parse_response(response, **kwargs):
	Log.info('ParsingResponse')
	Log.info('Response', response.status_code)
	Log.info('Content', response.content)


    
if __name__=="__main__":
	# set pythonpath to toplevel to run
	with Config(Const.CONFIG_PATH) as config:
		log = Log(config)
		gateway = IPFSGateway(config)
		gateway.setup()
		result = gateway.getHash("/xxx", 'This is sample content', None)
		print(result)
		#gateway.execute('files/ls', {"arg": "/"}, None, parse_response)
		#time.sleep(1)
		#file_name = 'article_test6.txt'
		#gateway.execute('files/write', {"arg": "/bywire/indices/"+file_name, "create": "true"}, {'file_name': file_name, 'content': 'This is my new content'}, parse_response)



