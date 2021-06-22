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

class TrustParameters(MappedClass):
	""" Maps Features of an article to the range [0-1] to allow better learning """
	class __mongometa__:
		session = Database.getInstance()
		name = 'trust_parameters'
		indexes = [["version"]]

	_id			= FieldProperty(schema.ObjectId)
	
	version				= FieldProperty(schema.Int)
	platform			= FieldProperty(schema.String)
	publisher			= FieldProperty(schema.String)
	sentiment_score			= FieldProperty(schema.String)
	sentiment_score2		= FieldProperty(schema.String)
	sentiment_positive		= FieldProperty(schema.String)
	sentiment_negative		= FieldProperty(schema.String)
	sentiment_expertai_positive	= FieldProperty(schema.String)
	sentiment_expertai_negative	= FieldProperty(schema.String)
	article_length			= FieldProperty(schema.String)
	complexity_punctuation		= FieldProperty(schema.String)
	complexity_word_length		= FieldProperty(schema.String)
	complexity_duplication		= FieldProperty(schema.String)
	complexity_complexity		= FieldProperty(schema.String)
	complexity_expertai		= FieldProperty(schema.String)
	baserate			= FieldProperty(schema.Float)


	def toJSON(self):
		record = {"version":			    self.version,
			  "platform":			    self.platform,
			  "publisher":			    self.publisher,
			  "sentiment_score":		    json.loads(self.sentiment_score),
			  "sentiment_score2":		    json.loads(self.sentiment_score2),
			  "sentiment_positive":		    json.loads(self.sentiment_positive),
			  "sentiment_negative":		    json.loads(self.sentiment_negative),
			  "sentiment_expertai_positive":    json.loads(self.sentiment_expertai_positive),
			  "sentiment_expertai_negative":    json.loads(self.sentiment_expertai_negative),
			  "article_length":		    json.loads(self.article_length),
			  "complexity_punctuation":	    json.loads(self.complexity_punctuation),
			  "complexity_word_length":	    json.loads(self.complexity_word_length),
			  "complexity_duplication":	    json.loads(self.complexity_duplication),
			  "complexity_complexity":	    json.loads(self.complexity_complexity),
			  "complexity_expertai":	    json.loads(self.complexity_expertai),
			  "baserate":			    self.baserate
			  
		}
		return record

	def __str__(self):
		return str(self.toJSON())
	
	@classmethod
	def fromJSON(self, record):
		return TrustParameters(version			   = record["version"],
				       platform			   = record["platform"],
				       publisher		   = record["publisher"],
				       sentiment_score		   = json.dumps(record["sentiment_score"]),
				       sentiment_score2		   = json.dumps(record["sentiment_score2"]),
				       sentiment_positive	   = json.dumps(record["sentiment_positive"]),
				       sentiment_negative	   = json.dumps(record["sentiment_negative"]),
				       sentiment_expertai_positive = json.dumps(record["sentiment_expertai_positive"]),
				       sentiment_expertai_negative = json.dumps(record["sentiment_expertai_negative"]),
				       article_length	      = json.dumps(record["article_length"]),
				       complexity_punctuation = json.dumps(record["complexity_punctuation"]),
				       complexity_word_length = json.dumps(record["complexity_word_length"]),
				       complexity_duplication = json.dumps(record["complexity_duplication"]),
				       complexity_complexity  = json.dumps(record["complexity_complexity"]),
				       complexity_expertai    = json.dumps(record["complexity_expertai"]),

				       baserate		      = record["baserate"]
				    )

	@classmethod
	def clean(cls):
		version = cls.getVersion()
		cls.query.remove({"version": {"$lt": version}})
		
	@classmethod
	def getVersion(cls):
		record = cls.query.find().sort([["version", pymongo.DESCENDING]]).first()
		return record["version"] if record else 0
		
	
	@classmethod
	def get(cls, version):
		return [item.toJSON() for item in  cls.query.find({"version": version}).all()]
	
	@classmethod
	def flush(cls):
		Database.flush()




    
