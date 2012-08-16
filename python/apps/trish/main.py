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
		if len(message) == 0:
			self.v.sms(phone_num, "Text #post msg")
			return
		zipcode = re.search("\d{5}", message)
		if(zipcode == None):
			zip_code = '00000'
		else:
			zip_code = str(zipcode.group())		
				
		post_id = self.mc.insert(phone_num, message, zip_code);		
		self.v.sms(phone_num, 'Msg successfully posted. To view the post, text #view ' + str(post_id))
		self.notify_followers(message, post_id)
		
	def notify_followers(self, message, post_id):
		tokens = re.split(' ', message)
		if(not tokens):
			return
		to_send = []
		for token in tokens:
			print 'token: ' + token
			res = self.mc.search(token)
			if(not res):
				continue
			sub_list = self.mc.get_subscription(token)
			if(not sub_list):
				continue
			to_send.append(sub_list)
		if(len(to_send)>0):
			recepients = ','.join(to_send)
			to_send = re.split(',', to_send)
			to_send = filter(lambda x: x!='' and x!=',', to_send)
			to_send = list(set(to_send))
			recepients = ','.join(to_send)
			self.v.sms(recepients, "New Post: " + message +", Post ID: " + str(post_id)+".")	


	def delete(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		message_array = msg.split(" ")
		print message_array
		if len(message_array) == 1:
			self.v.sms(phone_num, "To delete a post text #delete <Post ID>")
			return
		post_id = message_array[1]
		self.mc.delete(str(post_id))
		self.v.sms(phone_num, "Post #" + post_id+ " has been successfully deleted!")
		
				
	def view(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		post_id = msg[msg.find("#view") + len("#view") : ].strip()
		if len(post_id) == 0:
			self.v.sms(phone_num, "To view a post text #view <Post ID>")
			return
		blurb = self.mc.getPostFromId(int(post_id))
		self.v.sms(phone_num, blurb)

	def search(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		search_params = msg[msg.find("#search") + len("#search") : ].strip()
		if len(search_params) == 0:
			help_text = "Text #search keywords"
			self.v.sms(phone_num, help_text)
			return
		res = self.mc.search(search_params)
		if(not res):
			res = 'No matching results found' 
		self.v.sms(phone_num, res)

	def reply(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		message = msg[msg.find("#reply") + len("#reply") : ].strip()
		if (len(message) == 0):
			help_text = "Text #reply <Post ID> <msg>"
			self.v.sms(phone_num, help_text)
			return
		message_array = msg.split(" ")
		print message_array
		post_id = message_array[1]
		blurb_text = msg[msg.find(str(post_id)) + len(str(post_id)) : ].strip()
		print "post id obtained is:", post_id, "with msg", str(blurb_text)
		self.v.sms(phone_num, 'Your reply to post #' + post_id + " has been sucessfully sumbitted!")
		return_no = self.mc.reply(int(post_id))
		print return_no
		self.v.sms(return_no, "New reply from: " + phone_num + " -- " + str(blurb_text))
		return
		
	def follow(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		keywords = msg[msg.find("#follow") + len("#follow") : ].strip()
		keywords = re.split('\w+', keywords)
		print keywords
		for keyword in keywords:
			x = self.mc.follow(keyword, phone_num)
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
	
	

