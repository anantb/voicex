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
from util import *

'''
@author: anant bhardwaj
@date: Oct 4, 2012

Africa Talking Public APIs
'''	
class AfricaTalking:
	def __init__(self, username, api_key):
		self.username = username
		self.api_key = api_key
	
	def sms(self, to, message,frm='2122', bulkSMSMode=1):
		print "Sending message [ %s ] to: [%s]." %(message, to)
		params = {'to': to, 'message':message, 'username':self.username, 'from':frm, 'bulkSMSMode':bulkSMSMode }
		return http_post(params, self.api_key)
	
	def fetch_inbox(self, last_received_id = 0):
		print "Fetching Inbox."
		params = {'username':self.username,'lastReceivedId':last_received_id}
		return http_get(params, self.api_key)


class Test():
	def __init__(self, username, api_key):		
		self.client = AfricaTalking(username, api_key)
		print self.client.fetch_inbox()
		print self.client.sms(to="254706222092", message="Testing")

def main():	
	Test("voicex", "a87d14779ed780172d0d0f7ab47b6183ca1b17b9c047d887ab2a14fc1288cf28")



if __name__ == "__main__":
	main()
	
	
					
			
