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
import random, string

from Util.Log import Log
from Util.Const import Const
from Database.Database import Database


class User(MappedClass):
	class __mongometa__:
		session = Database.getInstance()
		name	= 'user'
		indexes = [["username"]]

	SALT_LEN       = 64
	ITERATIONS     = 100000
	ROLE_USER      = "user"
	ROLE_PARTNER   = "partner"
	ROLE_PUBLISHER = "publisher"
	ROLE_ISSUER    = "issuer"
	
		
	_id	    = FieldProperty(schema.ObjectId)
	username    = FieldProperty(schema.String(required=True))
	password    = FieldProperty(schema.String(required=True))
	parent	    = FieldProperty(schema.String(required=True))
	role	    = FieldProperty(schema.String)
	api_key	    = FieldProperty(schema.String)
	website_id  = FieldProperty(schema.String)
	email	    = FieldProperty(schema.String)
	timestamp   = FieldProperty(schema.String)
	url	    = FieldProperty(schema.String)
	
	def toJSON(self):
		record = {"username":		  self.username,
			  "password":		  self.password,
			  "parent":		  self.parent,
			  "api_key":		  self.api_key,
			  "role":		  self.role,
			  "website_id":		  self.website_id,
			  "email":		  self.email,
			  "url":		  self.url,
			  "timestamp":		  self.timestamp,			   
			  "encrypted":		  True
			  }
		return record

	@classmethod
	def fromJSON(cls, record):
		encrypted = record["encrypted"] if "encrypted" in record else False
		encrypt	  = lambda x: x if encrypted else cls.hash_create(x)
		timestamp = record["timestam"] if "timestamp" in record else datetime.now()
		timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S") if isinstance(timestamp, datetime) else timestamp
		api_key	  = encrypt(record["api_key"]) if ("api_key" in record and record["api_key"]) else ""
		website_id = record["website_id"] if "website_id" in record else ""
		return User(username	 = record["username"],
			    password	 = encrypt(record["password"]),
			    parent	 = record["parent"],
			    api_key	 = encrypt(api_key),
			    role	 = encrypt(record["role"]),
			    website_id	 = website_id,
			    email	 = record["email"],
			    timestamp	 = timestamp,
			    url		 = record["url"] if "url" in record else ""
			    )
	
	@classmethod
	def verify_secret(cls, secret, parent):
		parent_user = cls.get(parent)
		if not(parent_user):
			return False
		if not(cls.verify_role(parent_user.role, User.ROLE_PUBLISHER) or
		       cls.verify_role(parent_user.role, User.ROLE_ISSUER)):
			return False
		
		return cls.verify(parent_user.api_key, secret)
		
	@classmethod
	def verify_role(cls, stored_role, provided_role):
		return cls.verify(stored_role, provided_role)
		
	@classmethod
	def verify_password(cls, stored_password, provided_password):
		return cls.verify(stored_password, provided_password)
		
	@classmethod
	def verify(cls, stored, provided):
		"""Verify a stored password against one provided by user"""
		salt, stored_hashed = User.split_salt(stored)
		hashed		    = cls.hash_verify(provided, salt)
		return hashed == stored_hashed

	@classmethod
	def generateAPIKey(cls):
		return ''.join(random.choices(string.ascii_letters + string.digits, k=24))
	
	@staticmethod
	def split_salt(password):
		return (password[ :User.SALT_LEN], password[User.SALT_LEN: ])

	@staticmethod
	def hash_verify(password, salt):
		pwdhash = hashlib.pbkdf2_hmac('sha512',
					      password.encode('utf-8'), 
					      salt.encode('ascii'), 
					      User.ITERATIONS)
		return binascii.hexlify(pwdhash).decode('ascii')

	@classmethod
	def getAccountsForParent(cls, parent, page=0, nr_results=10):
		count = cls.query.find({"parent": parent}).count()
		data  = cls.query.find({"parent": parent}).skip(page*nr_results).limit(nr_results)
		data  = [{"username": item["username"], "timestamp": item["timestamp"] if "timestamp" in item else ""} for item in data]
		return {"count": count, "accounts": data}
	
	@staticmethod
	def hash_create(password):
		"""Hash a password for storing."""
		salt = hashlib.sha256(os.urandom(User.SALT_LEN)).hexdigest().encode('ascii')
		pwdhash = hashlib.pbkdf2_hmac('sha512',
					      password.encode('utf-8'), 
					      salt,
					      User.ITERATIONS)
		pwdhash = binascii.hexlify(pwdhash)
		return (salt[ :User.SALT_LEN] + pwdhash).decode('ascii') 
 
	def __str__(self):
		return str(self.toJSON())

	@classmethod
	def allowRex(cls, username):
		user = User.get(username)
		return (User.verify_role(user.role, User.ROLE_PUBLISHER) or
			User.verify_role(user.role, User.ROLE_ISSUER))

	@classmethod
	def get(cls, username):
		return cls.query.find({'username': username}).first()
		
	@classmethod
	def flush(cls):
		db = Database.getInstance()
		db.flush()




    
