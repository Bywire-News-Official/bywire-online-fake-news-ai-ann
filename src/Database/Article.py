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
from Database.Request import Request
import pymongo
import hashlib
from datetime import datetime
import json
import re

class Article(MappedClass):
	class __mongometa__:
		session = Database.getInstance()
		name	= 'articles'
		indexes = [["id"], ["publisher", "id"], ["author", "id"]]

	_id			    = FieldProperty(schema.ObjectId)
	
	id			= FieldProperty(schema.String(required=True))
	author			= FieldProperty(schema.String)
	publisher		= FieldProperty(schema.String)
	platform		= FieldProperty(schema.String)
	title			= FieldProperty(schema.String)
	content			= FieldProperty(schema.String(required=True))
	content_hash		= FieldProperty(schema.String)
	timestamp		= FieldProperty(schema.DateTime)

	@classmethod
	def fromIPFS(cls):
		return id.startswith("IPFS_")
	
	def toJSON(self):
		record = {"id":			  self.id,
			  "author":		  self.author,
			  "publisher":		  self.publisher,
			  "platform":		  self.platform,
			  "title":		  self.title,
			  "content":		  self.content,
			  "content_hash":	  self.content_hash,
			  "timestamp":		  self.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
		}
		return record

	def __str__(self):
		return str(self.toJSON())


	@classmethod
	def all(cls):
		#Alternative implementation as ming is very slow to loop over a collection
		client	     = pymongo.MongoClient("mongodb://localhost:27017/")
		db	     = client["bywire_trust"]
		articles     = db["articles"]		     
		for item in articles.find().sort([["id", pymongo.ASCENDING]]):
			yield item
			
	@classmethod
	def new_requests(cls):
		#Alternative implementation as ming is very slow to loop over a collection
		client	     = pymongo.MongoClient("mongodb://localhost:27017/")
		db	     = client["bywire_trust"]
		#db	     = client[Database.__INSTANCE.m_schema]
		trust	     = db["trust_articles"]		     
		request	     = db["request"]		     
		articles     = db["articles"]		     
		for item in articles.find().sort([["id", pymongo.ASCENDING]]):
			if (trust.find({"id": item["id"]}).count()>0):
				continue
			yield item
			
	@classmethod
	def requeue(cls):
		#Alternative implementation as ming is very slow to loop over a collection
		client	     = pymongo.MongoClient("mongodb://localhost:27017/")
		db	     = client["bywire_trust"]
		trust	     = db["trust_articles"]		     
		request	     = db["request"]		     
		articles     = db["articles"]		     
		for (i, item) in enumerate(articles.find().sort([["id", pymongo.ASCENDING]])):
			if (request.find({"id": item["id"]}).count() > 0):
				continue
			if (trust.find({"id": item["id"]}).count()>0):
				continue
			new_request = Request.fromJSON({"id": item["id"]})
			new_request.flush()
			if (i % 1000 == 0):
				print(i)
		print("Requeue Done")
			
	"""
	@classmethod
	def requeue(cls):
		for item in cls.query.find({}).all():
			request = Request.fromJSON(item.toJSON())
			request.flush()
	
	"""
	
	@staticmethod
	def genID(content_hash, ipfs_hash):
		return content_hash if not(ipfs_hash) else "IPFS_"+ipfs_hash

	@classmethod
	def fromJSON(self, record):
		Log.info("Article.fromJSON", record)
		record["timestamp"] = record["timestamp"]  if "timestamp" in record else datetime.now()
		timestamp = record["timestamp"]
		
		if isinstance(timestamp, str):
			timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
		if not("content_hash" in record):
			record["content_hash"] = Article.contentHash(record)
		if not("ipfs_hash" in record):
			record["ipfs_hash"] = ""
		if not("id" in record):
			record["id"] = Article.genID(record["content_hash"], record["ipfs_hash"])
		return Article(id	     = record["id"],
			       author	     = record["author"],
			       publisher     = record["publisher"],
			       platform	     = record["platform"],
			       title	     = record["title"],
			       content	     = record["content"],
			       content_hash  = record["content_hash"],
			       timestamp     = record["timestamp"]
		)

	@staticmethod
	def contentHash(record):
		content = record["title"]+record["author"]+record["content"]
		return str(hashlib.sha512(bytes(content, 'utf-8')).hexdigest().encode('ascii'))

	@classmethod
	def get(cls, id):
		return cls.query.find({'id': id}).first()

	@classmethod
	def fromMessage(cls, message):
		data	 = message
		timestamp=datetime.now()
		record = {"id":		     data[Const.REQ_ARTICLE],
			  "author":	     data[Const.REQ_ARTICLE_AUTHOR],
			  "platform":	     data["platform"],
			  "publisher":	     data["publisher"],
			  "title":	     data[Const.REQ_ARTICLE_TITLE],
			  "content":	     data[Const.REQ_ARTICLE_CONTENT],
			  "timestamp":	     timestamp
		}
		article = cls.fromJSON(record)
		return article

	@classmethod
	def flush(cls):
		db = Database.getInstance()
		db.flush()




    
