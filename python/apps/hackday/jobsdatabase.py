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
		
	def getAll(self):
		self.cursor.execute("""SELECT * FROM job_in""")
		data = self.cursor.fetchall()
		if data == None:
		       	return None
		for row in data:
			print row

	def delete(self, job_id):
		try:
			self.cursor.execute("DELETE FROM job_in WHERE job_id='"+str(job_id)+"'")
			self.cursor = self.conn.cursor()
			print "deleting from table "
		except:
			self.conn.rollback()
			print "excpeiton encountered in deletion", sys.exc_info()[0]

	def getPostFromId(self, job_id):
		stmt = "SELECT zip_code, blurb FROM job_in WHERE job_id='"+str(job_id)+"'"
		print stmt
		try:
			var = self.cursor.execute(stmt)
			
			print var
			print "got post from id"
			for row in self.cursor:
							print row
			
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
		
jdb = JobsDatabase()
jdb.insert("2154294019", "nurse needed", '94305')
#jdb.getAll()
#jdb.getPostFromZipcode( "19104")
			
