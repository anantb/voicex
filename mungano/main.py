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
import mungano.tasks
import sys, re
from model_controller import *
from models import *
from transport.voicex import VoiceXTransport
from transport import config

'''
Mungano Handler Interface

@author: Anant Bhardwaj
@date: Oct 7, 2012
'''

class Mungano:
	def __init__(self):
		print "here"
		self.mc = ModelController()
		self.v = VoiceXTransport(transport=config.GV, auth= config.GV_MUNGANO_AUTH)


	def init_callback(self):
		self.v.set_callback(callback = self.msg_new)


	def show_help(self, msg, phone_num):
		help_text = "Welcome to Mungano! To subscribe : #sub phone_numbers_separated_by_a_comma, To send an immediate alert: #alert, To send delayed alert: #alert delay_time_in_minutes msg, To view your subscription list: #view, To override your old subscription with a new list: #sub new_list_of_phone_numbers_separated_by_a_comma"
		if(not msg):
			pass
		elif('sub' in msg):
			help_text = "Help for #sub : #sub phone_numbers_separated_by_a_comma"
		elif('alert' in msg):
			help_text = "Help for #alert : For immediate alert: #alert, For delayed alert: #alert delay_time_in_minutes msg"
		elif('view' in msg):
			help_text = "Help for #view : #view"
		else:
			pass			
		self.v.sms(phone_num, help_text)



	def handle_alert(self, msg_data, phone_num):	
		sub = self.mc.find_subscription(phone_num)
		if(sub):
		#	alert_id = self.mc.insert_alert(sub);
			self.alert(sub, "alert from %s" %phone_num)
		else:		
			res = 'No subscription found for phone number: %s' %(phone_num)
		
        def testdelay(self, delay, phone_num):
		try:
			d = float(delay)
			print "Your d is " + d
			mungano.tasks.delayed_sms.delay(self.v, phone_num, "this text is delayed by %s minutes" %(delay), d)          
		except:
			print sys.exc_info()
			self.v.sms(phone_num, "couldn't schedule a delayed msg")


	def alert(self, sub, msg):
		self.v.sms(sub.sub_list, msg)


	def view(self, phone_num):	
		sub = self.mc.find_subscription(phone_num)
		if(sub):
			res = sub.sub_list
		else:		
			res = 'No subscription found for phone number: %s' %(phone_num)
		self.v.sms(phone_num, res)


	def subscribe(self, sub_list, phone_num):
		if(self.mc.update_subscription(sub_list, phone_num)):
			self.v.sms(phone_num, 'Alert subscription updated successfully for %s.' %(phone_num))
		else:
			self.v.sms(phone_num, 'Error occured while updating the alert subscription for %s.' %(phone_num))


	def parse(self, msg, phone_num):
		try:
			msg_data = (msg.strip()).split(" ", 1)
			msg_data = map(lambda x: x.strip(), msg_data)
			if (msg_data[0] == "#sub"):
				self.subscribe(msg_data[1], phone_num)
			elif(msg_data[0] == "#view"):
				self.view(phone_num)
			elif(msg_data[0] == "#alert"):
				self.handle_alert(msg, phone_num)
			elif (msg_data[0] == "#delayalert"):
				self.testdelay(msg_data[1], phone_num)
			elif(msg_data[0] == "#help"):
				self.show_help(msg, phone_num)
			else:
				self.show_help(msg, phone_num)
		except Exception, e:
			print "parse: ", e
			self.show_help(msg, phone_num)



	def handle(self, msg_data):
		print msg_data
		msg = msg_data['text'].strip()
		phone_num = msg_data['from'].strip()
		if(not msg):
			self.getHelp(msg, phone_num)
		else:
			self.parse(msg, phone_num)
	
	
	def msg_new(self, msg):
		self.handle(msg)


def main():	
	t= Mungano()
	t.init_callback()


if __name__ == "__main__":
    main()
	
	

