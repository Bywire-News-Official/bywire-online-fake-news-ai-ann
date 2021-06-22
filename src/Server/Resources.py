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
from flask_restful import Resource
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
from flask import Response, request
import re
import codecs
import json
from Server.Analyzer import Analyzer
from Util.Const import Const
from Util.Config import Config
from Util.Log import Log
from datetime import datetime, timedelta
from Util.DataUtil import DataUtil
from Server.Parsers import analyze_text_parser, analyze_ipfs_parser, analyze_query_parser, analyze_flag_parser
from Server.Messages import Messages
from Database.Trust import Trust
from Database.TrustFlagged import TrustFlagged
from Database.Article import Article
from Database.Request import Request
global ipfs_server


class AnalyzeText(Resource):
	def post(self):
		data	= analyze_text_parser.parse_args()
		data	= DataUtil.clean_data(data)
		article = Article.fromJSON(data)
		found	= Article.get(article.id)
		if (found):
			del article
			return {"id": found.id, "new": True}, 200
		request = Request.fromJSON(article.toJSON())
		article.flush()
		request.flush()
		return {"id": request.id, "new": True}, 200

class AnalyzeIPFS(Resource):
	def post(self):
		data	= analyze_ipfs_parser.parse_args()
		data	= DataUtil.clean_data(data)
		Log.info(data)
		record	= {}
		id	     = Article.genID("", data["ipfs_hash"])
		if (Article.get(id)):
			return {"id": id, "new": True}, 200
		record["id"] = id
		request = Request.fromJSON(record)
		request.flush()
		return {"id": id, "new": True}, 200

class AnalyzeQuery(Resource):
	def post(self):
		data	= analyze_query_parser.parse_args()
		data	= DataUtil.clean_data(data)
		Log.info("AnalyzeQuery", data)
		id	= re.sub("\\\\", "", data["id"])
		Log.info("AnalyzeQuery", id)
		if (Request.get(id)):
			Log.info("AnalyzeQuery - Got Query")
			return {"id": id, "status": "Processing", "done": False}, 200
		trust	= Trust.get(id)
		if not(trust):
			Log.info("AnalyzeQuery - Got Trust")
			return {"id": id, "status": "Unknown Request", "done": True}, 200
		msg = {"id": id, "status": "Done", "done": True, "data": trust.toJSON()}
		for (key, value) in msg["data"].items():
			msg["data"][key] = int(value) if isinstance(value, float) else value
		flagged = TrustFlagged.get(id)
		msg["data"]["is_flagged"] = False
		if (flagged):
			if (flagged.reader_strength > 0):
				msg["data"]["is_flagged"] = True
				msg["data"]["reasons"].append("Was Flagged as Fake")
		if (id.startswith("IPFS_")):
			article = Article.get(id)
			msg["text"] = article.content
		Log.info("AnalyzeQuery - DONE", msg)
		return msg, 200

class AnalyzeFlag(Resource):
	def post(self):
		data	= analyze_flag_parser.parse_args()
		data	= DataUtil.clean_data(data)
		Log.info(data)
		data["strength"] = float(data["strength"])
		Log.info(data)
		if (data["strength"] < -100 or data["strength"] > 100):
			return {"status": "Error", "done": True, "error": True, "message": "Strength must lie between -100 to +100", "flagged": False}, 500
		id	= data["id"]
		trust	= TrustFlagged.get(id)
		if not(trust):
			trust = TrustFlagged.fromJSON({"id":		  id,
						       "is_fake":	  True,
						       "expert_vote":	  0,
						       "expert_strength": 0, 
						       "reader_vote":	  0,
						       "reader_strength": 0
			})
		if (data["is_expert"]):
			trust.expert_vote += 1
			trust.expert_strength = (data["strength"] + (trust.expert_vote-1)*trust.expert_strength)/max(1, trust.expert_vote)
		else:
			trust.reader_vote += 1
			trust.reader_strength = (data["strength"] + (trust.reader_vote-1)*trust.reader_strength)/max(1, trust.reader_vote)
		trust.flush()
		return {"status": "Done", "done": True, "flagged": True}, 200

class RecalculateParameters(Resource):
	def post(self):
		analyzer = Analyzer.get()
		analyzer.recalculate()
		return {}, 200

class CalibrateParameters(Resource):
	def post(self):
		analyzer = Analyzer.get()
		analyzer.calibrate()
		return {}, 200


class CleanParameters(Resource):
	def post(self):
		analyzer = Analyzer.get()
		analyzer.clean()
		return {}, 200



class BrewCoffee(Resource):
	def post(self):
		return Response("I'm a teapot", status=418, mimetype='application/coffee-pot-command')

			
