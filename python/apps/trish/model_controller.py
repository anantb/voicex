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

import os, sys, pgdb, re

'''
Application Data Acceess

@author: Trisha Kothari, Anant Bhardwaj
@date: Aug 3, 2012
'''
PG = 'PG'
MYSQL = 'MYSQL'
DB = PG
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



	def insert_post(self, phone_num, post, zipcode):
		try:			
			rowid = -1;			
			self.cursor.execute("INSERT INTO posts (phone, post, zipcode) VALUES (%s, %s, %s) RETURNING id", (phone_num, post, zipcode))	
			self.conn.commit()
			rowid = self.cursor.fetchone()[0]
			return rowid
		except:
			self.conn.rollback()
			print "insert_post: ", sys.exc_info()
			return -1

	
	def update_post(self, post_id, zipcode, msg):
		try:
			stmt = "UPDATE posts SET zipcode = '" +zipcode+ "', post = '" +msg+ "' WHERE id = " + post_id		
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
		



	def search_posts(self, query):
		try:
			data = None		
			q = re.findall('\w+', query)
			q = map(lambda x: x.strip(), q)
			q = filter(lambda x: x!='' and x!=',', q)
			q = map(lambda x: x.lower(), q)
			q = '|'.join(q)				
			self.cursor.execute("SELECT post, id, ts_rank_cd(to_tsvector('english', post), query, 32 /* rank/(rank+1) */) as rank FROM posts, to_tsquery('english', '"+q+"') as query WHERE to_tsvector('english', post) @@ query ORDER BY rank DESC LIMIT 3")
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

	
			
	def find_subscription_list(self, tag):
		self.cursor.execute("SELECT subscription_list FROM follow_tags WHERE tag='"+tag.strip()+"'")
		row = self.cursor.fetchone()
		if(row == None):
			return None
		else:			
			return(row[0])


	def update_follow_tag(self, tag, phone_number):
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
			return True
		except:
			self.conn.rollback()
			print "exception encountered", sys.exc_info()
			return False






			
