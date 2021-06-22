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

from ming import schema
from ming.odm import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty
from Database.Database import Database
import pymongo
from datetime import datetime
import json
import re

class Transaction(MappedClass):
	class __mongometa__:
		session = Database.getInstance()
		name	= 'transaction'
		indexes = [("wallet", "timestamp")]

	_id			= FieldProperty(schema.ObjectId)
	request_id		= FieldProperty(schema.String)
	transactionID		= FieldProperty(schema.String)
	currency		= FieldProperty(schema.String)
	timestamp		= FieldProperty(schema.DateTime)
	date			= FieldProperty(schema.String)
	article			= FieldProperty(schema.String)
	action			= FieldProperty(schema.String)
	wallet			= FieldProperty(schema.String)
	amount			= FieldProperty(schema.Float)
	data			= FieldProperty(schema.String)


	def __str__(self):
		return str(self.toJSON())
	
	
	def toJSON(self):
		record = {"transactionID":	   self.transactionID,
			  "currency":		   self.currency,
			  "timestamp":		   self.timestamp,
			  "date":		   self.date,
			  "article":		   self.article,
			  "action":		   self.action,
			  "wallet":		   self.wallet,
			  "amount":		   self.amount,
			  "data":		   json.loads(self.data)}
		return record

	@classmethod
	def fromJSON(cls, record):
		return Transaction(
			transactionID		= record["transactionID"],
			currency		= record["currency"],
			timestamp		= record["timestamp"],
			date			= record["timestamp"].strftime("%Y%m%d"),
			article			= record["article"],
			action			= record["action"],
			wallet			= record["wallet"],
			amount			= record["amount"],
			data			= json.dumps(record["data"]))


	@classmethod
	def getAll(cls):
		return cls.query.find().all()
 
	@classmethod
	def getForRequestAll(cls, request):
		return cls.query.find({"request_id": request.id}).all()
 
	@classmethod
	def getAllForWallet(cls, wallet):
		return cls.query.find({'wallet': wallet}).sort([['timestamp', pymongo.ASCENDING]]).all()
 
	@classmethod
	def getAllForDate(cls, date):
		return cls.query.find({"date": date}).sort([['timestamp', pymongo.ASCENDING]]).all()


	@classmethod
	def flush(cls):
		db = Database.getInstance()
		db.flush()


