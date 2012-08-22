#!/usr/bin/python
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

'''
Application database 

@author: Anant Bhardwaj
@date: Aug 21, 2012
'''

import pgdb, sys, MySQLdb


conn = None
PG = 'PG'
MYSQL = 'MYSQL'
DB = PG

try:
	if(DB == PG):
		conn = pgdb.connect("localhost:trish:postgres:postgres")
		cur = conn.cursor()
		cur.execute('CREATE TABLE IF NOT EXISTS posts (id serial PRIMARY KEY, phone varchar(20), post text, zipcode varchar(10))')  
		cur.execute('CREATE TABLE IF NOT EXISTS follow_tags (id serial PRIMARY KEY, tag varchar(20), subscription_list varchar(500))')
		cur.execute("CREATE INDEX post_index ON posts USING gin(to_tsvector('english', post))")
		cur.execute("CREATE UNIQUE INDEX tag_index ON follow_tags(tag)")
		conn.commit()
	elif(DB == MYSQL):
		conn = MySQLdb.connect(host="mysql.abhardwaj.org", user="_mysql_admin", passwd="JCAT0486", db="trish")
		cur = conn.cursor()
		cur.execute('CREATE TABLE IF NOT EXISTS posts (id INT PRIMARY KEY AUTO_INCREMENT, phone varchar(20), post text, zipcode varchar(10), FULLTEXT(post))')  
		cur.execute('CREATE TABLE IF NOT EXISTS follow_tags (id INT PRIMARY KEY AUTO_INCREMENT, tag varchar(20), subscription_list varchar(500), UNIQUE(tag))')
		conn.commit()		
except:
	print 'Error: ', sys.exc_info()    
	sys.exit(1)    

finally:    
	if conn:
		conn.close()
