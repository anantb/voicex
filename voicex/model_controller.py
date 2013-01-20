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
from stemming.porter2 import stem
from models import *
from msg_codes import *

'''
Application Model Controller

@author: Anant Bhardwaj, Trisha Kothari
@date: Aug 3, 2012
'''

'''
please use the below generic return type

{
'status' : True/False,
'code' : msg_code (especially to indicate error),
'val' : return value,
'msg' :additional error message
} 



'''

class ModelController:
	def __init__(self):
		pass
	
	
	
	def add_account(self, name, phone):
		res = {'status':False}
		name=name.lower().strip()
		phone = phone.strip()
		try:
			acc = Account.objects.get(name = name, phone = phone)
			res['status']= True
		except Account.DoesNotExist:
			try:
				acc = Account(name = name, phone = phone)
				acc.save()
				res['status']= True
			except:
				res['code']= msg_code['DB_ERROR']
		except Exception, e:
			res['code']= msg_code['DB_ERROR']
		logging.debug(res)
		return res
	
	
	def delete_account(self, name, phone):
		res = {'status':False}
		name=name.lower().strip()
		phone = phone.strip()
		try:
			acc = Account.objects.get(name = name, phone = phone)
			acc.delete()
			res['status']= True
		except Account.DoesNotExist:
			res['code']= msg_code['INVALID_ACCOUNT_NAME_ERROR']
		except Exception, e:
			res['code']= msg_code['DB_ERROR']
		logging.debug(res)
		return res
			
	
	def find_account(self, phone):
		res = {'status':False}
		try:
			acc = Account.objects.get(phone = phone)
			res['status']= True
			res['val']=acc
		except Account.DoesNotExist:
			res['code']= msg_code['INVALID_ACCOUNT_NAME_ERROR']
		except Exception, e:
			res['code']= msg_code['DB_ERROR']
		logging.debug(res)
		return res
	
	
	def find_post(self, post_id):
		res = {'status':False}
		try:
			p = Post.objects.get(id = post_id)
			res['status']= True
			res['val']=p
		except Post.DoesNotExist:
			res['code']= msg_code['INVALID_POST_ID_ERROR']
		except Exception, e:
			res['code']= msg_code['DB_ERROR']
		logging.debug(res)
		return res



	def insert_post(self, phone_num, post):
		res = {'status':False}
		try:
			p = Post(phone = phone_num, post=post, public = True)
			p.save()
			res['status']= True
			res['val'] = p.id
		except Exception, e:
			res['code']= msg_code['DB_ERROR']
		logging.debug(res)
		return res

	
	def update_post(self, post_id, new_post):
		res = {'status':False}
		try:
			p = Post.objects.get(id = post_id)
			p.post = new_post
			p.save()
			res['status']= True
		except Post.DoesNotExist:
			res['code']= msg_code['INVALID_POST_ID_ERROR']
		except Exception, e:
			res['code']= msg_code['DB_ERROR']
		logging.debug(res)
		return res
			
	
			
	def delete_post(self, post_id):
		res = {'status':False}
		try:
			p = Post.objects.get(id = post_id)
			p.delete()
			res['status']= True
		except Post.DoesNotExist:
			res['code']= msg_code['INVALID_POST_ID_ERROR']
		except Exception, e:
			res['code']= msg_code['DB_ERROR']
		logging.debug(res)
		return res
			

	def insert_reply(self, phone_num, post, reply_to, public=False):
		res = {'status':False}
		try:
			p = Post(phone = phone_num, post = post, reply_to=reply_to, public = public)
			p.save()
			res['status']= True
			res['val'] = p.id
		except Exception, e:
			res['code']= msg_code['DB_ERROR']
		logging.debug(res)
		return res




	def search_posts(self, query, limit=3, offset=0):
		res = {'status':False}
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
			res['status'] = True
			if(not data):
				res['val'] = 'No matching post.'
			out = ""
			for d in data:
				out = out + str(d.post) + ' (Post ID: ' + str(d.id) + "). "
				out = out + '\n'
			if(data):
				res['val'] = out
		except Exception, e:
			res['code']= msg_code['DB_ERROR']
		logging.debug(res)
		return res

	
			
	def find_subscribers(self, account):
		res = {'status':False}
		subscribers_list = []
		try:
			subscribers = Subscriber.objects.filter(account = account).values()
			for s in subscribers:
				subscribers_list.append(s['phone'])
			res['status']= True
			res['val'] = subscribers_list
		except Exception, e:
			res['code']= msg_code['DB_ERROR']
		logging.debug(res)
		return res
	
	
	
	def delete_subscriber(self, name, phone_number):
		res = {'status':False}
		account = None
		phone = phone_number.strip()
		try:
			account = Account.objects.get(name = name.lower())
			s = Subscriber.objects.get(account = account, phone = phone)
			s.delete()
			res['status']= True
		except Exception, e:
			res['code']= msg_code['DB_ERROR']
		logging.debug(res)
		return res
			
	

	def add_subscriber(self, name, phone_number):
		res = {'status':False}
		account = None
		phone = phone_number.strip()	
		try:
			account = Account.objects.get(name = name.lower())
			s = Subscriber.objects.get(account = account, phone = phone)
			res['status']= True
		except Subscriber.DoesNotExist:
			try:
				s = Subscriber(account = account, phone = phone)
				s.save()
				res['status']= True
			except:
				res['code']= msg_code['DB_ERROR']
		except Exception, e:
			res['code']= msg_code['DB_ERROR']
		logging.debug(res)
		return res
