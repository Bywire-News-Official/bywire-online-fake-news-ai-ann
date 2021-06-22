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


from flask_restful import Resource, reqparse
from Util.Const import Const

registration_parser = reqparse.RequestParser()
registration_parser.add_argument(Const.REQ_USERNAME,	help = 'This field cannot be blank', required = True)
registration_parser.add_argument(Const.REQ_PASSWORD,	help = 'This field cannot be blank', required = True)
registration_parser.add_argument(Const.REQ_PARENT,	help = 'This field cannot be blank', required = False)
registration_parser.add_argument(Const.REQ_SECRET,	help = 'This field cannot be blank', required = True)
registration_parser.add_argument(Const.REQ_WALLET_NAME,	help = 'This field cannot be blank', required = False)

login_parser = reqparse.RequestParser()
login_parser.add_argument(Const.REQ_USERNAME,	help = 'This field cannot be blank', required = True)
login_parser.add_argument(Const.REQ_PASSWORD,	help = 'This field cannot be blank', required = True)
login_parser.add_argument('version',	help = 'This field cannot be blank', required = False)

analyze_text_parser = reqparse.RequestParser()
analyze_text_parser.add_argument('author',	help = 'This field cannot be blankxxxx', required = True)
analyze_text_parser.add_argument('publisher',	help = 'This field cannot be blankxxx', required = True)
analyze_text_parser.add_argument('platform',	help = 'This field cannot be blankxx', required = True)
analyze_text_parser.add_argument('title',	help = 'This field cannot be blankx', required = True)
analyze_text_parser.add_argument('content',	help = 'This field cannot be blanky', required = True)

analyze_ipfs_parser = reqparse.RequestParser()
analyze_ipfs_parser.add_argument('ipfs_hash',	help = 'This field cannot be blank', required = True)

analyze_query_parser = reqparse.RequestParser()
analyze_query_parser.add_argument('id',	help = 'This field cannot be blank', required = True)

analyze_flag_parser = reqparse.RequestParser()
analyze_flag_parser.add_argument('id',	help = 'This field cannot be blank', required = True)
analyze_flag_parser.add_argument('is_expert',	help = 'This field cannot be blank', required = True)
analyze_flag_parser.add_argument('strength',	help = 'This field cannot be blank', required = True)

