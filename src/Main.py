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
import sys
from gevent import monkey
monkey.patch_all(subprocess=True)
from datetime import datetime
import time
import json
import threading
import re
import codecs
import signal
import cProfile

from Server.Analyzer import Analyzer
from Util.Const import Const
from Util.Config import Config
from Util.Log import Log

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

global config, analyzer, PARAMETER_VERSION


app = Flask(__name__)
#app.config['PROFILE'] = True
#app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

api = Api(app)

from Server import Resources

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

@app.route('/')
def index():
    pass


config = Config(Const.CONFIG_PATH)
config.__enter__()
log = Log(config)
analyzer = Analyzer.get(config)
analyzer.start()
#api.add_resource(Resources.UserRegistration,		'/registration')
#api.add_resource(Resources.UserLogin,			'/login')
#api.add_resource(Resources.UserLogoutAccess,		'/logout')
#api.add_resource(Resources.UserLogoutRefresh,		'/logout/refresh')
#api.add_resource(Resources.TokenRefresh,		'/token/refresh')
#api.add_resource(Resources.GenerateKeys,		'/generatekeys')

api.add_resource(Resources.CalibrateParameters,		'/parameters/calibrate')
api.add_resource(Resources.CleanParameters,		'/parameters/clean')
api.add_resource(Resources.RecalculateParameters,	'/parameters/recalculate')
api.add_resource(Resources.AnalyzeFlag,			'/analyze/flag')
api.add_resource(Resources.AnalyzeText,			'/analyze/text')
api.add_resource(Resources.AnalyzeIPFS,			'/analyze/ipfs')
api.add_resource(Resources.AnalyzeQuery,		'/analyze/query')
api.add_resource(Resources.BrewCoffee,			'/brew/coffee')

@app.teardown_appcontext
def shutdown_session(exception=None):
	if exception:
		global config, analyzer
		db_session.remove()
		analyzer.stop()
		config.__exit__(None, None, None)
		

if __name__=='__main__':
	print("Running Main")
	cProfile.run("app.run(host='0.0.0.0', port='5055')", "profile.prof")


	
