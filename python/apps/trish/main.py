"""
Copyright (c) 2012 Trisha Kothari, Anant Bhardwaj

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

import os, sys, re
sys.path.append(os.getcwd()+"/../..")
from model_controller import *
from transport.voicex import *


'''
Main Handler Interface

@author: Trisha Kothari (Original Author)
@date: Aug 3, 2012

@author: Anant Bhardwaj (Code cleanup and bug fixes)
'''

class Trish:
	def __init__(self, email, password):		
		self.v = VoiceX(email, password, server=True, callback = self.msg_new)
		self.mc = ModelController()
		print "initialized"

	def getHelp(self, msg_data):
		phone_num = msg_data['phoneNumber']
		help_text = "Welcome to Trish! To post : #post, To search: #search, To follow: #follow, To reply: #reply, To view #view, To delete #delete"
		self.v.sms(phone_num, help_text)

	def post(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		message = msg[msg.find("#post") + len("#post") : ].strip()
		zipcode = re.search("\d{5}", message)
		if(zipcode == None):
			zip_code = '00000'
		else:
			zip_code = str(zipcode.group())				
		post_id = self.mc.insert_post(phone_num, message, zip_code);
		if(post_id >= 0):		
			self.v.sms(phone_num, 'Msg successfully posted. To view the post, text #view ' + str(post_id))
			self.notify_followers(message, post_id)
		else:
			self.v.sms(phone_num, "Error occured while posting the Msg.")
		
	
		
	def notify_followers(self, message, post_id):
		tokens = re.split(' ', message)
		if(not tokens):
			return
		to_send = []
		for token in tokens:
			print 'token: ' + token
			res = self.mc.search_posts(token)
			if(not res):
				continue
			sub_list = self.mc.find_subscription_list(token)
			if(not sub_list):
				continue
			to_send.append(sub_list)
		if(len(to_send)>0):
			recepients = ','.join(to_send)
			to_send = re.split(',', recepients)
			to_send = filter(lambda x: x!='' and x!=',', to_send)
			to_send = list(set(to_send))
			recepients = ','.join(to_send)
			self.v.sms(recepients, "New Post: " + message +", Post ID: " + str(post_id)+".")	


	def delete(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		post_id = msg.split(" ")[1]
		if(self.mc.delete_post(str(post_id))):
			self.v.sms(phone_num, "Post #" + post_id+ " has been successfully deleted!")
		else:
			self.v.sms(phone_num, "Couldn't delete post #" + post_id)
		
				
	def view(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		post_id = msg[msg.find("#view") + len("#view") : ].strip()
		post = self.mc.find_post(int(post_id))
		if(post):
			res = post[1]
		else:		
			res = 'No post found with id: .' + post_id
		self.v.sms(phone_num, res)

	def search(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		search_params = msg[msg.find("#search") + len("#search") : ].strip()
		res = self.mc.search_posts(search_params)
		if(not res):
			res = 'No matching results found.' 
		self.v.sms(phone_num, res)

	def reply(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		message_array = msg.split(" ")
		post_id = message_array[1]
		blurb_text = msg[msg.find(str(post_id)) + len(str(post_id)) : ].strip()		
		post = self.mc.find_post(int(post_id))
		if(post):
			self.v.sms(phone_num, 'Your reply to post #' + post_id + " has been sucessfully submitted!")
			reply_to  = post[0]
			self.v.sms(reply_to, "New reply from: " + phone_num + " -- " + str(blurb_text))
		else:
			self.v.sms(phone_num, 'Error occured while replying to post #' + post_id)
		
	def follow(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		tags = msg[msg.find("#follow") + len("#follow") : ].strip()
		tags = re.findall('\w+', tags)
		tags = map(lambda x: x.strip(), tags)
		tags = filter(lambda x: x!='' and x!=',', tags)
		for tag in tags:
			x = self.mc.update_follow_tag(tag, phone_num)
		self.v.sms(phone_num, 'Follow tags added successfully')


	def handle(self, msg_data):
		msg = msg_data['messageText']
		if "#post" in msg:
			self.post(msg_data)
		elif "#help" in msg:
			self.getHelp(msg_data)
		elif "#delete" in msg:
			self.delete(msg_data)
		elif "#view" in msg:
			self.view(msg_data)
		elif "#search" in msg:
			self.search (msg_data)
		elif "#reply" in msg:
			self.reply(msg_data)
		elif "#follow" in msg:
			self.follow(msg_data)
		else:
			self.getHelp(msg_data)
	
	
	def msg_new(self, msg):
		self.handle(msg)
		self.v.mark_read(msg)

def main():	
	Trish('voicex.git@gmail.com', 'VoiceX@Git')

if __name__ == "__main__":
    main()
	
	

