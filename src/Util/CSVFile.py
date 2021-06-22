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


from Util.Const import Const
import os, os.path
import codecs
import re

# Class to connect to email server and send error reports 
class CSVFile(object):
	ENCODING = 'utf-8'

	def __init__(self, path, mode, separator):
		self.m_path	 = path
		self.m_mode	 = mode
		self.m_separator = separator
		self.m_file	 = None
		self.m_header	 = None
		
	@staticmethod
	def open(path, mode, separator):
		result = CSVFile(path, mode, separator)
		return result.__enter__()
		
	def __enter__(self):
		self.m_file = codecs.open(self.m_path, self.m_mode, encoding=self.ENCODING)
		#self.m_file = open(self.m_path, self.m_mode)
		if (self.m_mode[0] == 'r'):
			self.m_header = [re.sub('^\\ufeff', '', item.strip()) for item in self.m_file.readline().split(self.m_separator)]
		return self

	def __exit__(self, type, value, traceback):
		self.m_file.close()
		
	def close(self):
		self.m_file.close()
	
	def flush(self):
		self.m_file.flush()

	def __iter__(self):
		quoted = ""
		tmp = ""
		data = []
		for line in self.m_file:
			if len(line.strip()) == 0:
				continue
			for item in line:
				if item in ('"', ):
					quoted = item if (quoted == "") else ("" if (quoted == item) else quoted)
					continue
				if item == self.m_separator or item=="\n":
					if (quoted == ""):
						data.append(tmp)
						tmp = ""
						continue
				tmp += item
			if quoted == "":
				if len(data):
					yield dict(zip(self.m_header, data))
				tmp = ""
				data = [];

	def read(self):
		for line in self.m_file:
			yield dict(zip(self.m_header, line.split(self.m_separator)))
			
	def write(self, data):
		assert self.m_header is not None, "CSVFile.write() - Header not set. Please use set_header"
		#assert (type(data} == type({})), "CSVFile.write() - Data is expected to be a dictionary"
		line = [ data[item] if item in data else "" for item in self.m_header ]
		for (index, item) in enumerate(line):
			if (isinstance(item, list)):
				line[index] = str([str(tmp) for tmp in item])
			elif (isinstance(item, str)):
				pass
			else:
				line[index] = str(item)
		self.m_file.write(self.m_separator.join(line)+"\n")
		
	@property
	def header(self):
		return self.m_header

	@header.setter
	def header(self, header):
		self.m_header = header
		self.m_file.write(self.m_separator.join(self.m_header)+"\n")
