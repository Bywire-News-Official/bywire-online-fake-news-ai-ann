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

class TrustArticle(MappedClass):
	""" Core Features of an article """
	class __mongometa__:
		session = Database.getInstance()
		name = 'trust_articles'
		indexes = [["id"], ["sentiment_score", "platform", "publisher"], ["complexity_score", "platform", "publisher"], ["capital_score", "platform", "publisher"], ["article_length", "platform", "publisher"], ["complexity_duplication", "platform", "publisher"], ["complexity_punctuation", "platform", "publisher"], ["complexity_complexity", "platform", "publisher"]]

	_id			= FieldProperty(schema.ObjectId)
	
	id				= FieldProperty(schema.String(required=True))
	platform			= FieldProperty(schema.String)
	publisher			= FieldProperty(schema.String)
	sentiment			= FieldProperty(schema.Float)
	sentiment_anger			= FieldProperty(schema.Float)
	sentiment_fear			= FieldProperty(schema.Float)
	sentiment_anticip		= FieldProperty(schema.Float)
	sentiment_trust			= FieldProperty(schema.Float)
	sentiment_surprise		= FieldProperty(schema.Float)
	sentiment_sadness		= FieldProperty(schema.Float)
	sentiment_disgust		= FieldProperty(schema.Float)
	sentiment_joy			= FieldProperty(schema.Float)
	sentiment_positive		= FieldProperty(schema.Float)
	sentiment_negative		= FieldProperty(schema.Float)
	sentiment_expertai_positive	= FieldProperty(schema.Float)
	sentiment_expertai_negative	= FieldProperty(schema.Float)
	complexity_expertai		= FieldProperty(schema.Float)
	sentiment_score			= FieldProperty(schema.Float)
	sentiment_score2		= FieldProperty(schema.Float)
	complexity_word_length		= FieldProperty(schema.Float)
	complexity_clean_length		= FieldProperty(schema.Float)
	complexity_punctuation		= FieldProperty(schema.Float)
	complexity_complexity		= FieldProperty(schema.Float)
	complexity_duplication		= FieldProperty(schema.Float)
	complexity_score		= FieldProperty(schema.Float)
	capital_score			= FieldProperty(schema.Float)
	article_length			= FieldProperty(schema.Int)
	
	def toJSON(self):
		record = {"id":				    self.id,
			  "platform":			    self.platform,
			  "publisher":			    self.publisher,
			  "sentiment":			    self.sentiment,
			  "sentiment_anger":		    self.sentiment_anger,
			  "sentiment_fear":		    self.sentiment_fear,
			  "sentiment_anticip":		    self.sentiment_anticip,
			  "sentiment_trust":		    self.sentiment_trust,
			  "sentiment_surprise":		    self.sentiment_surprise,
			  "sentiment_sadness":		    self.sentiment_sadness,
			  "sentiment_disgust":		    self.sentiment_disgust,
			  "sentiment_joy":		    self.sentiment_joy,
			  "sentiment_positive":		    self.sentiment_positive,
			  "sentiment_negative":		    self.sentiment_negative,
			  "sentiment_expertai_positive":    self.sentiment_positive,
			  "sentiment_expertai_negative":    self.sentiment_negative,
			  "complexity_expertai":	    self.sentiment_negative,
			  "sentiment_score":		    self.sentiment_score,
			  "sentiment_score2":		    self.sentiment_score2,
			  "complexity_word_length":	    self.complexity_word_length,
			  "complexity_clean_length":	    self.complexity_clean_length,
			  "complexity_punctuation":	    self.complexity_punctuation,
			  "complexity_complexity":	    self.complexity_complexity,
			  "complexity_duplication":	    self.complexity_duplication,
			  "complexity_score":		    self.complexity_score,
			  "capital_score":		    self.capital_score,
			  "article_length":		    self.article_length
			  }
		return record

	def __str__(self):
		return str(self.toJSON())
	
	@classmethod
	def fromJSON(self, record):
		get = lambda key: record[key] if key in record else 0.0
		return TrustArticle(id			   = record["id"],
				    platform		   = record["platform"],
				    publisher		   = record["publisher"],
				    sentiment		   = get("sentiment"),
				    sentiment_anger	   = get("sentiment_anger"),
				    sentiment_fear	   = get("sentiment_fear"),
				    sentiment_anticip	   = get("sentiment_anticip"),
				    sentiment_trust	   = get("sentiment_trust"),
				    sentiment_surprise	   = get("sentiment_surprise"),
				    sentiment_sadness	   = get("sentiment_sadness"),
				    sentiment_disgust	   = get("sentiment_disgust"),
				    sentiment_joy	   = get("sentiment_joy"),
				    sentiment_positive	   = get("sentiment_positive"),
				    sentiment_negative	   = get("sentiment_negative"),
				    sentiment_expertai_positive	= get("sentiment_positive"),
				    sentiment_expertai_negative	= get("sentiment_negative"),
				    complexity_expertai	   = get("sentiment_negative"),
				    sentiment_score	   = get("sentiment_score"),
				    sentiment_score2	   = get("sentiment_score2"),
				    complexity_word_length = get("complexity_word_length"),
				    complexity_clean_length= get("complexity_clean_length"),
				    complexity_punctuation = get("complexity_punctuation"),
				    complexity_complexity  = get("complexity_complexity"),
				    complexity_duplication = get("complexity_duplication"),
				    complexity_score	   = get("complexity_score"),
				    capital_score	   = get("capital_score"),
				    article_length	   = get("article_length")
				    )

	@classmethod
	def ci(cls, factor, filter={}):
		values = [item.toJSON()[factor] for item in cls.query.find(filter).sort([[factor, pymongo.ASCENDING]])]
		result = {"min": values[0],
			  "ci10": values[int(0.1*len(values))],
			  "ci50": values[int(0.5*len(values))],
			  "ci90": values[int(0.9*len(values))],
			  "mean": sum(values)/max(1, len(values)),
			  "max":  values[len(values)-1]


			  }
		del values
		print(factor, result)
		return result

	@classmethod
	def clean(cls):
		cls.query.remove({})
	
	@classmethod
	def get(cls, id):
		return cls.query.find({'id': id}).all()

	@classmethod
	def flush(cls):
		Database.flush()




    
