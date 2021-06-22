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


from Util.Log import Log
from Util.Const import Const
import os, os.path
import json
from datetime import datetime, timedelta

class DataUtil(object):
	CHARACTER_LIMIT = 100000
	
	@staticmethod
	def clean(variable):
		""" Guards against sql insertion and templating attacks. 
			Don't use regular expressions for the cleaning as they can be used for ddos attacks
		"""
		if variable is None:
			return ''
		variable = variable[0:min(len(variable), DataUtil.CHARACTER_LIMIT)]
		for ch in  ['\\','`','_',';']:
			variable = variable.replace(ch, '\\'+ch)
		return variable

	@staticmethod
	def clean_data(data):
		for (key, value) in data.items():
			data[key] = DataUtil.clean(value)
		return data


	@staticmethod
	def verify_message(message):
		return message
		result = {}
		triggered = False
		for (key, value) in message.items():
			if isinstance(value, dict):
				result[key] = DataUtil.verify_message(value)
			elif isinstance(value, str):
				if (len(value) > DataUtil.CHARACTER_LIMIT):
					result[key] = value[0:min(len(value), DataUtil.CHARACTER_LIMIT)]
					triggered = True
			elif isinstance(value, list):
				if (len(value) > DataUti.CHARACTER_LIMIT):
					result[key] = value[0:min(len(value), DataUtil.CHARACTER_LIMIT)]
					triggered = True
				
			else:
				result[key] = value
		if (triggered):
			Log.info("Exceptionally large Data - please check", str(json.dumps(result)))
		Log.info("Clean Response", json.dumps(result))
		return result
