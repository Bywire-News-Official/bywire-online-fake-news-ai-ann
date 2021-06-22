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


from Util.Const import Const
import os, os.path
import codecs
import re

# Class to connect to email server and send error reports 
class Settings(object):
	ENCODING = 'utf-8'

	def __init__(self, path):
		self.m_path	 = path
		self.m_settings	 = {}
		self.read()

	def read(self):
		if not(os.path.exists(self.m_path)):
			self.m_settings = {}
			return
		with codecs.open(self.m_path, 'r', encoding=Settings.ENCODING) as infile:
			self.m_settings = dict([[value.strip() for value in item.split('=')] for item in infile if item.count('=')])
			self.m_settings['last_timestamp'] = int(self.m_settings['last_timestamp']) if'last_timestamp' in self.m_settings else 0
		return 

	def write(self):
		backup_path = self.m_path+".bak"
		with codecs.open(backup_path, 'w', encoding=Settings.ENCODING) as outfile:
			outfile.write("\n".join(["{0: <30s} = {1: <30s}".format(key, str(value)) for (key, value) in self.m_settings.items()]))
		os.replace(backup_path, self.m_path)

	def flush(self):
		self.write()
		self.read()

	def __getitem__(self, key):
		return self.m_settings[key] if key in self.m_settings else None
	
	def __setitem__(self, key, value):
		self.m_settings[key] = value
	
