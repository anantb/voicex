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

import os, sys, re, logging

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "http_handler.settings")


from model_controller import *
from models import *
from transport.voicex import VoiceXTransport
from transport import config
#import voicex.tasks

logger = logging.getLogger(__name__)

'''
Main Handler Interface

@author: Anant Bhardwaj, Trisha Kothari
@date: Aug 3, 2012
'''

class VoiceX:
	def __init__(self, auth):
		logger.debug('__init__')
		self.mc = ModelController()
		self.v = VoiceXTransport(auth = auth)

	
	# only for testing (polling mode)
	def init_callback(self):
		logger.debug('init_callback')
		self.v.set_callback(callback = self.msg_new)


	def show_help(self, msg, phone_num):
		logger.debug('show_help')
		help_text = "Welcome to VoiceX! Commands: register name, unregister name, post msg, view post-id, delete post-id, search query, reply post-id msg, follow @name/#tag, unfollow @name/#tag"
		if(not msg):
			pass
		elif('register' in msg):
			help_text = "Help for register : register name. Example: register voicex"
		elif('unregister' in msg):
			help_text = "Help for unregister : unregister name. Example: unregister voicex"
		elif('post' in msg):
			help_text = "Help for post : post message. Example (simple post): post hello world. Example (tagged post): post voicex is free #voicex. Example (anonymous post): post voicex is free #anon"
		elif('search' in msg):
			help_text = "Help for search : search search-keywords. Example: search kenya election"
		elif('view' in msg):
			help_text = "Help for view : view post-id. Example: view 1"
		elif('delete' in msg):
			help_text = "Help for delete : delete post-id. Example: delete 1"
		elif('reply' in msg):
			help_text = "Help for reply : reply post-id reply-msg. Example (private reply): reply 1 welcome to voicex. Example (public reply): reply 1 welcome to voicex #public. Example (anonymous reply): reply 1 welcome to voicex #anon"
		elif('follow' in msg):
			help_text = "Help for follow : follow @name/#tag. Example: follow @voicex or follow #election"
		elif('unfollow' in msg):
			help_text = "Help for unfollow : unfollow @name/#tag. Example: unfollow @voicex or unfollow #election."
		else:
			pass			
		self.v.sms(phone_num, help_text)

	
	
	def register(self, name, phone_num):
		logger.debug('register')
		res = self.mc.add_account(name , phone_num)
		if(res['status']):
			self.v.sms(phone_num, 'Successfully registered %s with %s.' %(name, phone_num))
		else:
			self.v.sms(phone_num, res['code'])
	
	
	def unregister(self, name, phone_num):
		logger.debug('unregister')
		res = self.mc.delete_account(name , phone_num)	
		if(res['status']):
			self.v.sms(phone_num, 'Unregistered %s' %(name))
		else:
			self.v.sms(phone_num, res['code'])
	

	
	def post(self, text, phone_num):
		logger.debug('post')				
		res = self.mc.insert_post(phone_num, text);
		if(res['status']):
			post_id = res['val']	
			self.v.sms(phone_num, 'Msg successfully posted. To view the post, text -- view %s' %(str(post_id)))
			self.notify_followers(phone_num, text, post_id)
		else:
			self.v.sms(phone_num, res['code'])


	def notify_followers(self, phone_num, msg, post_id):
		logger.debug('notify_followers')
		tags = [tag.strip().lower() for tag in msg.split() if tag.startswith("#")]
		res_find = self.mc.find_account(phone_num)
		account = 'anonymous'
		if(res_find['status'] and ('#anon' not in tags)):
			account = res_find['val'].name
			tags.append('@'+account)
		
		res_following = self.mc.find_following(tags)
		text = "From: @%s (Post ID: %s): %s" %(account, post_id, msg)
		if(res_following['status']):
			follow_list = res_following['val']
			if(len(follow_list) == 0 ):
				return
			recipients = ','.join(follow_list)
			self.v.sms(recipients, text)
		else:
			self.v.sms(phone_num, res['code'])



	def delete(self, post_id, phone_num):
		logger.debug('delete')
		res = self.mc.delete_post(post_id)
		if(res['status']):
			self.v.sms(phone_num, "Post ID:(%s) has been successfully deleted!" %(post_id))
		else:
			self.v.sms(phone_num, res['code'])



	def view(self, post_id, phone_num):
		logger.debug('view')
		res = self.mc.find_post(post_id)
		if(res['status']):
			post = res['val']
			out = post.post
			posts = Post.objects.filter(reply_to = post, public = True)
			for p in posts:
				out =  out + "[Comment (ID:%s): %s]" %(str(p.id), p.post)
			self.v.sms(phone_num, out)
		else:		
			self.v.sms(phone_num, res['code'])
		



	def search(self, query, phone_num):
		logger.debug('search')
		res = self.mc.search_posts(query)
		if(res['status']):
			self.v.sms(phone_num, res['val'])
		else:
			self.v.sms(phone_num, res['code'])
		




	def reply(self, msg_data, phone_num):
		logger.debug('reply')
		tokens = msg_data.strip().split(" ", 1)
		tokens = filter(lambda x: x!='', map(lambda x: x.strip(), tokens))
		post_id = None
		reply_text = None
		try:
			post_id = str(int(tokens[0]))
			reply_text = tokens[1]
		except:
			self.show_help('reply', phone_num)
			return
		account = 'anonymous'
		tags = [tag.strip().lower() for tag in reply_text.split() if tag.startswith("#")]
		res_find_acc = self.mc.find_account(phone_num)
		if(res_find_acc['status'] and ('#anon' not in tags)):
			account = res_find_acc['val'].name
		reply_text = tokens[1]
		res_find = self.mc.find_post(post_id)
		if(res_find['status']):
			post = res_find['val']
			res_insert = {'status': False}
			if('#public' in tags):
				res_insert = self.mc.insert_reply(phone_num, reply_text, post, public=True)
			else:
				res_insert = self.mc.insert_reply(phone_num, reply_text, post)
			if(res_insert['status']):
				reply_id = str(res_insert['val'])
				self.v.sms(phone_num, "Your reply to post (ID:%s) has been successfully submitted!" %(post_id))
				reply_to  = post.phone
				self.v.sms(reply_to, "[Reply(ID:%s, From: @%s) to Post(ID:%s)] - %s" %(str(reply_id), account, str(post_id), reply_text))
			else:
				self.v.sms(phone_num, res_insert['code'])
		else:
			self.v.sms(phone_num, res_find['code'])
	


	def follow(self, tag, phone_num):
		logger.debug('follow')
		if(tag[0] not in ['#', '@']):
			self.v.sms(phone_num, "Invalid tag: '%s'. Valid tags are either hash-tags (start with '#'), or an account name (start with'@')." %(tag))
			return
		res = self.mc.add_following(tag.strip().lower(), phone_num)
		if(res['status']):
			self.v.sms(phone_num, 'You are now following %s.' %(tag))
		else:
			self.v.sms(phone_num, res['code'])
	
	
	def unfollow(self, name, phone_num):
		logger.debug('unfollow')
		res = self.mc.delete_following(name.strip().lower(), phone_num)
		if(res['status']):
			self.v.sms(phone_num, 'You are now not following %s.' %(name))
		else:
			self.v.sms(phone_num, res['code'])


	def parse(self, msg, phone_num):
		logger.debug('parse')
		try:
			msg_data = (msg.strip()).split(" ", 1)
			msg_data = map(lambda x: x.strip(), msg_data)
			cmd = msg_data[0].lower()
			text = None
			try:
				text = msg_data[1]
			except:
				pass
			
			if(not text):
				self.show_help(msg_data[0], phone_num)
				return
			
			if (cmd == "register"):
				self.register(text, phone_num)
			elif(cmd == "unregister"):
				self.unregister(text, phone_num)
			elif(cmd == "post"):
				self.post(text, phone_num)
			elif(cmd == "view"):
				self.view(text, phone_num)
			elif(cmd ==  "search"):
				self.search(text, phone_num)
			elif(cmd == "delete"):
				self.delete(text, phone_num)
			elif(cmd == "reply"):
				self.reply(text, phone_num)
			elif(cmd == "follow"):
				self.follow(text, phone_num)
			elif(cmd == "unfollow"):
				self.unfollow(text, phone_num)
			elif(cmd == "help"):
				try:
					self.show_help(msg_data[1], phone_num)
				except:
					self.show_help(None, phone_num)
			else:
				self.v.sms(phone_num, "Unknown command: '%s'. Text 'help' to get the list of commands." %s(cmd))
		except Exception, e:
			logger.exception('parse')



	def handle(self, msg_data):
		logger.debug('handle')
		msg = msg_data['text'].strip()
		phone_num = msg_data['from'].strip()
		logger.debug('From: %s, Text: %s' %(phone_num, msg))
		if(not msg):
			self.show_help(None, phone_num)
		else:
			self.parse(msg, phone_num)
	
	
	def msg_new(self, msg):
		logger.debug('msg_new')
		self.handle(msg)


def main():
	v = VoiceX(auth = config.GV_VOICEX_AUTH)
	v.init_callback()


if __name__ == "__main__":
	main()

