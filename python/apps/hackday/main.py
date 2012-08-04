import os
import re
from jobsdatabase import *
from transport.voicex import *

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
		job_id = self.jdb.insert(phone_num, message, str(zipcode.group()));		
		sms(phone_num, 'Job successfully posted. To view the post, text #view ' + str(job_id), self.token)
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
		self.jdb.delete(str(job_id))
		job_description =  "#post " + job_description
		self.post(job_description)
		print job_id
		print job_description
		print message
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
        x = self.jdb.search(search_params)
        print x
        sms(phone_num, x, self.token)
        return

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
        xreturn
        

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
		else:
			self.getHelp(msg_data)


#jms = JMS()
#jms.getType("#view 19")
#jms.defineMsg("19104 #nurse")
#jms.getType(
