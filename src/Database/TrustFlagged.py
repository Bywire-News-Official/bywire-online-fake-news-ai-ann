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

class TrustFlagged(MappedClass):
	""" Raw Features of an article """
	class __mongometa__:
		session = Database.getInstance()
		name = 'trust_flagged'
		indexes = [["id"]]

	_id			= FieldProperty(schema.ObjectId)
	
	id			= FieldProperty(schema.String(required=True))
	is_fake			= FieldProperty(schema.Bool)
	expert_vote		= FieldProperty(schema.Int)
	expert_strength		= FieldProperty(schema.Float)
	reader_vote		= FieldProperty(schema.Int)
	reader_strength		= FieldProperty(schema.Float)

	def toJSON(self):
		record = {"id":			  self.id,
			  "is_fake":		  self.is_fake,
			  "expert_vote":	  self.expert_vote,
			  "expert_strength":	  self.expert_strength,
			  "reader_vote":	  self.reader_vote,
			  "reader_strength":	  self.reader_strength
			  }
		return record

	def __str__(self):
		return str(self.toJSON())
	
	@classmethod
	def fromJSON(self, record):
		return TrustFlagged(id			   = record["id"],
				    is_fake		   = record["is_fake"],
				    expert_vote		   = record["expert_vote"],
				    expert_strength	   = record["expert_strength"],
				    reader_vote		   = record["reader_vote"],
				    reader_strength	   = record["reader_strength"]
				    )

	@classmethod
	def get(cls, id):
		Log.info("TrustFlagged - get", id)
		result = cls.query.find({'id': id}).first()
		Log.info("TrustFlagged - get", result)
		return result

	@classmethod
	def flush(cls):
		Database.flush()




    
