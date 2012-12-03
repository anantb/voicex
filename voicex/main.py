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

import os, sys, re

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "http_handler.settings")


from model_controller import *
from models import *
from transport.voicex import VoiceXTransport
from transport import config
import voicex.tasks
'''
Main Handler Interface

@author: Anant Bhardwaj, Trisha Kothari
@date: Aug 3, 2012
'''

class VoiceX:
	def __init__(self):
		self.mc = ModelController()
		self.v = VoiceXTransport(transport=config.GV, auth= config.GV_VOICEX_AUTH)


	def init_callback(self):
		self.v.set_callback(callback = self.msg_new)


	def show_help(self, msg, phone_num):
		help_text = "Welcome to VoiceX! To register: #register name, To unregister: #unregister name, To post: #post msg, To search: #search query, To follow: #follow name, To unfollow: #unfollow name, To reply: #reply post-id reply-msg, To comment: #comment post-id comment, To view #view post-id, To delete #delete post-id"
		if(not msg):
			pass
		elif('register' in msg):
			help_text = "Help for #register : #register name"
		elif('unregister' in msg):
			help_text = "Help for #unregister : #unregister name"
		elif('post' in msg):
			help_text = "Help for #post : #post msg"
		elif('search' in msg):
			help_text = "Help for #search : #search keywords"
		elif('view' in msg):
			help_text = "Help for #view : #view post-id"
		elif('delete' in msg):
			help_text = "Help for #delete : #delete post-id"
		elif('reply' in msg):
			help_text = "Help for #reply : #reply post-id reply-msg"
		elif('comment' in msg):
			help_text = "Help for #comment : #comment post-id comment"
		elif('follow' in msg):
			help_text = "Help for #follow : #follow name"
		elif('unfollow' in msg):
			help_text = "Help for #unfollow : #unfollow name"
		else:
			pass			
		self.v.sms(phone_num, help_text)

	
	
	def register(self, name, phone_num):	
		if(self.mc.add_account(name , phone_num)):
			self.v.sms(phone_num, 'Account created successfully.')
		else:
			self.v.sms(phone_num, 'Error occurred while creating the account.')
	
	
	def unregister(self, name, phone_num):	
		if(self.mc.delete_account(name , phone_num)):
			self.v.sms(phone_num, 'Account deleted successfully.')
		else:
			self.v.sms(phone_num, 'Error occurred while deleting the account.')
	

	
	def post(self, text, phone_num):				
		post_id = self.mc.insert_post(phone_num, text);
		if(post_id >= 0):		
			self.v.sms(phone_num, 'Msg successfully posted. To view the post, text #view ' + str(post_id))
			self.notify_followers(phone_num, text, post_id)
		else:
			self.v.sms(phone_num, "Error occurred while posting the Msg.")


	def notify_followers(self, phone_num, msg, post_id):
		account = self.mc.find_account(phone_num)
		if(not account):
			return
		follow_list = self.mc.find_following(account)
		text = "From: %s (Post ID: %s): %s" %(account.name, post_id, msg)
		if(len(follow_list)>0):
			recipients = ','.join(follow_list)
			self.v.sms(recipients, text)



	def delete(self, post_id, phone_num):
		if(self.mc.delete_post(post_id)):
			self.v.sms(phone_num, "Post ID:(" + post_id + ") has been successfully deleted!")
		else:
			self.v.sms(phone_num, "Couldn't delete post (ID:" + post_id+")")



	def view(self, post_id, phone_num):	
		post = self.mc.find_post(post_id)
		if(post):
			res = post.post
			posts = Post.objects.filter(reply_to = post, public = True)
			for p in posts:
				res =  res + "[Comment (ID:" + str(p.id) + "): " + p.post + "] "
		else:		
			res = 'No post found with id: ' + post_id
		self.v.sms(phone_num, res)



	def search(self, query, phone_num):
		res = self.mc.search_posts(query)
		if(not res):
			res = 'No matching results found.' 
		self.v.sms(phone_num, res)




	def reply(self, msg_data, phone_num):
		tokens = msg_data.strip().split(" ", 1)
		tokens = filter(lambda x: x!='', map(lambda x: x.strip(), tokens))
		post_id = None
		reply_text = None
		try:
			post_id = str(int(tokens[0]))
			reply_text = tokens[1]
		except:
			self.getHelp(msg_data, phone_num)
			return
			
		try:
			reply_text = tokens[1]
			post = self.mc.find_post(post_id)
			if(post):
				reply_id = str(self.mc.insert_reply(phone_num, reply_text, post))
				if(reply_id > 0):
					self.v.sms(phone_num, 'Your reply to post (ID:' + post_id + ") has been successfully submitted!")
					reply_to  = post.phone
					self.v.sms(reply_to, "New Reply (ID:" +reply_id+") : " + reply_text +".")
			else:
				self.v.sms(phone_num, 'No post found with ID: ' + post_id)
		except:
			self.v.sms(phone_num, 'Error occurred while replying to post (ID:' + post_id+")")



	def comment(self, msg_data, phone_num):
		post_id = None
		comment_text = None
		try:
			post_id = str(int(tokens[0]))
			comment_text = tokens[1]
		except:
			self.getHelp(msg_data, phone_num)
			return
					
		try:			
			post = self.mc.find_post(post_id)
			if(post):
				comment_id = self.mc.insert_reply(phone_num, comment_text, post, public = True)
				if(comment_id > 0):
					self.v.sms(phone_num, 'Your comment to post (ID:' + post_id + ") has been successfully submitted!")
					reply_to  = post.phone
					self.v.sms(reply_to, "New comment to post (ID:" +post_id+"): " + comment_text +".")
			else:
				self.v.sms(phone_num, 'No post found with ID: ' + post_id)
		except:
			self.v.sms(phone_num, 'Error occurred while adding comment to post (ID:' + post_id+")")


	def follow(self, name, phone_num):
		if(self.mc.add_following(name, phone_num)):
			self.v.sms(phone_num, 'You are now following %s.' %(name))
		else:
			self.v.sms(phone_num, 'Error occurred while adding the follow list for %s.' %(name))
	
	
	def unfollow(self, name, phone_num):
		if(self.mc.delete_following(name, phone_num)):
			self.v.sms(phone_num, 'You are now not following %s.' %(name))
		else:
			self.v.sms(phone_num, 'Error occurred while removing the follow list for %s.' %(name))


	def parse(self, msg, phone_num):
		try:
			msg_data = (msg.strip()).split(" ", 1)
			msg_data = map(lambda x: x.strip(), msg_data)
			if (msg_data[0] == "#register"):
				self.register(msg_data[1], phone_num)
			elif(msg_data[0] == "#unregister"):
				self.unregister(msg_data[1], phone_num)
			elif(msg_data[0] == "#post"):
				self.post(msg_data[1], phone_num)
			elif(msg_data[0] == "#view"):
				self.view(msg_data[1], phone_num)
			elif(msg_data[0] ==  "#search"):
				self.search(msg_data[1], phone_num)
			elif(msg_data[0] == "#delete"):
				self.delete(msg_data[1], phone_num)
			elif(msg_data[0] == "#reply"):
				self.reply(msg_data[1], phone_num)
			elif(msg_data[0] == "#comment"):
				self.comment(msg_data[1], phone_num)
			elif(msg_data[0] == "#follow"):
				self.follow(msg_data[1], phone_num)
			elif(msg_data[0] == "#unfollow"):
				self.unfollow(msg_data[1], phone_num)
			elif(msg_data[0] == "#help"):
				self.show_help(msg_data[1], phone_num)
			else:
				self.show_help(msg, phone_num)
		except Exception, e:
			print "parse: ", e
			self.show_help(msg, phone_num)



	def handle(self, msg_data):
		msg = msg_data['text'].strip()
		phone_num = msg_data['from'].strip()
		if(not msg):
			self.getHelp(msg, phone_num)
		else:
			self.parse(msg, phone_num)
	
	
	def msg_new(self, msg):
		self.handle(msg)


def main():
	v = VoiceX()
	v.init_callback()


if __name__ == "__main__":
	main()

