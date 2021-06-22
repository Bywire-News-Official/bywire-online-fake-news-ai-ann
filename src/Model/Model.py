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
import json
import math

from datetime import datetime, timedelta
from Util.Const import Const
from Util.Config import Config
from Util.Log import Log

from Database.Trust	      import Trust
from Database.TrustFlagged    import TrustFlagged
from Database.TrustArticle    import TrustArticle
from Database.TrustParameters import TrustParameters
from Model.ModelConst import ModelConst

class Model(object):
	VERSION = "0.1"
	""" Model: Virtual Base class for models
	"""
	def __init__(self, config):
		super(Model, self).__init__()
		self.m_config		      = config
		self.m_param_version	      = TrustParameters.getVersion()
		#print(TrustParameters.get(self.m_param_version))
		self.m_parameters	      = dict([(item["platform"], item) for item in TrustParameters.get(self.m_param_version)])
		#print(self.m_parameters)
		Model.VERSION		      = config[ModelConst.VERSION]
		print(Model.VERSION)
		base_path	  = config[ModelConst.BASE_PATH]
		self.m_model_path = os.path.join(base_path, "model_{0:s}.json".format(Model.VERSION))
		self.m_coeff_path = os.path.join(base_path, "coeff_{0:s}.h5".format(Model.VERSION))

	def flagged(self, id):
		flag = TrustFlagged.get(id)
		if not(flag):
			return 0
		return 2*flag.reader.strength/200 + 1

		
	def features(self, trust_article):
		
		platform	       = trust_article.platform if trust_article.platform in self.m_parameters else ModelConst.PLATFORM_ALL
		parameters	       = self.m_parameters[platform]
		a1  = parameters["sentiment_score"]["ci50"]
		b1  = parameters["sentiment_score"]["scale"]
		sentiment1 = (trust_article.sentiment_score - a1)/b1

		a1  = parameters["sentiment_score2"]["ci90"]
		b1  = parameters["sentiment_score2"]["scale"]
		sentiment2 = (trust_article.sentiment_score2 - a1)/b1
		
		a1  = parameters["sentiment_expertai_positive"]["ci50"]
		c1  = parameters["sentiment_expertai_positive"]["ci90"]
		b1  = c1 - a1
		euphoria_pos = (trust_article.sentiment_expertai_positive - a1)/b1

		a1  = parameters["sentiment_expertai_negative"]["ci50"]
		c1  = parameters["sentiment_expertai_negative"]["ci90"]
		b1  = c1 - a1
		euphoria_neg = (trust_article.sentiment_expertai_negative - a1)/b1
		
		euphoria     = max(euphoria_pos, euphoria_neg)
		

		a1  = parameters["article_length"]["ci10"]
		b1  = parameters["article_length"]["scale"]
		article_length = (a1 - trust_article.article_length)/b1

		a1 = parameters["complexity_punctuation"]["ci10"]
		a2 = parameters["complexity_punctuation"]["ci90"]
		punctuation = 1 if (trust_article.complexity_punctuation < a1 or
				    trust_article.complexity_punctuation > a2) else 0


		a1  = parameters["complexity_complexity"]["ci10"]
		complexity = 1 if (trust_article.complexity_complexity	< a1) else 0
		
		a1  = parameters["complexity_duplication"]["ci10"]
		duplication = 1 if (trust_article.complexity_duplication < a1) else 0
		
		a1  = parameters["complexity_word_length"]["ci10"]
		word_length = 1 if (trust_article.complexity_word_length < a1) else 0


		b1 = parameters["sentiment_expertai_positive"]["ci90"]
		b2 = parameters["sentiment_positive"]["ci90"]
		divergency_pos = abs(trust_article.sentiment_expertai_positive/b1 - trust_article.sentiment_positive/b2)
		
		b1 = parameters["sentiment_expertai_negative"]["ci90"]
		b2 = parameters["sentiment_negative"]["ci90"]
		divergency_neg = abs(trust_article.sentiment_expertai_negative/b1 - trust_article.sentiment_negative/b2)

		b1 = parameters["complexity_expertai"]["ci90"]
		b2 = parameters["complexity_complexity"]["ci90"]
		divergency_com = abs(trust_article.complexity_expertai/b1 - trust_article.complexity_complexity/b2)

		divergency = max(divergency_pos, divergency_pos, divergency_com)
		baserate   = parameters["baserate"]
			
		norm = lambda x: max(0, min(1, x))
		record = {"sentiment":		    norm(sentiment1),
			  "sentiment2":		    norm(sentiment2),
			  "euphoria":		    norm(euphoria),
			  "article_length":	    norm(article_length),
			  "punctuation":	    punctuation,
			  "complexity_complexity":  complexity,
			  "complexity_duplication": duplication,
			  "complexity_word_length": word_length,
			  "platform":		    1-baserate,
			  "divergency":		    norm(divergency),
			  "author":		    0
			  }
		return record		     


	def reasons(self, features):
		reasons		       = []
		if (features["euphoria"] > 0.5):
			  reasons.append("The tone is euphoric/depressed")
		if (features["punctuation"] > 0.5):
			  reasons.append("Suspicious Puntuation")
		if (features["sentiment"] > 0.5):
			  reasons.append("Suspicious Emotional Response")
		if (features["article_length"] > 0.5):
			  reasons.append("Article is shorter than expected")
		if (features["complexity_word_length"] > 0.5):
			  reasons.append("Simlistic Word Use")
		if (features["complexity_duplication"] > 0.5):
			  reasons.append("Repetitive Word Use")
		if (features["complexity_complexity"] > 0.5):
			  reasons.append("Suspicious Word Use")
		if (features["divergency"] > 0.5):
			  reasons.append("Suspicious Incompatability between algorithms")
		return reasons
			  
	def score(self, trust_article):
		if not(self.m_parameters):
			return
		platform	       = trust_article.platform if trust_article.platform in self.m_parameters else ModelConst.PLATFORM_ALL
		parameters	       = self.m_parameters[platform]
		features	       = self.features(trust_article)
		trust		       = self.predict(features)
		trust["id"]	       = trust_article.id
		trust["param_version"] = self.m_param_version
		trust["reasons"]       = self.reasons(features)

		trust = Trust.fromJSON(trust)
		trust.flush()
		return trust
		
	def predict(self, features):
		assert False, "Model.predict - Model is a virtual base class"
				
	def train(self):
		assert False, "Model.predict - Model is a virtual base class"
		
	def save(self):
		assert False, "Model.predict - Model is a virtual base class"
				
	def load(self):
		assert False, "Model.predict - Model is a virtual base class"
				
