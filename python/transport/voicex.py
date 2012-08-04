#!/usr/bin/python
import httplib, urllib, re, os, time
from constants import *
from login import *
from bs4 import BeautifulSoup

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
	
def sms(to_number, text, token):
	print "Sending message to: "+ to_number;
	params = {'phoneNumber': to_number, 'text':text, '_rnr_se':token['rnr_se']}
	print http_post(SMS_SEND_URL, params, token['auth'])

def fetch_unread_sms(token, url = SMS_UNREAD_URL):
	return fetch_inbox(token, url = url)


def fetch_all_sms(token, url = SMS_URL):
	return fetch_inbox(token, url = url)

def fetch_inbox(token, url = INBOX_URL):
	conn = httplib.HTTPSConnection("www.google.com")
	conn.putrequest("GET", url)
	conn.putheader( "Authorization", "GoogleLogin auth="+token['auth'])
	conn.endheaders()
	res = conn.getresponse().read()
	soup = BeautifulSoup(res)
	msg_data = soup.find('json').find(text = True)
	return str(msg_data)
	

def main():	
	token = login('voicex.git@gmail.com', 'VoiceX@Git')	
	#sms('2134530488', 'hello world', token)

if __name__ == "__main__":
    main()
