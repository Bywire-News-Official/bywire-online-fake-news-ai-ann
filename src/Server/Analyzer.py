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
import re
import time
import glob
import dateutil.parser
import codecs
import json
import threading
import hashlib
from collections import deque
from datetime import datetime, timedelta
import argparse
import math
import traceback

from nrclex import NRCLex
from nltk import corpus, tokenize, stem
from IPFS.ipfs import IPFSGateway
from Util.Const import Const
from Util.Config import Config
from Util.Log import Log
from Database.Article import Article
from Database.Request import Request
from Database.Trust	      import Trust
from Database.TrustArticle    import TrustArticle
from Database.TrustParameters import TrustParameters
from Database.Database import Database
from IPFS.ipfs import IPFSGateway

from Model.ModelFactory import ModelFactory
from Model.ModelConst import ModelConst
# Import according to the docs didn't work with the standard ubuntu installation.
from expertai.nlapi.cloud.client import ExpertAiClient
from expertai.nlapi.common.errors import ExpertAiRequestError as ExpertAiRequestError

class Analyzer(threading.Thread):
	""" Analyzer: Core class to calculate trust scores 
	"""
	INSTANCE = None
	def __init__(self, config):
		super(Analyzer, self).__init__()
		self.m_config		      = config
		self.m_ipfs_gateway	      = IPFSGateway(config)
		self.m_run		      = False
		self.m_queue		      = deque()
		self.m_model		      = ModelFactory.build(config)
		self.m_model.load()
		self.m_nlp_client	      = None
		if config[Const.EXPERTAI_USE].lower() == "true":
			os.environ["EAI_USERNAME"] = config[Const.EXPERTAI_USERNAME]
			os.environ["EAI_PASSWORD"] = config[Const.EXPERTAI_PASSWORD]
			self.m_nlp_client = ExpertAiClient()
			

		
	@classmethod
	def get(cls, config=None):
		print(cls.INSTANCE)
		if not(cls.INSTANCE):
			cls.INSTANCE		      = Analyzer(config)
		return cls.INSTANCE
				
	def run(self):
		while self.m_run:
			queue = Request.getQueue()
			for request in queue:
				request.processing = True
				article = Article.get(request.id)
				if not(article):
					if (request.fromIPFS()):
						self.download(request)
					else:
						Log.error("ERROR *** Article not found")
				else:
					result = self.analyze(article)
				request.delete()
				Request.flush()
			time.sleep(1)

	def send_to_api(self, text, language, resource):
		try:
			document = self.m_nlp_client.specific_resource_analysis(
				body={"document": {"text": text}}, 
				params={'language': language, 'resource': resource})

		except ExpertAiRequestError as e:
			if e.text.startswith("Failed to fetch the Bearer Token"):
				print("Invalid ExpertAi password. Please reconfigure Config/Config.xml")
				exit(0)
			else:
				raise
		return document
			

	def enrich(self, text):
		if not(self.m_nlp_client):
			return {"sentiment_expertai_positive":	 -1.0,
				  "sentiment_expertai_negative": -1.0,
				  "complexity_expertai":	 -1.0}
		sentiment_output   = self.send_to_api(text, 'en', 'sentiment')
		#complexity_output  = self.send_to_api(text, 'en', 'deep-linguistic-analysis')
		#print(complexity_output)
		try:
			Log.info(dir(sentiment_output))
			Log.info(dir(sentiment_output.sentiment))
			Log.info(sentiment_output.sentiment)
			record = {"sentiment_expertai_positive": sentiment_output.sentiment.positivity,
				  "sentiment_expertai_negative": sentiment_output.sentiment.negativity,
				  "complexity_expertai": 0.0}
		except AttributeError as e:
			traceback.print_tb()
		return record
			
		
	def complexity(self, text):
		tokens = tokenize.word_tokenize(text)
		tokens = [token.lower() for token in tokens if not(token in (".", ","))]
		tokens = [token for token in tokens if not token in corpus.stopwords.words("english")]
		clean_length  = max(1, len(" ".join(tokens)))
		word_length   = clean_length/max(1, len(tokens))
		punctuation   = len(text)/clean_length
		ps	      = stem.PorterStemmer()
		stemmed	      = set([ps.stem(token) for token in tokens])
		complexity    = len(" ".join(stemmed))/clean_length
		duplication   = len(tokens)/max(1, len(stemmed))
		return {"complexity_word_length":	word_length,
			"complexity_clean_length":	clean_length,
			"complexity_punctuation":	punctuation,
			"complexity_complexity":	complexity,
			"complexity_duplication":	duplication,
			"complexity_score":		-1*(word_length + complexity - duplication)
			}
			
	def analyze(self, article):
		text_object		     = NRCLex(article.content)
		sentiment		     = text_object.affect_frequencies
		complexity		     = self.complexity(article.content)
		enriched		     = self.enrich(article.content)
		record			     = {}
		record["id"]		     = article.id
		record["publisher"]	     = article.publisher
		record["platform"]	     = article.platform
		for (key, value) in sentiment.items():
			record["sentiment_{0:s}".format(key)] = value
		for (key, value) in complexity.items():
			record[key] = value
		for (key, value) in enriched.items():
			record[key] = value
		record["sentiment"]	     = sentiment["positive"] - sentiment["negative"]
		record["sentiment_score"]    = sentiment["anger"]  - sentiment["sadness"]
		record["sentiment_score2"]   = sentiment["anger"] + sentiment["fear"]  - 2*sentiment["sadness"] - sentiment["trust"]
		record["capital_score"]	     = sum(1 for letter in article.content if letter.isupper())/max(1, len(article.content))
		record["article_length"]     = len(article.content)
		trust			     = TrustArticle.fromJSON(record)
		self.m_model.score(trust)
		return True

	def clean(self):
		""" Frees up space from old algorithms
		"""
		Trust.clean()

	def calibrate(self):
		Article.requeue()
		
		version		= TrustParameters.getVersion()+1
		factors		= ["sentiment_score", "sentiment_score2", "sentiment_positive", "sentiment_negative", "article_length", "complexity_punctuation", "complexity_word_length", "complexity_complexity", "complexity_duplication", "sentiment_expertai_positive", "sentiment_expertai_negative", "complexity_expertai"]

		record = {"version": version,
			  "platform":  ModelConst.PLATFORM_ALL,
			  "publisher": ""}
		for factor in factors:
			ci = TrustArticle.ci(factor)
			ci["scale"] = (ci["ci90"] - ci["ci10"])
			record[factor] = ci
		record["baserate"] = 1
		parameters = TrustParameters.fromJSON(record)
		parameters.flush()
		self.m_model.train()
		self.m_model.save()
		for (i, item) in enumerate(Article.all()):
			trust = TrustArticle.get(item["id"])
			self.m_model.score(trust)
			if (i % 1000 == 0):
				print(i)
		
	def recalculate(self):
		TrustArticle.clean()
		Article.requeue()


	def parse_document(self, id, data):
		Log.info("ParseDocument", id, data, type(data))
		record = {}
		record["id"]	     = id
		try:
			if (isinstance(data, str)):
				data = json.loads(data)				       
			record["content"]    = data["content"]
			record["title"]	     = data["title"]
			record["author"]     = data["author"]
			record["publisher"]  = data["publisher"]
			record["platform"]   = "IPFS"
			
			      
		except (KeyError, ) as e:
			record["content"]    = str(data)
			record["title"]	     = ""
			record["author"]     = ""
			record["publisher"]  = ""
			record["platform"]   = "IPFS"
		Log.info("ParseDocument", id, record)
		article = Article.fromJSON(record)
		article.flush()
		self.analyze(article)
		Log.info("ParseDocument - Analysis Done", id, record)
		request = Request.get(id)
		request.delete()
		
		
	def download(self, request):
		ipfs_hash = re.sub("IPFS_", "", request.id)
		self.m_ipfs_gateway.retrieveDocumentFromHash(ipfs_hash, lambda x: self.parse_document(request.id, x))
	
	def start(self):
		if (self.m_run):
			return
		self.m_run = True
		super(Analyzer, self).start()

	def stop(self):
		self.m_run = False


if __name__=='__main__':
	os.environ['FLASK_ENV'] = 'development'

	with Config(Const.CONFIG_PATH) as config:
		log = Log(config)
		analyzer = Analyzer(config)
		analyzer.start()
		analyzer.join()
		analyzer.stop()
				


