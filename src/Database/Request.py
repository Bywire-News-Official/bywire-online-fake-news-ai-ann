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

from ming import schema
from ming.odm import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty
from Database.Database import Database
import pymongo
import hashlib
from collections import deque
from datetime import datetime
import json
import re

class Request(MappedClass):
	class __mongometa__:
		session = Database.getInstance()
		name	= 'request'
		indexes = [["id"], ["processing", "timestamp"]]

	_id			= FieldProperty(schema.ObjectId)
	
	id			= FieldProperty(schema.String(required=True))
	timestamp		= FieldProperty(schema.DateTime)
	processing		= FieldProperty(schema.Bool)

	def toJSON(self):
		record = {"id":			  self.id,
			  "timestamp":		  self.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
			  "processing":		  self.processing
			  }
		return record

	def __str__(self):
		return str(self.toJSON())
	
	@classmethod
	def fromJSON(cls, record):
		timestamp = record["timestamp"] if "timestamp" in record else datetime.now()
		if isinstance(timestamp, str):
			timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
		record["processing"] = record["processing"] if "processing" in record else False
		return Request(	 id	   = record["id"],
				 timestamp   = timestamp,
				 processing  = record["processing"]
			       )

	def fromIPFS(self):
		return self.id.startswith("IPFS_")

	@classmethod
	def getQueue(cls):
		return deque([item for item in cls.query.find({'processing': False}).sort([["timestamp",  pymongo.ASCENDING]]).limit(100)])


	@classmethod
	def get(cls, id):
		return cls.query.find({"id": id}).first()

	def remove(self):
		cls.query.remove({"id": self.id})
		self.flush()
	

	@classmethod
	def flush(cls):
		db = Database.getInstance()
		db.flush()

