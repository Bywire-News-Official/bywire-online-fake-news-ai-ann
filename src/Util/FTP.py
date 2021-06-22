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
sys.path.append(os.getcwd())
from Util.Config import Config
from Util.Const import Const
import time
import requests
import argparse
from urlparse import urlparse
import urllib3
# Disable some warnings related to ssl certificates of the itscope server
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)
urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)
urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning)
# Reconnect times in case download fails

class FTP(object):
	DOWNLOAD_WAIT_TIMES = (5, 10)
	
	def __init__(self, config, user="", password=""):
		
		self.m_path = config[Const.LOCK_FILE]
		self.m_timeout	 = config[Const.LOCK_TIMEOUT]
		self.m_timeout	 = [int(item) for item in self.m_timeout.split(':')]
		self.m_timeout	 = timedelta(hours=self.m_timeout[0], minutes=self.m_timeout[1], seconds=self.m_timeout[2])
		self.m_separator = config[Const.LOCK_SEPARATOR]
		self.m_format	 = config[Const.LOCK_FORMAT]
		
	def download(self, remote_path, local_path):
		for wait_time in FTP.DOWNLOAD_WAIT_TIMES:
			try:
				r = requests.get(remote_path, auth=(settings[('general_settings', 'itscope_usr')], settings[('general_settings', 'itscope_pw')]))
				if r.status_code == Const.DOWNLOAD_STATUS_SUCCESS:
					# Write to file if download successful
					with open(filename, 'wb') as output:
						for bits in r.iter_content():
							output.write(bits)
						success = True
				elif r.status_code == Const.DOWNLOAD_STATUS_INVALID_PWD:
					print "Invalid Username or Password"
					sys.stderr.write("Invalid Username or Password\n")
					exit(0)
				else:
					sys.stderr.write("Unknown status. Status: {0:d} Trying reconnect in {1:d}s \n".format(r.status_code, wait_time))
					time.sleep(wait_time)
					continue
			except KeyboardInterrupt:
				raise
			except Exception as e:
				sys.stderr.write("Error downloading data. Reconnect in: {0:d}\n".format(wait_time))
				print(e.message)
				raise
				# Case of a disconnect, wait a bit and try again
				time.sleep(wait_time)
				continue
			break
		if success:
			print "Download successful"
		else:
			sys.stderr.write("Error downloading file: {0:s}\n".format(filename))
					
	
	
		
		

if (__name__ == "__main__"):
	parser = argparse.ArgumentParser(description='Process product xmls itscope.')
	parser.add_argument('-c', '--config', default=Const.CONFIG_FILE, help="Config file - default: {0:s}".format(Const.CONFIG_FILE))
	args = parser.parse_args()

	with Config(args.config) as config, Config(Const.DOWNLOAD_SETTINGS_FILE) as settings:
		url = config[Const.DOWNLOAD_URL]
		# Determine which tags are available.
		for i in range(1, 100000):
			key = settings[Const().DOWNLOAD_SOURCE_FILE(i)]
			if not key:
				break
			filename = os.path.join(config[Const.INPUT_PATH], config[Const.DOWNLOAD_TARGET_FILE].format(i))
			print "Downloading: {0:s}".format(key)
			# Loop to allow for disconnects
			success = False
			for wait_time in Const.DOWNLOAD_WAIT_TIMES:
				try:
					#http = urllib3.PoolManager()
					#headers = urllib3.util.make_headers(basic_auth='abc:xyz')
					#r = http.request('GET', url, headers=headers)
					# Actual download
					r = requests.get(url.format(key), auth=(settings[('general_settings', 'itscope_usr')], settings[('general_settings', 'itscope_pw')]))
					if r.status_code == Const.DOWNLOAD_STATUS_SUCCESS:
						# Write to file if download successful
						with open(filename, 'wb') as output:
							for bits in r.iter_content():
								output.write(bits)
							success = True
					elif r.status_code == Const.DOWNLOAD_STATUS_INVALID_PWD:
						print "Invalid Username or Password"
						sys.stderr.write("Invalid Username or Password\n")
						exit(0)
					else:
						sys.stderr.write("Unknown status. Status: {0:d} Trying reconnect in {1:d}s \n".format(r.status_code, wait_time))
						time.sleep(wait_time)
						continue
				except KeyboardInterrupt:
					raise
				except Exception as e:
					sys.stderr.write("Error downloading data. Reconnect in: {0:d}\n".format(wait_time))
					print(e.message)
					raise
					# Case of a disconnect, wait a bit and try again
					time.sleep(wait_time)
					continue
				break
			if success:
				print "Download successful"
			else:
				sys.stderr.write("Error downloading file: {0:s}\n".format(filename))
				
