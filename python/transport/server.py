from voicex import *
from login import *
import jsonpickle

notifiee = []
def register_notifiee(n):
	notifiee.append(n)


def start_server():
	token = login('voicex.git@gmail.com', 'VoiceX@Git')
	while(True):
		msg_data = fetch_unread_sms(token)
		print msg_data
		messages = jsonpickle.decode(msg_data)
		if(messages['unreadCounts']['sms'] > 0):		
			for n in notifiee:
				n(messages['messages'])
		time.sleep(1)
		
	
def main():	
	start_server()
	
def msg_new(msg_data):
	token = login('voicex.git@gmail.com', 'VoiceX@Git')
	for msg in msg_data:
		text = msg_data[msg]['messageText']
		phone_number = msg_data[msg]['phoneNumber']
		print ('got %s from %s' % (text, phone_number))
		sms(phone_number, "got it", token)


register_notifiee(msg_new)

if __name__ == "__main__":
    main()
