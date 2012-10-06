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

import sys, re
from model_controller import *
from transport import voicex
'''
Main Handler Interface

@author: Anant Bhardwaj, Trisha Kothari
@date: Aug 3, 2012
'''

class VoiceXEngine:
	def __init__(self):
		self.mc = ModelController()
		self.v = voicex.VoiceX()
		
	def init_callback(self):
		self.v.set_callback(callback = self.msg_new)
	
	def show_help(self, msg, phone_num):
		help_text = "Welcome to VoiceX! To post : #post msg, To search: #search keywords, To follow: #follow tags, To reply: #reply post-id reply-msg, To comment: #comment post-id comment, To view #view post-id, To delete #delete post-id, To tag #tag post-id tag-id."
		if(not msg):
			pass
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
			help_text = "Help for #follow : #follow keywords"
		elif('tag' in msg):
			help_text = "Help for #tag : #tag post-id tag-id"
		else:
			pass			
		self.v.sms(phone_num, help_text)
		
	

	def post(self, text, phone_num):				
		post_id = self.mc.insert_post(phone_num, text);
		if(post_id >= 0):		
			self.v.sms(phone_num, 'Msg successfully posted. To view the post, text #view ' + str(post_id))
			tags = re.findall('\w+', text)
			if(tags):
				self.notify_followers(tags, "New post (ID:" + str(post_id) + "): "+ text +".", post_id)
		else:
			self.v.sms(phone_num, "Error occured while posting the Msg.")
		
	
		
	def notify_followers(self, tags, msg, post_id):
		follow_list = self.mc.find_follow_list(tags)
		if(len(follow_list)>0):
			recipients = ','.join(follow_list)
			self.v.sms(recipients, msg)


	def delete(self, post_id, phone_num):
		if(self.mc.delete_post(post_id)):
			self.v.sms(phone_num, "Post ID:(" + post_id + ") has been successfully deleted!")
		else:
			self.v.sms(phone_num, "Couldn't delete post (ID:" + post_id+")")
		
				
	def view(self, post_id, phone_num):	
		post = self.mc.find_post(post_id)
		if(post):
			res = post.post
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
		post_id = tokens[0]
		try:
			reply_post = tokens[1]
			post = self.mc.find_post(post_id)
			if(post):
				reply_id = self.mc.insert_reply(phone_num, reply_post, post)
				if(reply_id > 0):
					self.v.sms(phone_num, 'Your reply to post (ID:' + post_id + ") has been sucessfully submitted!")
					reply_to  = post.phone
					self.v.sms(reply_to, "New Reply (ID:" +str(reply_id)+") : " + reply_post +".")
			else:
				self.v.sms(phone_num, 'No post found with ID: ' + post_id)
		except:
			self.v.sms(phone_num, 'Error occured while replying to post (ID:' + post_id+")")
	
	def comment(self, msg_data, phone_num):
		tokens = msg_data.strip().split(" ", 1)
		tokens = filter(lambda x: x!='', map(lambda x: x.strip(), tokens))
		post_id = tokens[0]
		try:
			comment_text = tokens[1]
			post = self.mc.find_post(post_id)
			if(post):
				comment_id = self.mc.insert_reply(phone_num, comment_text, post, to_all = True)
				if(comment_id > 0):
					self.v.sms(phone_num, 'Your comment to post (ID:' + post_id + ") has been sucessfully submitted!")
					reply_to  = post.phone
					self.v.sms(reply_to, "New comment to post (ID:" +post_id+"): " + comment_text +".")
					tags = re.findall('\w+', post.post)
					if(tags):
						self.notify_followers(tags, "New comment to post (ID:"+ post_id+"): "+ comment_text +".", post_id)
			else:
				self.v.sms(phone_num, 'No post found with ID: ' + post_id)
		except:
			self.v.sms(phone_num, 'Error occured while adding comment to post (ID:' + post_id+")")
		
		
	def follow(self, msg, phone_num):
		tags = re.findall('\w+', msg)		
		if(self.mc.update_follow_tag(tags, phone_num)):
			self.v.sms(phone_num, 'Follow tags added successfully.')
		else:
			self.v.sms(phone_num, 'Error occured while adding the follow tags.')
		
	
	def parse(self, msg, phone_num):
		try:
			msg_data = (msg.strip()).split(" ", 1)
			msg_data = map(lambda x: x.strip(), msg_data)
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
			elif(msg_data[0] == "#comment"):
				self.comment(msg_data[1], phone_num)
			elif(msg_data[0] == "#follow"):
				self.follow(msg_data[1], phone_num)
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
	t= VoiceXEngine()
	t.init_callback()

if __name__ == "__main__":
    main()
	
	

