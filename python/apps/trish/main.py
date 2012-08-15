"""
Copyright (c) 2012 Trisha Kothari

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
import re
from jobsdatabase import *
from transport.voicex import *


'''
@author: Trisha Kothari
@date: Aug 3, 2012

main entry for the application  -- my first opensource project
'''

class JMS:

	def __init__(self, token):
		self.jdb = JobsDatabase();
		print "initialized"
		self.token = token

	def getHelp(self, msg_data):
		phone_num = msg_data['phoneNumber']
		help_text = "Welcome to LinkUnlinked! Search for jobs: #search; Post a job: #post"
		sms(phone_num, help_text, self.token)

	def post(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		message = msg[msg.find("#post") + len("#post") : ].strip()
		if len(message) == 0:
			sms(phone_num, "Text #post zipcode jobdescription", self.token)
			return
		zipcode = re.search("\d{5}", message)
		if(zipcode==None):
			zip_code = '00000'
		else:
			zip_code = str(zipcode.group())		
				
		job_id = self.jdb.insert(phone_num, message, zip_code);		
		sms(phone_num, 'Job successfully posted. To view the post, text #view ' + str(job_id), self.token)
		tokens = re.split(' ', message)
		print 'tokens: ' + str(tokens)
		if(tokens != None):
			for token in tokens:
				print 'token: ' + token
				res = self.jdb.search(token)
				if(res!='No matching result'):
					to_send = self.jdb.get_subscription(token)
					print to_send
					if(to_send!= None):
						sms(to_send, "New Job Post: " + message +", Job ID: " + str(job_id), self.token)		
				
		return
		
	def edit(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		message = msg[msg.find("#edit") + len("#edit") : ].strip()
		if len(message) == 0:
					sms(phone_num, "To edit a post, text #edit JOBID new job description (include zip code)", self.token)
					return
		message_array = msg.split(" ")
		print message_array
		job_id = message_array[1]
		job_description = msg[msg.find(str(job_id)) + len(str(job_id)) : ].strip()
		zipcode = re.search("\d{5}", job_description)
		print zipcode


		if(zipcode==None):
			zip_code = '00000'
		else:
			zip_code = str(zipcode.group())
		sms(phone_num, 'success! Your job: ' + str(job_id) + "has been updated!:", self.token)
		mesg = msg[msg.find(str(zipcode.group())) + 5 :].strip()
		self.jdb.update(job_id, zip_code, mesg);	
				
		print job_id
		print job_description
		print zip_code
		sms(phone_num, 'Job ' + str(job_id) + "has been succesfully updated", self.token)
		

	def getAllPosts(self):
		print from_number

	def delete(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		message_array = msg.split(" ")
		print message_array
		if len(message_array) == 1:
					sms(phone_num, "To delete a post text #delete JOBID", self.token)
					return
		job_id = message_array[1]
		self.jdb.delete(str(job_id))
		sms(phone_num, "Job " + job_id+ " has been successfully deleted!", self.token)
		
				
	def view(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		job_id = msg[msg.find("#view") + len("#view") : ].strip()
		if len(job_id) == 0:
			sms(phone_num, "To view a post text #view JOBID", self.token)
			return
		blurb = self.jdb.getPostFromId(int(job_id))
		sms(phone_num, blurb, self.token)

	def search(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		search_params = msg[msg.find("#search") + len("#search") : ].strip()
		if len(search_params) == 0:
			help_text = "Text #search keywords; Text for more information:#apply JOBID"
			sms(phone_num, help_text, self.token)
			return
		res = self.jdb.search(search_params)
		print res
		sms(phone_num, res, self.token)

	def apply(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		message = msg[msg.find("#apply") + len("#apply") : ].strip()
		if (len(message) == 0):
			help_text = "Text #apply JOBID introduce yourself!"
			sms(phone_num, help_text, self.token)
			return
		message_array = msg.split(" ")
		print message_array
		job_id = message_array[1]
		job_description = msg[msg.find(str(job_id)) + len(str(job_id)) : ].strip()
		print "job id obtained is:", job_id, "with job_description", job_description
		sms(phone_num, 'Your application for JOBID' + job_id + "has been sucessfully sumbitted!", self.token)
		return_no = self.jdb.apply(int(job_id))
		print return_no
		sms(return_no, job_description, self.token)
		return
		
	def follow(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		keywords = msg[msg.find("#follow") + len("#follow") : ].strip()
		keywords = re.split(',', keywords)
		for keyword in keywords:
			x = self.jdb.follow(keyword, phone_num)
		sms(phone_num, 'follow entry added successfully', self.token)


	def handle(self, msg_data):
		msg = msg_data['messageText']
		print "inside main --- " +  msg
		if "#post" in msg:
			self.post(msg_data)
		elif "#help" in msg:
			self.getHelp(msg_data)
		elif "#edit" in msg:
			self.edit(msg_data)
		elif "#myPosts" in msg:
			self.getAllPosts()
		elif "#delete" in msg:
			self.delete(msg_data)
		elif "#view" in msg:
			self.view(msg_data)
		elif "#search" in msg:
			self.search (msg_data)
		elif "#apply" in msg:
			self.apply(msg_data)
		elif "#follow" in msg:
			self.follow(msg_data)
		else:
			self.getHelp(msg_data)


#jms = JMS()
#jms.getType("#view 19")
#jms.defineMsg("19104 #nurse")
#jms.getType(
