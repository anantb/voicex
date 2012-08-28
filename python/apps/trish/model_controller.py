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

import os, sys, pgdb, re
from stemming.porter2 import stem
from utils import *

'''
Application Data Acceess

@author: Anant Bhardwaj, Trisha Kothari
@date: Aug 3, 2012
'''

class ModelController:
	def __init__(self):
		self.conn = pgdb.connect("localhost:trish:postgres:postgres") 
		self.cursor = self.conn.cursor()
		

	def find_post(self, post_id):
		try:
			stmt = "SELECT phone, post FROM posts WHERE id="+post_id		
			var = self.cursor.execute(stmt)			
			row = self.cursor.fetchone()
			return row	
		except:
			print "find_post: ", sys.exc_info()
			return None



	def insert_post(self, phone_num, post):			
		try:
			zipcode = extract_zipcode(post)			
			rowid = -1;	
			self.cursor.execute("INSERT INTO posts (phone, post, zipcode) VALUES (%s, %s, %s) RETURNING id", (phone_num, post, zipcode))	
			self.conn.commit()
			rowid = self.cursor.fetchone()[0]
			return rowid
		except:
			self.conn.rollback()
			print "insert_post: ", sys.exc_info()
			return -1

	
	def update_post(self, post_id, new_post):
		try:
			zipcode = extract_zipcode(post)	
			stmt = "UPDATE posts SET post = '" +new_post+ "', zipcode = '" +zipcode+ "' WHERE id = " + post_id		
			self.cursor.execute(stmt)
			self.conn.commit()
			return True
		except:
			self.conn.rollback()
			print "update_post: ", sys.exc_info()
			return False
			
	
			
	def delete_post(self, post_id):
		try:
			self.cursor.execute("DELETE FROM posts WHERE id="+ post_id)
			self.conn.commit();
			return True
		except:
			self.conn.rollback()
			print "delete_post: ", sys.exc_info()
			return False
		



	def search_posts(self, query, limit=3, offset=0):
		try:
			data = None		
			q = re.findall('\w+', query)
			q = map(lambda x: x.lower(), filter(lambda x: x!='' and x!=',', map(lambda x: x.strip(), q)))
			q = '|'.join(q)				
			self.cursor.execute("SELECT post, id, ts_rank_cd(to_tsvector('english', post), query, 32 /* rank/(rank+1) */) as rank FROM posts, to_tsquery('english', '"+q+"') as query WHERE to_tsvector('english', post) @@ query ORDER BY rank DESC LIMIT " + str(limit) + " OFFSET " + str(offset))
			data = self.cursor.fetchall()
			if(not data):
				return None
			res = ""
			for d in data:
				res = res + str(d[0]) + ' (Post ID: ' + str(d[1]) + "). "
				res = res + '\n'
			return res
		except:
			print "search_posts: ", sys.exc_info()
			return None

	
			
	def find_subscription_list(self, tags):
		tags = map(lambda x: stem(x.lower()), filter(lambda x: x!='' and x!=',', map(lambda x: x.strip(), tags)))
		sub_list = []
		for tag in tags:	
			self.cursor.execute("SELECT subscription_list FROM follow_tags WHERE tag='"+tag.strip()+"'")
			row = self.cursor.fetchone()
			if(row == None):
				continue
			else:			
				sub_list_for_this_tag = row[0]
				sub_list.append(sub_list_for_this_tag)
		if(len(sub_list) > 0):
			recipients = ','.join(sub_list)
			sub_list = re.split(',', recipients)
			sub_list = list(set(filter(lambda x: x!='' and x!=',', sub_list)))
		return sub_list
	


	def update_follow_tag(self, tags, phone_number):
		tags = map(lambda x: stem(x.lower()), filter(lambda x: x!='' and x!=',', map(lambda x: x.strip(), tags)))
		for tag in tags:
			self.cursor.execute("SELECT subscription_list FROM follow_tags WHERE tag='"+tag.strip()+"'")
			row = self.cursor.fetchone()
			try:		
				if(not row):
					self.cursor.execute("INSERT INTO follow_tags (tag, subscription_list) VALUES (%s, %s)", (tag.strip(), phone_number))				
					self.conn.commit()
				else:
					subscription_list = row[0]
					if(phone_number not in subscription_list):
						new_subscription_list = subscription_list + ','+ phone_number
						self.cursor.execute("UPDATE follow_tags SET subscription_list=%s WHERE tag=%s", (new_subscription_list, tag.strip()))
						self.conn.commit()
			except:
				self.conn.rollback()
				print "exception encountered", sys.exc_info()






			
