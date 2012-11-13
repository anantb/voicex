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

import os, sys, pgdb, re
from stemming.porter2 import stem
from models import *

'''
Mungano Model Controller

@author: Anant Bhardwaj
@date: Oct 7, 2012
'''

class ModelController:
	def __init__(self):
		pass

	def find_subscription(self, phone_number):
		try:
			sub = Subscription.objects.get(phone = phone_number)
			return sub
		except Exception, e:
			print "find_subscription: ", e
			return None



	def insert_alert(self, sub, delay=0, msg=None):
		try:
			alert = Alert(sub=sub, delay=delay, msg=msg)
			alert.save()
			return alert.id
		except Exception, e:
			print "insert_alert: ", e
			return -1
	


	def update_subscription(self, sub_list, phone_number):
		try:
			sub = Subscription.objects.get(phone = phone_number)
			sub.sub_list = sub_list
			sub.update()
			return True
		except Subscription.DoesNotExist:
			try:
				sub = Subscription(phone = phone_number, sub = sub_list)
				sub.save()
				return True
			except Exception, e:
				print "update_subscription: ", e
				return False
			
