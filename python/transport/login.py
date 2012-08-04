#!/usr/bin/python
import httplib, urllib, re
from constants import *
'''
@author: anant bhardwaj
@date: Aug 3, 2012

voicex login
'''
accountType = "google";
service = "grandcentral";
source = "voicex";


def login(email, password):
	conn = httplib.HTTPSConnection("www.google.com")
	headers = {"Content-type": "application/x-www-form-urlencoded",
			"Accept": "text/plain"}
	params = urllib.urlencode({'accountType': accountType, 
						   'Email': email,
						   'Passwd': password,
						   'service': service,
						   'source':source})	
	conn.request("POST", LOGIN_URL, params, headers)
	res = conn.getresponse().read()
	print res
	if('Auth=' in res):		
		auth = res[res.find('Auth=')+len('Auth='):]
		print "auth success: " + auth
	elif('Error=: ' in res):
		error = res[res.find('=')+1:]
		print "auth failed: " + error
	conn = httplib.HTTPSConnection("www.google.com")
	conn.putrequest("GET", ROOT_URL)
	conn.putheader( "Authorization", "GoogleLogin auth="+auth)
	conn.endheaders()
	res = conn.getresponse().read()
	lines = re.split('\n', res)
	for line in lines:
		if("'_rnr_se': '" in line):
			print line
			rnr_se = line[line.find("'_rnr_se': '")+len("_rnr_se': "):-1]
			rnr_se = rnr_se.replace("'",'')
			print rnr_se


def main():
	login('voicex.git@gmail.com', 'VoiceX@Git')

if __name__ == "__main__":
    main()
