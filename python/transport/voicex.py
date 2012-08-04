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
	

def call(forwardingNumber, outgoingNumber, token):
	print "Initiating call to: "+outgoingNumber + ", through: " + forwardingNumber
	params = {'forwardingNumber': forwardingNumber, 
			  'outgoingNumber':outgoingNumber, 
			  'phoneType':'1',
			  'subscriberNumber':'undefined',
			  'remember' : '0',
			  '_rnr_se':token['rnr_se']}
	print http_post(CALL_INITIATE_URL, params, token['auth'])
	

def mark_read(msg, token):
	print "Marking Msg as Read: "+ msg['messageText']
	params = {'messages': msg['id'], 'read':'1', '_rnr_se':token['rnr_se']}
	print http_post(MSG_MARK_READ_URL, params, token['auth'])


def mark_unread(msg, token):
	print "Marking Msg as UnRead: "+ msg['messageText']
	params = {'messages': msg['id'], 'read':'0', '_rnr_se':token['rnr_se']}
	print http_post(MSG_MARK_READ_URL, params, token['auth'])

	
def delete(msg, token):
	print "Deleting Msg: "+ msg['messageText']
	params = {'messages': msg['id'], 'trash':'1', '_rnr_se':token['rnr_se']}
	print http_post(MSG_MARK_READ_URL, params, token['auth'])	
	

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
