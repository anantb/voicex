import os
import re
from jobsdatabase import *
from transport.voicex import *

class JMS:
    
    def __init__(self, token):
        self.jdb = JobsDatabase();
        print "initialized"
        self.token = token
    
    def getHelp(self):
        print "Help ..."

    def post(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		message = msg[msg.find("#post") + len("#post") : ].strip()
		zipcode = re.search("\d{5}", message)
		job_description = msg[msg.find(str(zipcode.group())) + 5 : ].strip()
		job_id = self.jdb.insert(phone_num, job_description, str(zipcode.group()));		
		sms(phone_num, 'success! job post_id is: ' + str(job_id), self.token)

    def edit(self, msg_data):
		msg = msg_data['messageText']
		message = msg[msg.find("#edit") + len("#edit") : ].strip()
		message_array = msg.split(" ")
		print message_array
		job_id = message_array[1]
		job_description = msg[msg.find(str(job_id)) + len(str(job_id)) : ].strip()
		self.jdb.delete(str(job_id))
		job_description =  "#post " + job_description
		self.post(job_description)
		print job_id
		print job_description
		print message

    def getAllPosts(self):
		print from_number
    
    def delete(self, msg_data):
		msg = msg_data['messageText']
		phone_num = msg_data['phoneNumber']
		message_array = msg.split(" ")
		print message_array
		job_id = message_array[1]
		self.jdb.delete(str(job_id))
		sms(phone_num, 'Message successfully deleted! ', self.token)
		
				
    def view(self, msg_data):
        msg = msg_data['messageText']
        phone_num = msg_data['phoneNumber']
        job_id = msg[msg.find("#view") + len("#view") : ].strip()
        print job_id
        x = self.jdb.getPostFromId(int(job_id))				
        print x
        sms(phone_num, "success", self.token)

    def search(self, msg_data):
        msg = msg_data['messageText']
        phone_num = msg_data['phoneNumber']
        search_params = msg[msg.find("#search") + len("#search") : ].strip()
        print search_params

    def apply(self, msg_data):
        msg = msg_data['messageText']
        phone_num = msg_data['phoneNumber']
        message = msg[msg.find("#apply") + len("#apply") : ].strip()
        message_array = msg.split(" ")
        print message_array
        job_id = message_array[1]
        job_description = msg[msg.find(str(job_id)) + len(str(job_id)) : ].strip()
        print "job id obtained is:", job_id, "with job_description", job_description
        sms(phone_num, 'Succesfully applied for job! ', self.token)
        return_no = self.jdb.apply(int(job_id))
        print return_no
        sms(return_no, job_description, self.token)
        

    def handle(self, msg_data):
		msg = msg_data['messageText']
		print "inside main --- " +  msg
		if "#post" in msg:
			self.post(msg_data)
		elif "#help" in msg:
			self.getHelp()
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
		else:
			self.getHelp()


#jms = JMS()
#jms.getType("#view 19")
#jms.defineMsg("19104 #nurse")
#jms.getType(
