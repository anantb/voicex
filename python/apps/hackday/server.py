import os, sys
sys.path.append(os.getcwd()+"/../..")
from transport.voicex import *
from transport.login import *
from main import *
import jsonpickle

'''
@author: anant bhardwaj
@date: Aug 3, 2012

hackday server
'''

notifiee = []
token = None
jms = None
def register_notifiee(n):
	notifiee.append(n)


def start_server():
	global token
	global jms
	token = login('voicex.git@gmail.com', 'VoiceX@Git')
	jms = JMS(token)
	while(True):
		try:
			inbox_raw = fetch_unread_sms(token)
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
	global token
	global jms
	jms.handle(msg)
	mark_read(msg, token)	
	delete(msg, token)


register_notifiee(msg_new)

if __name__ == "__main__":
    main()
