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
from datetime import datetime, timedelta
from Util.Const import Const
from Util.Config import Config
from Util.Log import Log

from Model.ModelANN import ModelANN
from Model.ModelHeuristic import ModelHeuristic
from Model.ModelConst import ModelConst

class ModelFactory(object):
	""" ModelFactory: FactoryClass to generate Models
	"""
	@classmethod
	def build(cls, config):
		if config[ModelConst.TYPE].lower() == ModelConst.TYPE_HEURISTIC:
			return ModelHeuristic(config)
		if config[ModelConst.TYPE].lower() == ModelConst.TYPE_ANN:
			return ModelANN(config)
