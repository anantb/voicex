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
from stemming.porter2 import stem


'''
Main Handler Interface

@author: Trisha Kothari, Anant Bhardwaj
@date: Aug 3, 2012
'''

class Trish:
	def __init__(self, email, password):		
		self.mc = ModelController()
		print "initialized"
		self.v = VoiceX(email, password)
		self.v.start_server(self.msg_new)

	def show_help(self, msg, phone_num):
		help_text = "Welcome to Trish! To post : #post <msg>, To search: #search <keywords>, To follow: #follow <post-id>, To reply: #reply <post-id> <reply msg>, To view #view <post-id>, To delete #delete <post-id>"
		if(not msg):
			pass
		elif('post' in msg):
			help_text = "Help for #post : #post <msg>"
		elif('search' in msg):
			help_text = "Help for #search : #search <keywords>"
		elif('view' in msg):
			help_text = "Help for #view : #view <post-id>"
		elif('delete' in msg):
			help_text = "Help for #delete : #delete <post-id>"
		elif('reply' in msg):
			help_text = "Help for #reply : #reply <post-id> <reply msg>"
		elif('follow' in msg):
			help_text = "Help for #follow : #follow <keywords>"
		else:
			pass			
		self.v.sms(phone_num, help_text)

	def post(self, msg_data, phone_num):
		zipcode = re.search("\d{5}", msg_data)
		if(zipcode == None):
			zip_code = '00000'
		else:
			zip_code = str(zipcode.group())				
		post_id = self.mc.insert_post(phone_num, msg_data, zip_code);
		if(post_id >= 0):		
			self.v.sms(phone_num, 'Msg successfully posted. To view the post, text #view ' + str(post_id))
			self.notify_followers(msg_data, str(post_id))
		else:
			self.v.sms(phone_num, "Error occured while posting the Msg.")
		
	
		
	def notify_followers(self, msg_data, post_id):
		tokens = re.findall('\w+', msg_data)
		if(not tokens):
			return
		to_send = []
		for token in tokens:
			print 'token: ' + token
			sub_list = self.mc.find_subscription_list(stem(token.lower()))
			if(not sub_list):
				continue
			to_send.append(sub_list)
		if(len(to_send)>0):
			recepients = ','.join(to_send)
			to_send = re.split(',', recepients)
			to_send = filter(lambda x: x!='' and x!=',', to_send)
			to_send = list(set(to_send))
			recepients = ','.join(to_send)
			self.v.sms(recepients, "New Post: " + msg_data +", Post ID: " + post_id +".")	


	def delete(self, msg_data, phone_num):
		if(self.mc.delete_post(msg_data)):
			self.v.sms(phone_num, "Post #" + msg_data + " has been successfully deleted!")
		else:
			self.v.sms(phone_num, "Couldn't delete post #" + msg_data)
		
				
	def view(self, msg_data, phone_num):	
		post = self.mc.find_post(msg_data)
		if(post):
			res = post[1]
		else:		
			res = 'No post found with id: ' + msg_data
		self.v.sms(phone_num, res)

	def search(self, msg_data, phone_num):
		res = self.mc.search_posts(msg_data)
		if(not res):
			res = 'No matching results found.' 
		self.v.sms(phone_num, res)

	def reply(self, msg_data, phone_num):
		tokens = msg_data.strip().split(" ", 1)
		tokens = map(lambda x: x.strip(), tokens)
		tokens = filter(lambda x: x!='', tokens)
		post_id = tokens[0]
		try:
			blurb_text = tokens[1]
			post = self.mc.find_post(post_id)
			if(post):
				self.v.sms(phone_num, 'Your reply to post #' + post_id + " has been sucessfully submitted!")
				reply_to  = post[0]
				self.v.sms(reply_to, "New reply from: " + phone_num + " -- " + blurb_text)
			else:
				self.v.sms(phone_num, 'Error occured while replying to post #' + post_id)
		except:
			self.v.sms(phone_num, 'Error occured while replying to post #' + post_id)
		
		
	def follow(self, msg_data, phone_num):
		tags = re.findall('\w+', msg_data)
		tags = map(lambda x: x.strip(), tags)
		tags = filter(lambda x: x!='' and x!=',', tags)
		tags = map(lambda x: stem(x.lower()), tags)
		for tag in tags:
			x = self.mc.update_follow_tag(tag, phone_num)
		self.v.sms(phone_num, 'Follow tags added successfully')
		
	
	def parse(self, msg, phone_num):
		msg_data = msg.strip().split(" ", 1)
		msg_data = map(lambda x: x.strip(), msg_data)
		try:
			if (msg_data[0] == "#post"):
				self.post(msg_data[1], phone_num)
			elif(msg_data[0] == "#view"):
				self.view(msg_data[1], phone_num)
			elif(msg_data[0] ==  "#search"):
				self.search(msg_data[1], phone_num)
			elif(msg_data[0] == "#delete"):
				self.delete(msg_data[1], phone_num)
			elif(msg_data[0] == "#reply"):
				self.reply(msg_data[1], phone_num)
			elif(msg_data[0] == "#follow"):
				self.follow(msg_data[1], phone_num)
			elif(msg_data[0] == "#help"):
				self.show_help(msg_data[1], phone_num)
			else:
				self.show_help(msg, phone_num)
		except:
			self.show_help(msg, phone_num)

	def handle(self, msg_data):
		msg = msg_data['messageText'].strip()
		phone_num = msg_data['phoneNumber'].strip()
		if(not msg):
			self.getHelp(msg, phone_num)
		else:
			self.parse(msg, phone_num)
	
	
	def msg_new(self, msg):
		self.handle(msg)
		self.v.mark_read(msg)

def main():	
	Trish('voicex.git@gmail.com', 'VoiceX@Git')

if __name__ == "__main__":
    main()
	
	

