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

class Messages(object):
	SUCCESS		= {'success': True}
	LOGIN_FAIL_USER_NOT_DEFINED	= {'code': 'LOGIN_FAIL_USER_NOT_DEFINED', 'message': 'User does not exists', 'success': False}
	LOGIN_FAIL_INVALID_CREDENTIALS	= {'code': 'LOGIN_FAIL_INVALID_CREDENTIALS', 'message': 'Invalid Credentials', 'success': False}
	LOGIN_SUCCESS			= {'code': 'LOGIN_SUCCESS', 'message': 'Logged in as {0:s}', 'access_token': '', 'refresh_token': '', 'success': True}
	REGISTER_FAIL_USER_EXISTS	= {'code': 'REGISTER_FAIL_USER_EXISTS', 'message': 'User already exists in db', 'success': False}
	REGISTER_FAIL_SECRET_INVALID	= {'code': 'REGISTER_FAIL_INVALID_SECRET', 'message': 'Secret invalid', 'success': False}
	REGISTER_SUCCESS		= {'code': 'REGISTER_SUCCESS', 'message': 'User {0:s} was created', 'access_token': '', 'refresh_token': '', 'success': True}
	REGISTER_FAIL			= {'code': 'REGISTER_FAIL', 'message': 'Register failed on unidentified error', 'success': False}

	GENKEYS_SUCCESS			= {'code': 'GENKEYS_SUCCESS', 'message': 'Generate api keys success', 'success': True}
	GENKEYS_FAIL_USER_EXISTS	= {'code': 'GENKEYS_FAIL_USER_EXISTS', 'message': 'Generate api keys failed because user already exists', 'success': False}
	GENKEYS_FAIL_INVALID_ROLE	= {'code': 'GENKEYS_FAIL_INVALID_ROLE', 'message': 'Generate api keys failed because invalid role', 'success': False}
	GENKEYS_FAIL_INVALID_WALLET	= {'code': 'GENKEYS_FAIL_INVALID_WALLET', 'message': 'Generate api keys failed because wallet is invalid', 'success': False}
	GENKEYS_FAIL			= {'code': 'GENKEYS_FAIL', 'message': 'Generate api keys failed because of unknown reason', 'success': False}

	LOGOUT_SUCCESS					= {'code': 'LOGOUT_SUCCESS', 'message': 'Logout successful - Token Revoked', 'success': True}
	LOGOUT_FAIL						= {'code': 'LOGOUT_FAIL', 'message': 'Logout failed due to unknown error', 'success': False}
	TOKEN_REFRESH_SUCCESS			= {'code': 'TOKEN_REFRESH_SUCCESS', 'message': 'Token succesfully refreshed', 'success': True}
	TOKEN_REFRESH_FAIL_INVALID		= {'code': 'TOKEN_REFRESH_FAIL_INVALID', 'message': 'Invalid Refresh Token', 'success': False}
	TOKEN_REFRESH_FAIL				= {'code': 'TOKEN_REFRESH_FAIL', 'message': 'Token Refresh failed due to unknown Error', 'success': False}
	FEE_IMPROPER_PACING				= {'code': 'FEE_IMPROPER_PACING', 'message': 'Can only set one fee at a time', 'success': False}
	FEE_SUCCESS				= {'code': 'FEE_SUCCESS', 'message': 'Fee set successfully', 'success': True}
	FEE_FAIL_UNKNOWN				= {'code': 'FEE_FAIL_UNKNOWN', 'message': 'Fee set failed due to unknown reason', 'success': False}
	FEE_FAIL_AUTHORIZATION				= {'code': 'FEE_FAIL_AUTHORIZATION', 'message': 'Fee set failed due to insufficient authorization', 'success': False}
	
	TIP_SUCCEEDED = {'code': 'TIP_SUCCEED', 'message': 'Tipping was successful for article {0:s}', 'success': True}
	TIP_FAIL_UNKNOWN = {'code': 'TIP_FAIL_UNKNOWN', 'message': 'Tipping failed for unknown reason', 'success': False}
	TIP_FAIL_NO_ARTICLE = {'code': 'TIP_FAIL_NO_ARTICLE', 'message': 'Tipping failed as article is unknown {0:s}', 'success': False}
	TIP_FAIL_NO_ACCOUNT = {'code': 'TIP_FAIL_NO_ACCOUNT', 'message': 'Tipping failed as user has no wirebit account {0:s}', 'success': False}
	TIP_FAIL_AUTHORIZATION = {'code': 'TIP_FAIL_AUTHORIZATION', 'message': 'Tipping failed due to insufficient authorization for user {0:s}', 'success': False}
	TIP_FAIL_NO_WRITER = {'code': 'TIP_FAIL_NO_WRITER', 'message': 'Tipping failed as the writers account does not exist', 'success': False}

	READ_SUCCEEDED = {'code': 'READ_SUCCEED', 'message': 'Read was successful for article {0:s}', 'success': True}
	READ_SUCCESS_ALREADY_READ = {'code': 'READ_SUCCEED', 'message': "Article was already read", 'success': True}
	READ_FAIL_UNKNOWN = {'code': 'READ_FAIL_UNKNOWN', 'message': 'Read failed for unknown reason', 'success': False}
	#READ_FAIL_INVALID_ARTICLE = {'code': 'READ_FAIL_INVALID_ARTICLE', 'message': 'Read failed as article is unknown {0:s}', 'success': True}
	#READ_FAIL_INVALID_ACCOUNT = {'code': 'READ_FAIL_INVALID_ACCOUNT', 'message': 'Read failed as user has no wirebit account {0:s}', 'success': True}
	READ_FAIL_INVALID_ARTICLE = {'code': 'READ_SUCCEED', 'message': 'Read failed as article is unknown {0:s}', 'success': True}
	READ_FAIL_INVALID_ACCOUNT = {'code': 'READ_SUCCEED', 'message': 'Read failed as user has no wirebit account {0:s}', 'success': True}
	READ_FAIL_AUTHORIZATION = {'code': 'READ_FAIL_AUTHORIZATION', 'message': 'Read failed due to insufficient authorization for user {0:s}', 'success': False}
	READ_FAIL_INVALID_WRITER = {'code': 'READ_FAIL_INVALID_WRITER', 'message': 'Read failed as the writers account does not exist', 'success': False}

	TRANSFER_SUCCEEDED = {'code': 'TRANSFER_SUCCEED', 'message': 'Transfer was successful', 'success': True}
	TRANSFER_FAIL_UNKNOWN = {'code': 'TRANSFER_FAIL_UNKNOWN', 'message': 'Transfer failed for unknown reason', 'success': False}
	TRANSFER_FAIL_INVALID_TO = {'code': 'TRANSFER_FAIL_INVALID_TO', 'message': 'Transfer failed as to account is unknown {0:s}', 'success': False}
	TRANSFER_FAIL_INVALID_FROM = {'code': 'TRANSFER_FAIL_INVALID_FROM', 'message': 'Transfer failed as from account is unknown {0:s}', 'success': False}
	TRANSFER_FAIL_INVALID_AMOUNT = {'code': 'TRANSFER_FAIL_INVALID_AMOUNT', 'message': 'Transfer failed as the amount was invalid {0:s}', 'success': False}
	TRANSFER_FAIL_INVALID_BALANCE = {'code': 'TRANSFER_FAIL_INVALID_AMOUNT', 'message': 'Transfer failed as the amount was invalid {0:s}', 'success': False}
	TRANSFER_FAIL_AUTHORIZATION = {'code': 'TRANSFER_FAIL_AUTHORIZATION', 'message': 'Transfer failed due to an authorization failure', 'success': False}
	TRANSFER_FAIL_TIP_FIRST = {'code': 'TRANSFER_FAIL_TIP_FIRST', 'message': 'Transfer failed you will have to tip and read before you can transfer you wire', 'success': False}
	
	
	BUY_SUCCESS = {'code': 'BUY_SUCCESS', 'message': 'Successfully bought wirebits', 'success': True}
	BUY_FAIL_INSUFFICIENT_FUNDS = {'code': 'BUY_FAIL_INSUFFICIENT_FUNDS', 'message': 'Issuer has insufficient funds. Please issue more token to the issuer account.', 'success': False}
	BUY_FAIL_INVALID_USER = {'code': 'BUY_FAIL_INVALID_USER', 'message': 'Buy cannot be processed as username is invalid.', 'success': False}
	BUY_FAIL_UNKNWON = {'code': 'BUY_FAIL_UNKNOWN', 'message': 'Buy failed due to unknown reason.', 'success': False}

	SELL_SUCCESS = {'code': 'SELL_SUCCESS', 'message': 'Successfully sold wirebits', 'success': True}
	SELL_FAIL_INSUFFICIENT_FUNDS = {'code': 'SELL_FAIL_INSUFFICIENT_FUNDS', 'message': 'Seller has insufficient funds.', 'success': False}
	SELL_FAIL_INVALID_USER = {'code': 'SELL_FAIL_INVALID_USER', 'message': 'Sell cannot be processed as username is invalid.', 'success': False}
	SELL_FAIL_UNKNWON = {'code': 'SELL_FAIL_UNKNOWN', 'message': 'Sell failed due to unknown reason.', 'success': False}

	PUBLISH_SUCCEEDED = {'code': 'PUBLISH_SUCCEED', 'message': 'Publish was successful for article {0:s}', 'success': True}
	PUBLISH_FAIL_UNKNOWN = {'code': 'PUBLISH_FAIL_UNKNOWN', 'message': 'Publish failed for unknown reason', 'success': False}
	PUBLISH_FAIL_INSUFFICIENT_FUNDS = {'code': 'PUBLISH_FAIL_INSUFFICIENT_FUNDS', 'message': 'Publish failed due to insufifient funds. Please buy more wirebits', 'success': False}
	PUBLISH_FAIL_DUPLICATE_ARTICLE = {'code': 'PUBLSIH_DUPLICATE_ARTICLE', 'message': 'Publish failed due to a hash-collision. Create a new hash and try again {0:s}', 'success': False}
	PUBLISH_FAIL_INVALID_ARTICLE = {'code': 'PUBLSIH_FAIL_INVALID_ARTICLE', 'message': 'Publish failed due to an invalid article hash {0:s}', 'success': False}
	PUBLISH_FAIL_INVALID_WRITER = {'code': 'PUBLISH_FAIL_INVALID_WRITER', 'message': 'Publish failed as writer has no wirebit account {0:s}', 'success': False}
	PUBLISH_FAIL_INVALID_PUBLISHER = {'code': 'PUBLISH_FAIL_INVALID_PUBLISHER', 'message': 'Publish failed as publisher is not missing, but has no wirebit account {0:s}', 'success': False}
	PUBLISH_FAIL_AUTHORIZATION = {'code': 'PUBLISH_FAIL_AUTHORIZATION', 'message': 'Publish failed due to insufficient authorization for user {0:s}', 'success': False}

	PUBLISH_SUCCEEDED = {'code': 'PUBLISH_SUCCEED', 'message': 'Publish was successful for article {0:s}', 'success': True}
	PUBLISH_FAIL_UNKNOWN = {'code': 'PUBLISH_FAIL_UNKNOWN', 'message': 'Publish failed for unknown reason', 'success': False}
	PUBLISH_FAIL_DUPLICATE_ARTICLE = {'code': 'PUBLISH_DUPLICATE_ARTICLE', 'message': 'Publish failed due to a hash-collision. Create a new hash and try again {0:s}', 'success': False}
	PUBLISH_FAIL_INVALID_ARTICLE = {'code': 'PUBLISH_FAIL_INVALID_ARTICLE', 'message': 'Publish failed due to an invalid article hash {0:s}', 'success': False}
	PUBLISH_FAIL_INVALID_WRITER = {'code': 'PUBLISH_FAIL_INVALID_WRITER', 'message': 'Publish failed as writer has no wirebit account {0:s}', 'success': False}
	PUBLISH_FAIL_INVALID_PUBLISHER = {'code': 'PUBLISH_FAIL_INVALID_PUBLISHER', 'message': 'Publish failed as publisher is not missing, but has no wirebit account {0:s}', 'success': False}
	PUBLISH_FAIL_AUTHORIZATION = {'code': 'PUBLISH_FAIL_AUTHORIZATION', 'message': 'Publish failed due to insufficient authorization for user {0:s}', 'success': False}

	CREATE_SUCCESS = {'code': 'CREATE_SUCCESS', 'message': 'Wallet created successfully. Enter the active and owner keys on the jungle testnet under monitor.jungle.cr', 'private_key': '', 'owner_private_key': '', 'owner_public_key': '', 'active_private_key': '', 'active_public_key': '', 'success': True}
	CREATE_FAIL_WALLET_EXISTS = {'code': 'CREATE_FAIL_WALLET_EXISTS', 'message': 'Wallet creation failed as wallet already exists', 'success': False}
	CREATE_FAIL_WALLETNAME_INVALID = {'code': 'CREATE_FAIL_WALLETNAME_INVALID', 'message': 'Wallet creation failed as wallet name was invalid', 'success': False}
	CREATE_FAIL_NETWORK_ERROR = {'code': 'CREATE_FAIL_NETWORK_ERROR', 'message': 'Wallet creation failed due to errors to connect to the blockchain netword', 'success': False}
	CREATE_SUCCESS_FAIL_KEY_CREATION = {'code': 'CREATE_SUCCESS_FAIL_KEY_CREATION', 'message': 'Wallet creation succeeded, but active and owner keys were not properly generated', 'private_key': '', 'success': False}
	CREATE_FAIL_UNKNOWN = {'code': 'CREATE_FAIL_UNKNOWN', 'message': 'Wallet creation failed due to unknown error', 'success': False}

	ACCOUNT_BALANCE_SUCCESS = {'code': 'ACCOUNT_BALANCE_SUCCESS', 'message': 'Account balance successfuly queried', 'success': True}
	ACCOUNT_BALANCE_FAIL_UNKNOWN = {'code': 'ACCOUNT_BALANCE_FAIL_UNKNOWN', 'message': 'Account balance query failed for unknown reason', 'success': False}
	FX_SUCCESS = {'code': 'FX_SUCCESS', 'message': 'FX-rates successfuly queried', 'success': True}


	GENERAL_INVALID_ISSUER_PASSWORD = {'code': 'GENERAL_INVALID_ISSUER_PASSWORD', 'message': 'Server not setup correctly - issuer password is invalid', 'success': False}
	GENERAL_INVALID_USER = {'code': 'GENERAL_INVALID_USER', 'message': 'User not valid', 'success': False}
	GENERAL_KEOSD_ERROR = {'code': 'GENERAL_KEOSD_ERROR', 'message': 'Keosd had an hiccup on the incomming message. Retry will resolve it', 'success': False}
	GENERAL_INVALID_PASSWORD = {'code': 'GENERAL_INVALID_PASSWORD', 'message': 'User password is not valid', 'success': False}
	GENERAL_CPU_INSUFFICIENT = {'code': 'GENERAL_CPU_INSUFFICIENT', 'message': 'Insufficient CPU', 'success': False}
	GENERAL_RAM_INSUFFICIENT = {'code': 'GENERAL_RAM_INSUFFICIENT', 'message': 'Insufficient RAM', 'success': False}
	GENERAL_NET_INSUFFICIENT = {'code': 'GENERAL_NET_INSUFFICIENT', 'message': 'Insufficient Bandwith', 'success': False}
	GENERAL_WALLET_PERMISSIONS = {'code': 'GENERAL_WALLET_PERMISSIONS', 'message': 'Invalid wallet permissions', 'success': False}
	GENERAL_NETWORK_ERROR		= {'code': 'GENERAL_NETWORK_ERROR', 'message': 'Unable to reach EOS node', 'success': False}
	GENERAL_CURRENCY_INVALID   = {"code": "GENERAL_INVALID_CURRENCY", "message": "Invalid Currency in amount"}

	
	VALIDATE_ARTICLE_NOT_RECOGNIZED	= {'code': 'VALIDATE_ARTICLE_NOT_RECOGNIZED', 'message': 'Article hash not recognized. It can be that the article is not uploaded or it is too early to be found in the blockchain', 'success': False}
	VALIDATE_ARTICLE_SUCCESS	= {'code': 'VALIDATE_ARTICLE_SUCCESS', 'message': '{0:s}', 'success': True}

	CERTIFY_ARTICLE_NOT_SPECIFIED	= {'code': 'CERTIFY_ARTICLE_NOT_SPECIFIED', 'message': "Specify either the article_id or article_ipfs_hash", "success": False, 'article': {}, 'revisions': []}
	CERTIFY_ARTICLE_SUCCESS		= {'code': 'CERITFY_ARTICLE_SUCCESS', 'message': '{0:s}', 'success': True}
	CERTIFY_ARTICLE_NOT_FOUND	= {'code': 'CERITFY_ARTICLE_NOT_FOUND', 'message': 'Article not found in db', 'success': False, 'article': {}, 'revisions': []}
	TRUST_ARTICLE_SUCCESS		= {'code': 'TRUST_ARTICLE_SUCCESS', 'message': '{0:s}', 'success': True}
	TRUST_ARTICLE_NOT_FOUND		= {'code': 'TRUST_ARTICLE_NOT_FOUND', 'message': '{0:s}', 'success': False}

	GENERAL_NETWORK_ERROR		= {'code': 'GENERAL_NETWORK_ERROR', 'message': 'Unable to reach EOS node', 'success': False}

	PUBLISHER_REPORT_SUCCESS	= {'code': 'PUBLISHER_REPORT_SUCCESS', 'message': 'Successfully queries publisher report', 'count_total': 0, 'count_since': 0, 'success': True}
	STAKES_SUCCESS			= {'code': 'STAKES_SUCCESS', 'message': 'Successfully queries stakes', 'count_total': 0, 'count_since': 0, 'success': True}
	ACCOUNT_REPORT_SUCCESS		= {'code': 'ACCOUNT_REPORT_SUCCESS', 'message': 'Successfully queries account report', 'count_total': 0, 'count_since': 0, 'success': True}


	ARTICLES_CHANGESET_SUCCESS	= {'code': 'ARTICLES_CHANGESET_SUCCESS', 'message': 'Successfully queried changeset', 'count': 0, 'data': [], 'success': True}



	CURRENCY_CONVERT_SUCCESS	= {'code': 'CURRENCY_CONVERT_SUCCESS', 'message': 'Displayed quotes have a latency up to 6 min and exclude exchange/broker commissions', 'success': True}
	CURRENCY_CONVERT_FAIL		= {'code': 'CURRENCY_CONVERT_FAIL', 'message': 'Failure while trying to convert currency', 'success': False}

	TRANSACTION_HISTORY_SUCCESS	= {'code': 'TRANSACTION_HISTORY_SUCCESS', 'message': 'Transaction History Success', 'success': True}
	TRANSACTION_HISTORY_FAIL	= {'code': 'TRANSACTION_HISTORY_FAIL', 'message': 'Transaction History Failed due to problems with username', 'success': True}

	TRANSACTION_REPORT_SUCCESS	= {'code': 'TRANSACTION_REPORT_SUCCESS', 'message': 'Transaction Report Success', 'success': True}
	TRANSACTION_REPORT_FAIL	= {'code': 'TRANSACTION_REPORT_FAIL', 'message': 'Transaction Report Failed due to problems with username', 'success': True}

	HEARTBEAT_SUCCESS = {'code': 'HEARTBEAT_SUCCESS', 'message': 'Heartbeat was successful', 'success': True}
	
	
	ERROR_SUCCESS = 0
	ERROR_INVALID_PASSWORD = 1
	
	




