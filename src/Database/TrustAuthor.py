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

class TrustAuthor(MappedClass):
	class __mongometa__:
		session = Database.getInstance()
		name	= 'trust_author'
		indexes = [["author", "trust_version"]]

	_id			= FieldProperty(schema.ObjectId)
	
	author			= FieldProperty(schema.String(required=True))
	trust_version		= FieldProperty(schema.Int(required=True))
	timestamp		= FieldProperty(schema.Datetime)
	sentiment_score		= FieldProperty(schema.Float)
	title_score		= FieldProperty(schema.Float)
	author_score		= FieldProperty(schema.Float)
	worduse_score		= FieldProperty(schema.Float)
	comments_score		= FieldProperty(schema.Float)
	total_score		= FieldProperty(schema.Float)

	def toJSON(self):
		record = {"author":		  self.author,
			  "timestamp":		  self.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'), 
			  "trust_version":	  self.trust_version,
			  "sentiment_score":	  self.sentiment_score,
			  "title_score":	  self.title_score,
			  "author_score":	  self.author_score,
			  "worduse_score":	  self.worduse_score,
			  "total_score":	  self.total_score
			  }
		return record

	def __str__(self):
		return str(self.toJSON())
	
	@classmethod
	def fromJSON(self, record):
		return TrustAuthor(author	   = record["author"],
				   timestamp	  = record["timestamp"],
				   trust_version  = record["trust_version"],
				   sentiment_score= record["sentiment_score"],
				   title_score	  = record["title_score"],
				   author_score	  = record["author_score"],
				   worduse_score  = record["worduser_score"],
				   total_score	  = record["total_score"])



	@classmethod
	def getAuthor(cls, author):
		return cls.query.find({'author': author}).all()
	
	@classmethod
	def getAllAuthors(cls):
		return cls.query.find().all()

	@classmethod
	def update(cls, record):
		author		       = TrustAuthor.getAuthor(record['author'])
		if not(author):
			author = cls.fromJSON(record)
			author.flush()
			return
		author		       = author[0]
		author.timestamp       = record["timestamp"],
		author.trust_version   = record["trust_version"],
		author.sentiment_score = record["sentiment_score"],
		author.title_score     = record["title_score"],
		author.author_score    = record["author_score"],
		author.worduse_score   = record["worduser_score"],
		author.total_score     = record["total_score"])
		author.flush()




    
