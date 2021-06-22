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


import requests
import pymongo
import json
import time

client	 = pymongo.MongoClient("mongodb://localhost:27017/")
db	 = client["bywire"]
articles = db["articles"]
analyzer = "http://127.0.0.1:5055"
routes	 = {'text':  analyzer+'/analyze/text',
	    'query': analyzer+'/analyze/query'}

for (i, item) in enumerate(articles.find()):
	if i < 0:
		continue
	#print(i)
	if i%1000 == 0:
		print(i)
		time.sleep(10)
	record = {'content':   item['content'],
		  'title':     item['title'],
		  'platform':  "bywire",
		  'author':    item['author'] if 'author' in item else "",
		  'publisher': item['publisher'] if 'publisher' in item else ""}
	for (key, value) in record.items():
		record[key] = record[key] if record[key] else ""
	request = requests.post(routes['text'], params=record)
	response = json.loads(request.text)
	id = response["id"]
	if response["new"]:
		time.sleep(0.01)



