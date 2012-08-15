"""
Copyright (c) 2012 Anant Bhardwaj, Trisha Kothari

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

import os, sys
sys.path.append(os.getcwd()+"/../..")
from transport.voicex import VoiceX
from main import *
import jsonpickle

'''
@author: anant bhardwaj
@date: Aug 3, 2012

hackday server
'''

notifiee = []
v = None
jms = None
def register_notifiee(n):
	notifiee.append(n)


def start_server():
	global v
	global jms
	v = VoiceX('voicex.git@gmail.com', 'VoiceX@Git')
	jms = JMS(v)
	while(True):
		try:
			inbox_raw = v.fetch_unread_sms()
			print inbox_raw
			inbox = jsonpickle.decode(inbox_raw)
			if(inbox['unreadCounts']['unread'] > 0):
				for msg in inbox['messages']:
					msg_data = inbox['messages'][msg]	
					if(not (msg_data['isRead'] or msg_data['isTrash'])):		
						for n in notifiee:
							n(msg_data)
		except:
			pass						
		time.sleep(1)
		
	
def main():	
	start_server()
	
def msg_new(msg):
	global v
	global jms
	jms.handle(msg)
	v.mark_read(msg)	
	v.delete(msg)


register_notifiee(msg_new)

if __name__ == "__main__":
    main()
