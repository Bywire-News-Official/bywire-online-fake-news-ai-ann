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
import xml.etree.ElementTree as ElementTree

class Config(object):
	def __init__(self, path):
		if not path is None:
			tree = ElementTree.parse(path).getroot()
			self.m_tree = tree
		else:
			self.m_tree = None

	def __enter__(self):
		return self
		
	def __exit__(self, type, value, traceback):
		pass
			
	def getNodes(self, tags):
		nodes = [ self.m_tree ]
		for tag in tags:
			nodes = [ child for node in nodes for child in node if child.tag == tag]
		configs = [ ]
		for node in nodes:
			conf = Config(None)
			conf.m_tree = node
			configs.append(conf)
		return configs
	
	def path(self, tags):
		return os.path.join(*self[tags].split('/'))


	def __getitem__(self, tags):
		nodes = [ self.m_tree ]
		for tag in tags:
			nodes = [ child for node in nodes for child in node if child.tag == tag]
		if len(nodes)==1:
			return nodes[0].text.strip()
		else:
			return [ node.text.strip() for node in nodes ]

	def __contains__(self, tags):
		assert(isinstance(tags, list) or isinstance(tags, tuple))
		return len(self.__getitem__(tags)) > 0
	
	@property
	def text(self):
		return self.m_tree.text
