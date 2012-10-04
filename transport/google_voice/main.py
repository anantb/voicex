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

import json
from constants import *
from login import *
from util import *
from bs4 import BeautifulSoup
from gv_poller import GoogleVoicePoller

'''
@author: anant bhardwaj
@date: Aug 3, 2012

Google Voice public APIs
'''	
class GoogleVoice:
	def __init__(self, email, password, d = True):
		self.token = login(email, password)
		self.d = d
		
	def start_poll(self, callback):		
		self.poller = GoogleVoicePoller(self, callback, d = self.d)
		self.poller.daemon = True
		self.poller.start()
		self.poller.join(1000)
	
	def sms(self, to_number, text):
		print "Sending message [ %s ] to: [%s]." %(text, to_number)
		params = {'phoneNumber': to_number, 'text':text, '_rnr_se':self.token['rnr_se']}
		return http_post(SMS_SEND_URL, params, self.token['auth'])
		

	def call(self, forwardingNumber, outgoingNumber):
		print "Initiating call to: "+outgoingNumber + ", through: " + forwardingNumber
		params = {'forwardingNumber': forwardingNumber, 
				  'outgoingNumber':outgoingNumber, 
				  'phoneType':'1',
				  'subscriberNumber':'undefined',
				  'remember' : '0',
				  '_rnr_se':token['rnr_se']}
		return http_post(CALL_INITIATE_URL, params, self.token['auth'])
		

	def mark_read(self, msg):
		print "Marking message [ %s ] as Read."  %(msg['messageText'])
		params = {'messages': msg['id'], 'read':'1', '_rnr_se':self.token['rnr_se']}
		return http_post(MSG_MARK_READ_URL, params, self.token['auth'])


	def mark_unread(self, msg):
		print "Marking message [ %s ] as UnRead."  %(msg['messageText'])
		params = {'messages': msg['id'], 'read':'0', '_rnr_se':self.token['rnr_se']}
		return http_post(MSG_MARK_READ_URL, params, self.token['auth'])

		
	def delete(self, msg):
		print "Deleting message [ %s ]."  %(msg['messageText'])
		params = {'messages': msg['id'], 'trash':'1', '_rnr_se':self.token['rnr_se']}
		return http_post(MSG_DELETE_URL, params, self.token['auth'])	
		

	def fetch_unread_sms(self, url = SMS_UNREAD_URL):
		return self.fetch_inbox(url = url)


	def fetch_all_sms(self, url = SMS_URL):
		return self.fetch_inbox(url = url)

	def fetch_inbox(self, url = INBOX_URL):
		conn = httplib.HTTPSConnection("www.google.com")
		conn.putrequest("GET", url)
		conn.putheader( "Authorization", "GoogleLogin auth="+self.token['auth'])
		conn.endheaders()
		page = conn.getresponse().read()
		soup = BeautifulSoup(page)
		meta_data = soup.find('json').find(text = True).strip()
		print meta_data
		return str(meta_data), page
		


class Test():
	def __init__(self, email, password):		
		self.client = GoogleVoice(email, password, d = False)
		self.client.start_poll(callback = self.msg_new)
		
	def msg_new(self, msg):
		print "Got text [ %s ] from [%s]." %(msg['messageText'], msg['phoneNumber'])
		print self.client.mark_read(msg)
		print self.client.sms(msg['phoneNumber'], "Ack :" + msg['messageText'])
		print self.client.delete(msg)

def main():	
	Test('voicex.git@gmail.com', 'VoiceX@Git')



if __name__ == "__main__":
	main()
	
	
					
			
