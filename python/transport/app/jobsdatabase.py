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

	def insert(self, from_number, zipcode, description, job_id):
		try:
			self.cursor.execute("INSERT INTO job_in VALUES (%s,%s, %s, %s)", (from_number, zipcode, description, job_id))
			self.conn.commit()
			print "inserting values!"
		except:
			self.conn.rollback()
			print "exception encountered", sys.exc_info()[0]
#		self.conn.close()
		
	def getAll(self):
		self.cursor.execute("""SELECT * FROM job_in""")
		data = self.cursor.fetchall()
		if data == None:
		       	return None
		for row in data:
			print row

	def delete(self, job_id):
		try:
			self.cursor.execute("""DELETE FROM job_in WHERE job_id=%s""", (job_id))
			self.cursor = self.conn.cursor()
			print "deleting from table "
		except:
			self.conn.rollback()
			print "excpeiton encountered in deletion"

			
	def getPostFromZipcode(self, zipcode_obtained):
		jobs = list()
		try:
			var = self.cursor.execute("""SELECT description, job_id FROM job_in WHERE zipcode=%s LIMIT 3""", (zipcode_obtained))
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
#jdb.insert("2154294019", "19104", "nurse needed", "999989100")
#jdb.getAll()
#jdb.getPostFromZipcode( "19104")
			
