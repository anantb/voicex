import os
import MySQLdb
import re
from xml.etree import ElementTree
import sys

class JobsDatabase:
#	conn = MySQLdb.connect(host="mysql.abhardwaj.org", user="_mysql_admin", passwd="JCAT0486", db="in_hackday")

	def __init__(self):
		self.conn = MySQLdb.connect(host="mysql.abhardwaj.org", user="_mysql_admin", passwd="JCAT0486", db="in_hackday")
		self.cursor = self.conn.cursor()
		print (self.conn)

	def insert(self, phone_num, blurb, zip_code):
		try:
			self.cursor.execute("INSERT INTO job_in (phone_num, blurb, zip_code) VALUES (%s, %s, %s)", (phone_num, blurb, zip_code))			
			self.conn.commit()
			return self.cursor.lastrowid
		except:
			self.conn.rollback()
			print "exception encountered", sys.exc_info()[0]
		return None
		
	def follow(self, keyword, phone_number):
		self.cursor.execute("SELECT subscription FROM follow_in WHERE keyword='"+keyword.strip()+"'")
		row = self.cursor.fetchone()
		print "here..."
		try:		
			if(row == None):
				print "inserting"
				self.cursor.execute("INSERT INTO follow_in (keyword, subscription) VALUES (%s, %s)", (keyword.strip(), phone_number))				
			else:
				print "updating"
				subscription = row[0]
				new_subscription = subscription + ','+ phone_number
				print new_subscription
				self.cursor.execute("UPDATE follow_in SET subscription=%s WHERE keyword=%s", (new_subscription, keyword.strip()))
			self.conn.commit()
		except:
			self.conn.rollback()
			print "exception encountered", sys.exc_info()[0]
	
	def update(self, job_id, zip_code, msg):
		stmt = "UPDATE job_in SET zip_code = " +zip_code+ ", blurb = " +msg+ "WHERE job_id = " + job_id
		print stmt
		try:
			var = self.cursor.execute(stmt)
			print var
		except:
			print "exception encountered in search", sys.exc_info()[0]
		
			
		
		
	def getAll(self):
		self.cursor.execute("""SELECT * FROM job_in""")
		data = self.cursor.fetchall()
		if data == None:
		       	return None
		for row in data:
			print row


	def search(self, keyword):
		stmt = "SELECT zip_code, blurb, job_id FROM job_in WHERE MATCH (blurb) AGAINST('"+ keyword+"') LIMIT 3"
		print stmt
		#stmt = "SELECT job_id, blurb, zip_code FROM job_in WHERE MATCH (zip_code, blurb) AGAINST('"+str(key_word)"')"
		try:
			var = self.cursor.execute(stmt)
			print var
			data = self.cursor.fetchall()
			return data
		except:
			print "exception encountered in search", sys.exc_info()[0]

	def delete(self, job_id):
		try:
			self.cursor.execute("DELETE FROM job_in WHERE job_id='"+str(job_id)+"'")
			self.cursor = self.conn.cursor()
			print "deleting from table "
		except:
			self.conn.rollback()
			print "excpeiton encountered in deletion", sys.exc_info()[0]

	def getPostFromId(self, job_id):
		stmt = "SELECT blurb FROM job_in WHERE job_id='"+str(job_id)+"'"
		try:
			var = self.cursor.execute(stmt)			
			row = self.cursor.fetchone()
			return row[0]			
		except:
			print "got exception from getPostFromId", sys.exc_info()[0]

	def apply(self, job_id):
			stmt = "SELECT phone_num FROM job_in WHERE job_id='"+str(job_id)+"'"
			print stmt
			try:
				var = self.cursor.execute(stmt)
			 	print var
				for row in self.cursor:
					x= row[0]
				return x
			except:
				print "got exception from apply", sys.exc_info()[0]
			
	def getPostFromZipcode(self, zipcode_obtained):
		jobs = list()
		try:
			var = self.cursor.execute("""SELECT post, job_id FROM job_in WHERE zip_code=%s LIMIT 3""", (zipcode_obtained))
			for row in self.cursor:
				jobs.append("Job Id:" + str(row[1]) +  " looking for: " + row[0])
				print row[1]
				print row[0]
				#print row[1]				
			print "got data!"+ str(var)
			print jobs
		except:
			print "got exception :(", sys.exc_info()[0]
		self.conn.close()
		
#jdb = JobsDatabase()
#jdb.insert("2154294019", "nurse needed", '94305')
#jdb.getAll()
#jdb.getPostFromZipcode( "19104")
			
