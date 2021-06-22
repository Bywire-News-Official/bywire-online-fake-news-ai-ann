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

class Const(object):
	CSV_SEPARATOR				= ('input', 'csv-separator')
	CONFIG_PATH				= os.path.join((os.environ.get("APP_ROOT")) if os.environ.get("APP_ROOT") else ".", 'Config', 'Config.xml')
	STORAGE_BASE_PATH			= ('storage', 'base-path')
	STORAGE_KEYS_FILE			= ('storage', 'keys', 'file')
	STORAGE_KEYS_PATH			= ('storage', 'keys', 'path')
	STORAGE_BLOCK_EXPLORER			= ('storage', 'block-explorer', 'path')
	STORAGE_BLOCK_EXPLORER_URL		= ('storage', 'block-explorer', 'url')
	STORAGE_PUBLISHED_TRANSACTIONS		= ('storage', 'block-explorer', 'published-transactions')
	STORAGE_PUBLISHED_ARTICLES		= ('storage', 'block-explorer', 'published-articles')
	STORAGE_CERTIFIED_TRANSACTIONS		= ('storage', 'block-explorer', 'certified-transactions')

	STORAGE_TRANSACTIONS_SETTINGS		= ('storage', 'transaction-explorer', 'settings')
	STORAGE_TRANSACTIONS_PATH		= ('storage', 'transaction-explorer', 'path')
	STORAGE_TRANSACTIONS_FILE		= ('storage', 'transaction-explorer', 'file')
	STORAGE_TRANSACTIONS_URL		= ('storage', 'transaction-explorer', 'url')

	STORAGE_TRANSFER_LIMITS_FILE		= ('storage', 'transfer-limits', 'file')
	STORAGE_KEYS_PATH_BACKUP		= ('storage', 'keys', 'path-backup')
	STORAGE_STAKES_PATH			= ('storage', 'stakes', 'path')
	STORAGE_STAKES_FILE			= ('storage', 'stakes', 'file')
	STORAGE_CLEOS_PATH			= ('storage', 'cleos', 'path')
	STORAGE_KEYS_COPY_CMD			= ('storage', 'keys', 'copy-cmd')

	EXPERTAI_USE				= ('api', 'expertai', 'use')
	EXPERTAI_USERNAME			= ('api', 'expertai', 'username')
	EXPERTAI_PASSWORD			= ('api', 'expertai', 'password')
	
	EOS_METHOD				= ('eos', 'method')
	EOS_URL					= ('eos', 'url')
	EOS_TOKEN				= ('eos', 'token')
	EOS_ISSUER_WALLET			= ('eos', 'issuer-wallet')
	EOS_NEW_WALLET_DEPOSIT			= ('eos', 'new-wallet', 'initial-deposit')
	EOS_NEW_WALLET_RAM_STAKE		= ('eos', 'new-wallet', 'ram-stake')
	EOS_NEW_WALLET_LOCAL_PATH		= ('eos', 'new-wallet', 'local-path')
	EOS_NEW_WALLET_CPU_STAKE		= ('eos', 'new-wallet', 'cpu-stake')
	EOS_NEW_WALLET_CPU_MAX_STAKE		= ('eos', 'new-wallet', 'cpu-max-stake')
	EOS_NEW_WALLET_RAM_KB			= ('eos', 'new-wallet', 'ram-kb')
	EOS_NEW_WALLET_RAM_MAX_KB		= ('eos', 'new-wallet', 'ram-kb')
	EOS_NEW_WALLET_NET_STAKE		= ('eos', 'new-wallet', 'net-stake')
	EOS_NEW_WALLET_NET_MAX_STAKE		= ('eos', 'new-wallet', 'net-max-stake')
	EOS_NEW_WALLET_STAKE_TIMEOUT		= ('eos', 'new-wallet', 'stake-timeout')
	EOS_NEW_WALLET_STAKE_DEAD		= ('eos', 'new-wallet', 'stake-dead')
	EOS_REQUEST_RETRY			= ('eos', 'request-max-requeue')
	EOS_HEARTBEAT_INTERVAL			= ('eos', 'heartbeat', 'interval')
	EOS_READ_READER_SHARE			= ('eos', 'read-reader-share')
	EOS_READ_WRITER_SHARE			= ('eos', 'read-writer-share')
	EOS_READ_PUBLISHER_SHARE		= ('eos', 'read-publisher-share')


	EOS_BASE_PRECISION			= ('eos', 'eos-precision')
	EOS_BASE_TOKEN				= ('eos', 'eos-token')
	REX_CPU_STAKE				= ('eos', 'rex', 'cpu-stake')
	REX_NET_STAKE				= ('eos', 'rex', 'net-stake')
	REX_MAX_CPU_STAKE			= ('eos', 'rex', 'max-cpu-stake')
	REX_MAX_NET_STAKE			= ('eos', 'rex', 'max-net-stake')

	PUBLISH_NEW_AMOUNT			= ('publish', 'new', 'amount')
	PUBLISH_UPDATE_AMOUNT			= ('publish', 'update', 'amount')

	WEB_URL					= ('web', 'url')
	WEB_PUBLISH_ENDPOINT			= ('web', 'publish-endpoint')
	WEB_API_KEY				= ('web', 'api-key')
	WEB_DEFAULT_PUBLISHER_ID		= ('web', 'default-publisher-id')
	
	WEB_URL					= ('web', 'url')
	WEB_PUBLISH_ENDPOINT			= ('web', 'publish-endpoint')
	WEB_API_KEY				= ('web', 'api-key')
	WEB_DEFAULT_PUBLISHER_ID		= ('web', 'default-publisher-id')
	
	EOS_VALID_NAMES				= ('eos', 'valid-names')
	TOKEN_PRECISION				= ('eos', 'token-precision')
	EOS_PRECISION				= ('eos', 'eos-precision')
	
	REQ_EMAIL				= 'email'
	REQ_READER				= 'reader'
	REQ_USERNAME				= 'username'
	REQ_WALLET				= 'wallet'
	REQ_PARENT				= 'parent'
	REQ_NAME				= 'name'
	REQ_WALLET_NAME				= 'wallet-name'
	REQ_PASSWORD				= 'password'
	REQ_SECRET				= 'secret'
	REQ_ARTICLE				= 'article'
	REQ_ARTICLE_TITLE			= 'article-title'
	REQ_ARTICLE_AUTHOR			= 'article-author'
	REQ_ARTICLE_CONTENT			= 'article-content'
	REQ_ARTICLE_TIMESTAMP			= 'article-timestamp'
	REQ_ARTICLE_PREVIEW			= 'article-preview'
	REQ_ARTICLE_SLUG			= 'article-slug'
	REQ_AMOUNT				= 'amount'
	REQ_FROM				= 'from'
	REQ_TO					= 'to'
	REQ_PAGE				= 'page'
	REQ_PAGE_SIZE				= 'page-size'
	REQ_WRITER				= 'writer'
	REQ_PUBLISHER				= 'publisher'
	REQ_READ_RATE				= 'read-rate'
	REQ_TIP_RATE				= 'tip-rate'
	REQ_TRANSFER_RATE			= 'transfer-rate'
	REQ_WRITER_RATE				= 'writer-rate'
	REQ_PUBLISHER_RATE			= 'publisher-rate'
	REQ_JWT						= 'jwt'


	EOS_CHECK_LIQUID_ABS		= ('eos-check', 'warn-liquid-abs')
	EOS_CHECK_LIQUID_PERC		= ('eos-check', 'warn-liquid-perc')
	EOS_CHECK_TOKEN_ABS		= ('eos-check', 'warn-token-abs')
	EOS_CHECK_TOKEN_PERC		= ('eos-check', 'warn-token-perc')
	EOS_CHECK_WARN_RAM_KB		= ('eos-check', 'warn-ram-kb')
	EOS_CHECK_WARN_CPU_MS		= ('eos-check', 'warn-cpu-ms')
	EOS_CHECK_WARN_BW_MS		= ('eos-check', 'warn-bw-ms')
	EOS_CHECK_INTERVAL		= ('eos-check', 'check-interval')

	LOG_LEVEL			= ('logging', 'level')
	LOG_PATH			= ('logging', 'path')
	LOG_FORMAT			= ('logging', 'format')
	LOG_LOGGER			= ('logging', 'logger')
	LOGGER_LEVEL			= ('level', )
	LOGGER_NAME			= ('name', )
	LOGGER_DESTINATION		= ('destination', )
	
	EMAIL_HOST_KEY			= ('email', 'host')
	EMAIL_MSG_HEADER_KEY		= ('email', 'message-text-error')
	EMAIL_MSG_TEXT_KEY		= ('email', 'message-header-error')
	EMAIL_PORT_KEY			= ('email', 'port')
	EMAIL_USER_KEY			= ('email', 'user')
	EMAIL_ADDRESS_KEY		= ('email', 'address')
	EMAIL_PASS_KEY			= ('email', 'password')
	EMAIL_TEMPLATES			= ('email', 'templates', 'path')
	EMAIL_TEMPLATE_APIKEYS		= ('email', 'templates', 'email-apikeys')

