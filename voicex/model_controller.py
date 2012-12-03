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
from stemming.porter2 import stem
from utils import *
from models import *

'''
Application Model Controller

@author: Anant Bhardwaj, Trisha Kothari
@date: Aug 3, 2012
'''

class ModelController:
	def __init__(self):
		pass
	
	
	
	def add_account(self, name, phone):
		name=name.lower().strip()
		phone = phone.strip()
		try:
			acc = Account.objects.get(name = name, phone)
			return True
		except Account.DoesNotExist:
			try:
				acc = Account(name = name, phone = phone)
				acc.save()
				return True
			except:
				return False
		except Exception, e:
			print "insert_post: ", e
			return False
	
	
	def delete_account(self, name, phone):
		name=name.lower().strip()
		phone = phone.strip()
		try:
			acc = Account.objects.get(name = name, phone = phone)
			acc.delete()
			return True
		except Account.DoesNotExist:
			return False
		except Exception, e:
			print "insert_post: ", e
			return False
			
	
	def find_account(self, phone):
		try:
			acc = Account.objects.get(phone = phone)
			return acc
		except Exception, e:
			print "find_post: ", e
			return None
	
	
	def find_post(self, post_id):
		try:
			p = Post.objects.get(id = post_id)
			return p
		except Exception, e:
			print "find_post: ", e
			return None



	def insert_post(self, phone_num, post):
		try:
			zipcode = extract_zipcode(post)
			p = Post(phone = phone_num, post=post, zip_code = zipcode, public = True)
			p.save()
			return p.id
		except Exception, e:
			print "insert_post: ", e
			return -1

	
	def update_post(self, post_id, new_post):
		try:
			zipcode = extract_zipcode(post)	
			p = Post.objects.get(id = post_id)
			p.post = new_post
			p.save()
			return True
		except Exception, e:
			print "update_post: ", e
			return False
			
	
			
	def delete_post(self, post_id):
		try:
			p = Post.objects.get(id = post_id)
			p.delete()
			return True
		except Exception, e:
			print "delete_post: ", e
			return False
			

	def insert_reply(self, phone_num, post, reply_to, public=False):
		try:
			zipcode = extract_zipcode(post)
			p = Post(phone = phone_num, post = post, reply_to=reply_to, zip_code = zipcode, public = public)
			p.save()
			return p.id
		except Exception, e:
			print "insert_reply: ", e
			return -1




	def search_posts(self, query, limit=3, offset=0):
		try:
			data = None		
			q = re.findall('\w+', query)
			q = map(lambda x: x.lower(), filter(lambda x: x!='' and x!=',', map(lambda x: x.strip(), q)))
			q = '|'.join(q)
			data = Post.objects.extra(
			select={
				'post': "post",
				'id': "id",
				'public': "public",
				'rank': "ts_rank_cd(post_tsv, %s, 32)",
				},
			where=["(post_tsv @@ %s) AND (public = %s)"],
			params=[q, True],
			select_params=[q],
			order_by=('-rank',)
			)
			
			if(not data):
				return None
			res = ""
			for d in data:
				res = res + str(d.post) + ' (Post ID: ' + str(d.id) + "). "
				res = res + '\n'
			return res
		except Exception, e:
			print "search_posts: ", e
			return None

	
			
	def find_following(self, account):
		follow_list = []
		try:
			following = Following.objects.get(account = account)
			for f in following:
				follow_list.append(f['phone'])
		except Exception, e:
			print "find_following: ", e
		finally:
			return follow_list
	
	
	
	def delete_following(self, name, phone_number):
		account = None
		phone = phone_number.strip()
		try:
			account = Account.objects.get(name = name.lower())
			following = Following.objects.get(account = account, phone = phone)
			following.delete()
			return True
		except Exception, e:
			print "delete_following: ", e
		finally:
			return follow_list
			
	

	def add_following(self, name, phone_number):
		account = None
		phone = phone_number.strip()	
		try:
			account = Account.objects.get(name = name.lower())
			following = Following.objects.get(account = account, phone = phone)
			return True
		except Following.DoesNotExist:
			try:
				following = Following(account = account, phone = phone)
				following.save()
				return True
			except:
				return False
		except Exception, e:
			print "add_following: ", e
			return False
