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

from ming import schema
from ming.odm import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty
import pymongo
import hashlib
from datetime import datetime
import json
import re
import hashlib, binascii

from Util.Log import Log
from Util.Const import Const
from Database.Database import Database


class RevokedToken(MappedClass):
	class __mongometa__:
		session = Database.getInstance()
		name	= 'revoked_token'
		indexes = [["jti"]]

	_id	    = FieldProperty(schema.ObjectId)
	jti	    = FieldProperty(schema.String(required=True))
	
	def toJSON(self):
		record = {"jti":		  self.jti
			  }
		return record

	@classmethod
	def fromJSON(self, record):
		return RevokedToken(jti	 = record["jti"])

	@classmethod
	def flush(cls):
		db = Database.getInstance()
		db.flush()




    
