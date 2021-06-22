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

class IPFSConst(object):
	CHANNEL_NAME		= "bywire-channel-{0:s}-{1:s}"
	CONFIG_READ_ONLY_SERVER	= ('storage', 'ipfs-server', 'read-only')
	CONFIG_SERVER_URL	= ('storage', 'ipfs-server', 'url')
	CONFIG_SERVER_PORT	= ('storage', 'ipfs-server', 'port')
	CONFIG_SERVER_NODE	= ('storage', 'ipfs-server', 'node')
	IPFS_PATH		= ('storage', 'ipfs-server', 'ipfs-path')
	IPFS_OUTPUT		= ('storage', 'ipfs-server', 'ipfs-path-output')
	IPFS_PEER_REF		= ('storage', 'ipfs-server', 'peer-ref')
	IPFS_PEERS_FILE		= ('storage', 'ipfs-server', 'peers-file')
	IPFS_PEER_IP_STABLE	= ('storage', 'ipfs-server', 'ip-stable')
	IPFS_PEER_IP_ADDRESS	= ('storage', 'ipfs-server', 'ip-address')
	IPFS_PEER_IP_COMMAND	= ('storage', 'ipfs-server', 'ip-command')
	IPFS_NODE		= ('storage', 'ipfs-server', 'node')

	SERVER_MODE		= ('storage', 'ipfs-server', 'server-mode')
	SERVER_MODE_SINGLE	= 'stand-alone'
	SERVER_MODE_SLAVE	= 'slave'
	SERVER_MODE_MASTER	= 'master'

	CACHE_LENGTH		= ('storage', 'article-cache', 'length')
	CACHE_CLEAN_FREQUENCY	= ('storage', 'article-cache', 'clean-frequency')
	
	
