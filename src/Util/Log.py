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


import os, os.path
import sys
sys.path.append(os.getcwd())
from Util.Config import Config
from Util.Const import Const
from datetime import datetime
import traceback
import logging
import glob
import re

class Log(object):	
	INSTANCE = None

	LEVELS = {	'error': logging.ERROR,
				'info': logging.INFO,
				'warn': logging.WARNING,
				'debug': logging.DEBUG
			}
	
	def __init__(self, config):
		print('Configuring Log')
		print(Log.INSTANCE)
		if Log.INSTANCE is None:
			self.m_config = config
			self.m_level = Log.LEVELS[self.m_config[Const.LOG_LEVEL].lower()]		
			logging.basicConfig(level=self.m_level)
			Log.INSTANCE = logging.getLogger('BaseLogger')
		else:
			return None
			#return Log.INSTANCE
		self.m_path = self.m_config[Const.LOG_PATH]
		self.m_path = os.path.join(*self.m_path.split('/'))
		self.m_format = self.m_config[Const.LOG_FORMAT]
		
		self.m_path = re.sub('[{]date[}]', datetime.now().strftime('%Y%m%d'), self.m_path) 

		Log.INSTANCE.setLevel(self.m_level)

		tmp = re.sub('[{]count[}]', '*', self.m_path)
		files = [file for file in glob.glob(tmp)]
		tmp = self.m_path.replace('\\', '\\\\')
		tmp = re.sub('[{]count[}]', '([0-9]+)', tmp)
		tmp = tmp.replace('[.]', '')
		matches = [re.search(tmp, file) for file in files]
		counts = [int(item.group(1)) for item in matches if item]
		print(counts)
		self.m_path = re.sub('[{]count[}]', "{0:0>4d}".format(max(counts + [-1])+1), self.m_path)
		print(self.m_path)
		if not(os.path.exists(self.m_path)):
			os.makedirs(self.m_path)
		for node in self.m_config.getNodes(Const.LOG_LOGGER):
			logger = logging.getLogger(node[Const.LOGGER_NAME])
			level = Log.LEVELS[node[Const.LOGGER_LEVEL].lower()]
			print(logger, level, self.m_level)
			logger.setLevel(level)
			destination = node[Const.LOGGER_DESTINATION]
			if (destination.lower() == 'screen'):
				handler = logging.StreamHandler()
			else:
				destination = os.path.join(os.path.join(self.m_path, destination))				
				handler = logging.FileHandler(destination)
			formatter = logging.Formatter(self.m_format)
			handler.setFormatter(formatter)
			Log.INSTANCE.addHandler(handler)
	
	@staticmethod
	def log(priority, *message):
		message = [traceback.format_stack()[-2].split('\n')[0], *message]
		Log.INSTANCE(Log.LEVELS[priority], message)
		
	@staticmethod
	def critical(*message):
		message = [traceback.format_stack()[-2].split('\n')[0], *message]
		Log.INSTANCE.critical(message)

	@staticmethod
	def exception():
		message = traceback.format_stack()
		Log.INSTANCE.error(" ".join([str(item) for item in message]), exc_info=True)
		
	@staticmethod
	def error(*message):
		message = [traceback.format_stack()[-2].split('\n')[0], *message]
		Log.INSTANCE.error(" ".join([str(item) for item in message]))
		
	@staticmethod
	def info(*message):
		message = [traceback.format_stack()[-2].split('\n')[0], *message]

		Log.INSTANCE.info(" ".join([str(item) for item in message]))
		
	@staticmethod
	def warn(*message):
		message = [traceback.format_stack()[-2].split('\n')[0], *message]

		Log.INSTANCE.warn(" ".join([str(item) for item in message]))
		

	@staticmethod
	def debug(*message):

		message = [traceback.format_stack()[-2].split('\n')[0], *message]
		Log.INSTANCE.debug( " ".join([str(item) for item in message]))

	@staticmethod
	def exception(*message):

		message = [traceback.format_stack()[-2].split('\n')[0], *message]
		Log.INSTANCE.exception( " ".join([str(item) for item in message]), exc_info=True)
