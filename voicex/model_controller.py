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
from django.db import *
from msg_codes import *

'''
Application Model Controller

@author: Anant Bhardwaj
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

logger = logging.getLogger(__name__)


class ModelController:
	def __init__(self):
		logger.debug('__init__')	
	
	
	def add_account(self, name, phone):
		logger.debug('add_account')
		res = {'status':False}
		name=name.lower().strip()
		phone = phone.strip()
		try:
			acc = Account.objects.get(name = name, phone = phone)
			res['code']= msg_code['ALREADY_REGISTERED_ERROR']
		except Account.DoesNotExist:
			try:
				acc = Account(name = name, phone = phone)
				acc.save()
				res['status']= True
			except IntegrityError:
				res['code']= msg_code['REGISTER_ERROR']
			except Exception, e:
				logger.exception('add_account')
				res['code']= msg_code['DB_ERROR']
		except Exception, e:
			logger.error(e)
			res['code']= msg_code['DB_ERROR']
		logger.debug(res)
		return res
	
	
	def delete_account(self, name, phone):
		logger.debug('delete_account')
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
			logger.exception('delete_account')
			res['code']= msg_code['DB_ERROR']
		logger.debug(res)
		return res
			
	
	def find_account(self, phone):
		logger.debug('find_account')
		res = {'status':False}
		try:
			acc = Account.objects.get(phone = phone)
			res['status']= True
			res['val']=acc
		except Account.DoesNotExist:
			res['code']= msg_code['INVALID_ACCOUNT_NAME_ERROR']
		except Exception, e:
			logger.exception('find_account')
			res['code']= msg_code['DB_ERROR']
		logger.debug(res)
		return res
	
	
	def find_post(self, post_id):
		logger.debug('find_post')
		res = {'status':False}
		try:
			p = Post.objects.get(id = post_id)
			res['status']= True
			res['val']=p
		except Post.DoesNotExist:
			res['code']= msg_code['INVALID_POST_ID_ERROR']
		except Exception, e:
			logger.exception('find_post')
			res['code']= msg_code['DB_ERROR']
		logger.debug(res)
		return res



	def insert_post(self, phone_num, post):
		logger.debug('insert_post')
		res = {'status':False}
		try:
			p = Post(phone = phone_num, post=post, public = True)
			p.save()
			res['status']= True
			res['val'] = p.id
		except Exception, e:
			logger.exception('insert_post')
			res['code']= msg_code['DB_ERROR']
		logger.debug(res)
		return res

	
	def update_post(self, post_id, new_post):
		logger.debug('update_post')
		res = {'status':False}
		try:
			p = Post.objects.get(id = post_id)
			p.post = new_post
			p.save()
			res['status']= True
		except Post.DoesNotExist:
			res['code']= msg_code['INVALID_POST_ID_ERROR']
		except Exception, e:
			logger.exception('update_post')
			res['code']= msg_code['DB_ERROR']
		logger.debug(res)
		return res
			
	
			
	def delete_post(self, post_id):
		logger.debug('delete_post')
		res = {'status':False}
		try:
			p = Post.objects.get(id = post_id)
			p.delete()
			res['status']= True
		except Post.DoesNotExist:
			res['code']= msg_code['INVALID_POST_ID_ERROR']
		except Exception, e:
			logger.exception('delete_post')
			res['code']= msg_code['DB_ERROR']
		logger.debug(res)
		return res
			

	def insert_reply(self, phone_num, post, reply_to, public=False):
		logger.debug('insert_reply')
		res = {'status':False}
		try:
			p = Post(phone = phone_num, post = post, reply_to=reply_to, public = public)
			p.save()
			res['status']= True
			res['val'] = p.id
		except Exception, e:
			logger.exception('insert_reply')
			res['code']= msg_code['DB_ERROR']
		logger.debug(res)
		return res




	def search_posts(self, query, limit=3, offset=0):
		logger.debug('search_posts')
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
			logger.exception('search_posts')
			res['code']= msg_code['DB_ERROR']
		logger.debug(res)
		return res

	
			
	def find_following(self, tags):
		logger.debug('find_following')
		res = {'status':False}
		following_list = []
		try:
			following = Following.objects.filter(tag__in = tags).values()
			for f in following:
				following_list.append(f['phone'])
			res['status']= True
			res['val'] = list(set(following_list))
		except Exception, e:
			logger.exception('find_following')
			res['code']= msg_code['DB_ERROR']
		logger.debug(res)
		return res
	
	
	
	def delete_following(self, tag, phone_number):
		logger.debug('delete_following')
		res = {'status':False}
		phone = phone_number.strip()
		try:
			f = Following.objects.get(tag = tag, phone = phone)
			f.delete()
			res['status']= True
		except Following.DoesNotExist:
			res['code']= msg_code['INVALID_TAG_NAME_ERROR']
		except Exception, e:
			logger.exception('delete_following')
			res['code']= msg_code['DB_ERROR']
		logger.debug(res)
		return res
			
	

	def add_following(self, tag, phone_number):
		logger.debug('add_following')
		res = {'status':False}
		phone = phone_number.strip()	
		try:
			f = Following.objects.get(tag = tag, phone = phone)
			res['code']= msg_code['ALREADY_FOLLOWING_ERROR']
		except Following.DoesNotExist:
			try:
				if(tag[0] == '@'):
					account_name = tag[1:]
					acc = Account.objects.get(name = account_name)					
				f = Following(tag = tag, phone = phone)
				f.save()
				res['status']= True
			except Account.DoesNotExist:
				res['code']= msg_code['INVALID_ACCOUNT_NAME_ERROR']
			except Exception, e:
				logger.exception('insert_following')
				res['code']= msg_code['DB_ERROR']
		except Exception, e:
			logger.exception('add_following')
			res['code']= msg_code['DB_ERROR']
		logger.debug(res)
		return res
