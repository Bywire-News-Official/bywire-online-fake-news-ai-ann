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
from datetime import datetime
import json
import re

ALGO_VERSION = "0.1"
class Trust(MappedClass):
	""" Raw Features of an article """
	class __mongometa__:
		session = Database.getInstance()
		name = 'trust_{0:s}'.format(re.sub("[.]", "_", ALGO_VERSION))
		indexes = [["id", "param_version"]]

	_id			= FieldProperty(schema.ObjectId)
	
	id			= FieldProperty(schema.String(required=True))
	param_version		= FieldProperty(schema.Int)
	trust_score		= FieldProperty(schema.Float)
	divergency_score	= FieldProperty(schema.Float)
	sentiment_score		= FieldProperty(schema.Float)
	layout_score		= FieldProperty(schema.Float)
	complexity_score	= FieldProperty(schema.Float)
	platform_score		= FieldProperty(schema.Float)
	author_score		= FieldProperty(schema.Float)
	reasons			= FieldProperty(schema.String)

	def toJSON(self):
		record = {"id":			  self.id,
			  "param_version":	  self.param_version,
			  "trust_score":	  self.trust_score,
			  "sentiment_score":	  self.sentiment_score,
			  "divergency_score":	  self.divergency_score,
			  "layout_score":	  self.layout_score,
			  "complexity_score":	  self.complexity_score,
			  "platform_score":	  self.platform_score,
			  "author_score":	  self.author_score,
			  "reasons":		  json.loads(self.reasons),
			  }
		return record

	def __str__(self):
		return str(self.toJSON())
	
	@classmethod
	def fromJSON(self, record):
		get = lambda key: max(0, min(100, record[key])) if key in record else 101
		return Trust(id			   = record["id"],
			     param_version	   = record["param_version"],
			     trust_score	   = get("trust_score"),
			     sentiment_score	   = get("sentiment_score"),
			     divergency_score	   = get("divergency_score"),
			     layout_score	   = get("layout_score"),
			     complexity_score	   = get("complexity_score"),
			     platform_score	   = get("platform_score"),
			     author_score	   = get("author_score"),
			     reasons		   = json.dumps(record["reasons"])
		)


	@classmethod
	def clean(cls):
		version = TrustParameters.getVersion()
		cls.query.remove({"param_version": {"$lt": version}})
	
	@classmethod
	def get(cls, id):
		return cls.query.find({'id': id}).sort([["param_version", pymongo.DESCENDING]]).first()

	@classmethod
	def flush(cls):
		Database.flush()




    
