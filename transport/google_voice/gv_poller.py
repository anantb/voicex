"""
Copyright (c) 2012 Anant Bhardwaj

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import time, threading, sys, json, re, daemon
from bs4 import BeautifulSoup

'''
@author: anant bhardwaj
@date: Aug 3, 2012

Google Voice Poller Thread
'''	

class GoogleVoicePoller(threading.Thread):
	def __init__(self, v, callback, d = True):
		self.callback = callback
		self.v = v
		self.d = d	
		threading.Thread.__init__(self)
		print "Google Voice polling thread started"
	
	
	def process(self, meta, page):
		res = re.search(r'<html>(.*?)</html>', page, re.DOTALL)
		body = res.group()
		body = body.strip().lstrip('<html>').rstrip('</html>').strip().lstrip("<![CDATA[").rstrip("]]>").strip()
		soup = BeautifulSoup(body)
		msg_thread = soup.find('div', {'id': meta['id']})
		messages = msg_thread.findAll('div', {'class' : 'gc-message-sms-row'})
		phone_num = messages[-1].find('span', {'class' : 'gc-message-sms-from'}).find(text=True).strip().rstrip(':').strip()
		text = messages[-1].find('span', {'class' : 'gc-message-sms-text'}).find(text=True).strip()
		return {'id':meta['id'], 'messageText': text, 'phoneNumber': phone_num}
		
	def poll_new(self):
		while(True):		
			try:				
				meta_data, page = self.v.fetch_unread_sms()				
				inbox = json.loads(meta_data)
				if(inbox['unreadCounts']['sms'] > 0):
					for msg in inbox['messages']:						
						if(not (inbox['messages'][msg]['isRead'] or inbox['messages'][msg]['isTrash'])):							
							m = self.process(inbox['messages'][msg], page)
							print m
							self.callback(m)						
			except:
				print sys.exc_info()
			time.sleep(1)
		
	def run(self):
		if(self.d):
			with daemon.DaemonContext():
				self.poll_new()
		else:
			self.poll_new()
			
	
	
					
			
