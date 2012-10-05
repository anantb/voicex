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

import httplib, urllib, re, os
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
	tokens = load_tokens()
	if(tokens !=None):
		t = tokens.split('|')
		print "loaded tokens"
		return {'auth':t[0], 'rnr_se':t[1]}
		
	else:
		print "login reset"
		tokens = login_reset(email, password)
	return tokens
	
def load_tokens():
	try:	
		tokens = open('/tmp/resources/' + 'voicex_token', 'rU').read()
		return tokens
	except IOError:
		return None
	

def write_tokens(auth, rnr_se):
	f = w_open('/tmp/resources/' + 'voicex_token')
	f.write('|'.join([auth, rnr_se]))
	f.close()
	
def w_open(filename):
	dir = os.path.dirname(filename)
	try:
		os.stat(dir)
	except:
		os.makedirs(dir)
	return open(filename, 'w')

def login_reset(email, password):
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
		auth = res[res.find('Auth=')+len('Auth='):].strip()
		print "auth success: " + auth
	elif('Error=: ' in res):
		error = res[res.find('Error=')+len('Error='):].strip()
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
			rnr_se = rnr_se.replace("'",'').strip()
			print rnr_se
	write_tokens(auth, rnr_se)
	return {'auth':auth, 'rnr_se':rnr_se}
