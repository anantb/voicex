from transport.voicex import *
from transport.login import *
from apps.hackday.main import *
import jsonpickle

'''
@author: anant bhardwaj
@date: Aug 3, 2012

voicex server
'''

notifiee = []
token = None
def register_notifiee(n):
	notifiee.append(n)


def start_server():
	global token
	token = login('voicex.git@gmail.com', 'VoiceX@Git')
	while(True):
		inbox_raw = fetch_unread_sms(token)
		print inbox_raw
		inbox = jsonpickle.decode(inbox_raw)
		if(inbox['unreadCounts']['unread'] > 0):
			for msg in inbox['messages']:
				msg_data = inbox['messages'][msg]	
				if(not (msg_data['isRead'] or msg_data['isTrash'])):		
					for n in notifiee:
						n(msg_data)
		time.sleep(1)
		
	
def main():	
	start_server()
	
def msg_new(msg):
	global token
	jms = JMS()
	jms.getType(msg['messageText'])
	mark_read(msg, token)	
	delete(msg, token)


register_notifiee(msg_new)

if __name__ == "__main__":
    main()
