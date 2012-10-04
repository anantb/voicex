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
@date: Oct 4, 2012

VoiceX public APIs
'''	
class VoiceX:
	def __init__(self, config=None):
		pass
		
	def set_callback(self, callback):
		pass

	def sms(self, to_number, text):
		print "Sending message [ %s ] to: [%s]." %(text, to_number)


	def mark_read(self, msg):
		print "Marking message [ %s ] as Read."  %(msg['messageText'])


	def mark_unread(self, msg):
		print "Marking message [ %s ] as UnRead."  %(msg['messageText'])


	def delete(self, msg):
		print "Deleting message [ %s ]."  %(msg['messageText'])

	def fetch_unread_sms():
		pass


	def fetch_all_sms(self):
		pass

class Test():
	def __init__(self):		
		self.client = VoiceX()
		self.client.set_callback(callback = self.msg_new)

	def msg_new(self, msg):
		print "Got text [ %s ] from [%s]." %(msg['text'], msg['from'])
		print self.client.mark_read(msg)
		print self.client.sms(msg['from'], "Ack :" + msg['text'])
		print self.client.delete(msg)

def main():	
	Test()



if __name__ == "__main__":
	main()
