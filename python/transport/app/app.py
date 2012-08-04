import os
import re
from jobsdatabase import *


class JMS:
    
    def __init__(self):
        self.jdb = JobsDatabase();
        print "initialized"
        self.from_number = "12345"
    
    def getHelp(self):
        print "Help descriptionx"
        return "Help description"

    def post(self, msg):
        message = msg[msg.find("#post") + len("#post") : ].strip()
        zipcode = re.search("\d{5}", message)
        job_description = msg[msg.find(str(zipcode.group())) + 5 : ].strip()
        self.jdb.insert(self.from_number, str(zipcode.group()), job_description, "19");
    
        print zipcode.group()
        print job_description

    def edit(self, msg):
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
    
    def delete(self, msg):
        message_array = msg.split(" ")
        print message_array
        job_id = message_array[1]
        self.jdb.delete(str(job_id))
        return "Message succesfully deleted"
				
    def view(self, msg):
        print msg

    def search(self, msg):
        search_params = msg[msg.find("#search") + len("#search") : ].strip()
        print search_params

    def apply(self, msg):
        job_id = msg[msg.find("#apply") + len("#apply") : ].strip()
        return job_id

    def getType(self, msg):
        if "#post" in msg:
            self.post(msg)
        elif "#help" in msg:
            self.getHelp()
        elif "#edit" in msg:
            self.edit(msg)
        elif "#myPosts" in msg:
            self.getAllPosts()
        elif "#delete" in msg:
            self.delete(msg)
        elif "#view" in msg:
            self.view(msg)
        elif "#search" in msg:
            self.search (msg)
        elif "#apply" in msg:
            self.apply(msg)
        else:
            self.getHelp()

jms = JMS()
jms.getType("#edit 18 19104 Needed a contractor for construction work")

#jms = JMS()
#jms.defineMsg("19104 #nurse")
#jms.getType(
