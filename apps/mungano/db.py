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

import os
import MySQLdb
import re
import sys

'''
Application database 

@author: Anant Bhardwaj
@date: Aug 3, 2012

'''

class MunganoDatabase:
	def __init__(self):
		self.conn = MySQLdb.connect(host="mysql.abhardwaj.org", 
		user="_mysql_admin", passwd="JCAT0486", db="mungano")
		self.cursor = self.conn.cursor()
	
			
	def find_subscription_list(self, tag):
		self.cursor.execute("SELECT subscription_list FROM follow_tags WHERE tag='"+tag.strip()+"'")
		row = self.cursor.fetchone()
		if(row == None):
			return None
		else:			
			return(row[0])


	def update_subscription(self, tag, phone_number):
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






			
