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

import time, threading
from constants import *
from login import *
from util import *
from bs4 import BeautifulSoup

'''
@author: anant bhardwaj
@date: Aug 3, 2012

voicex APIs
'''	
class VoiceX:
	def __init__(self, email, password, server = False):
		self.token = login(email, password)
		self.notifiee = []
		if(server == True):
			t = threading.Thread(target=self.run_server())
			t.daemon = True
			t.start()
	
	def sms(self, to_number, text):
		print "Sending message to: "+ to_number;
		params = {'phoneNumber': to_number, 'text':text, '_rnr_se':self.token['rnr_se']}
		print http_post(SMS_SEND_URL, params, self.token['auth'])
		

	def call(self, forwardingNumber, outgoingNumber):
		print "Initiating call to: "+outgoingNumber + ", through: " + forwardingNumber
		params = {'forwardingNumber': forwardingNumber, 
				  'outgoingNumber':outgoingNumber, 
				  'phoneType':'1',
				  'subscriberNumber':'undefined',
				  'remember' : '0',
				  '_rnr_se':token['rnr_se']}
		print http_post(CALL_INITIATE_URL, params, self.token['auth'])
		

	def mark_read(self, msg):
		print "Marking Msg as Read: "+ msg['messageText']
		params = {'messages': msg['id'], 'read':'1', '_rnr_se':token['rnr_se']}
		print http_post(MSG_MARK_READ_URL, params, self.token['auth'])


	def mark_unread(self, msg):
		print "Marking Msg as UnRead: "+ msg['messageText']
		params = {'messages': msg['id'], 'read':'0', '_rnr_se':token['rnr_se']}
		print http_post(MSG_MARK_READ_URL, params, self.token['auth'])

		
	def delete(self, msg):
		print "Deleting Msg: "+ msg['messageText']
		params = {'messages': msg['id'], 'trash':'1', '_rnr_se':self.token['rnr_se']}
		print http_post(MSG_MARK_READ_URL, params, self.token['auth'])	
		

	def fetch_unread_sms(self, url = SMS_UNREAD_URL):
		return self.fetch_inbox(url = url)


	def fetch_all_sms(self, url = SMS_URL):
		return self.fetch_inbox(url = url)

	def fetch_inbox(self, url = INBOX_URL):
		conn = httplib.HTTPSConnection("www.google.com")
		conn.putrequest("GET", url)
		conn.putheader( "Authorization", "GoogleLogin auth="+self.token['auth'])
		conn.endheaders()
		res = conn.getresponse().read()
		soup = BeautifulSoup(res)
		msg_data = soup.find('json').find(text = True)
		return str(msg_data)
		
	def register_notifiee(self, notifie):
		self.notifiee.append(notifie)
	
	def notify(msg_data):
		for notifie in self.notifiee:
			notifie(msg_data)
		
	def run_server(self):
		while(True):		
			try:
				inbox_raw = self.fetch_unread_sms()
				print inbox_raw
				inbox = jsonpickle.decode(inbox_raw)
				if(inbox['unreadCounts']['unread'] > 0):
					for msg in inbox['messages']:
						msg_data = inbox['messages'][msg]	
						if(not (msg_data['isRead'] or msg_data['isTrash'])):
							self.notify(msg_data)					
			except:
				pass
			time.sleep(1)
	
	
					
			
