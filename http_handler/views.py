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

from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import *
import json
from voicex.main import VoiceX
from transport import config

'''
Main Query Handler (Views)

@author: Anant Bhardwaj
@date: Oct 8, 2012
'''

def index(request):
	return render_to_response("index.html")
	

@csrf_exempt
def voicex_us(request):
	if(request.POST):
		msg_data = {}
		if('number' in request.POST):
			msg_data['from'] = request.POST['number']
		if('text' in request.POST):
			msg_data['text'] = request.POST['text']
		if('from' in request.POST):
			msg_data['from'] = request.POST['from']
		try:
			print "...here ..."
			v = VoiceX(auth= config.GV_VOICEX_AUTH)
			v.msg_new(msg_data)
			print "... end ..."
			return HttpResponse(json.dumps({'status':'ok'}))
		except Exception, e:
			print e
			return HttpResponse(json.dumps({'status':'error'}))
	else:
		return HttpResponse(json.dumps({'status':'ok'}))
		
		

@csrf_exempt
def voicex_ke(request):
	if(request.POST):
		msg_data = {}
		if('number' in request.POST):
			msg_data['from'] = request.POST['number']
		if('text' in request.POST):
			msg_data['text'] = request.POST['text']
		if('from' in request.POST):
			msg_data['from'] = request.POST['from']
		
		try:
			v = VoiceX(auth= config.AT_VOICEX_AUTH)
			v.msg_new(msg_data)
			return HttpResponse(json.dumps({'status':'ok'}))
		except Exception, e:
			print e
			return HttpResponse(json.dumps({'status':'error'}))
		
	else:
		return HttpResponse(json.dumps({'status':'ok'}))


