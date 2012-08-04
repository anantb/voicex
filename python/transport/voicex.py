#!/usr/bin/python
import httplib, urllib, re, os
from constants import *
from login import *

'''
@author: anant bhardwaj
@date: Aug 3, 2012

voicex APIs
'''


def http_post(url, params, auth):
	conn = httplib.HTTPSConnection("www.google.com")
	headers = {"Content-type": "application/x-www-form-urlencoded",
			"Accept": "text/plain", "Authorization": "GoogleLogin auth="+auth}
	params = urllib.urlencode(params)
	conn.request("POST", url, params, headers)	
	res = conn.getresponse().read()
	return res
	
def sms(to_number, text, auth, rnr_se):
	print "Sending message to: "+ to_number;
	params = {'phoneNumber': to_number, 'text':text, '_rnr_se':rnr_se}
	print http_post(SMS_SEND_URL, params, auth)

def fetch_inbox(url, auth):
	conn = httplib.HTTPSConnection("www.google.com")
	conn.putrequest("GET", url)
	conn.putheader( "Authorization", "GoogleLogin auth="+auth)
	conn.endheaders()
	res = conn.getresponse().read()
	print res
	

def main():	
	auth, rnr_se = login('voicex.git@gmail.com', 'VoiceX@Git')	
	fetch_inbox(INBOX_URL, auth)
	#sms('2134530488', 'hello world')

if __name__ == "__main__":
    main()
