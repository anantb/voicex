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
from engine.main import VoiceXEngine

'''
VoiceX Query Handler (Views)

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
		t = VoiceXEngine()
		t.msg_new(msg_data)
		res = {'status':True, 'request':request.POST, 'msg':'response sent to your number'}
		return HttpResponse(json.dumps(res))
	else:
		return render_to_response("voicex_us.html")
		

@csrf_exempt
def voicex_ke(request):
	if(request.POST):
		res = {'status':False, 'request':request.POST, 'msg':'not available'}
		return HttpResponse(json.dumps(res))
	else:
		return render_to_response("voicex_ke.html")
		


@csrf_exempt
def mungano_us(request):
        if(request.POST):
                res = {'status':False, 'request':request.POST, 'msg':'not available'}
                return HttpResponse(json.dumps(res))
        else:
                return render_to_response("mungano_us.html")
                

@csrf_exempt
def mungano_ke(request):
        if(request.POST):
                res = {'status':False, 'request':request.POST, 'msg':'not available'}
                return HttpResponse(json.dumps(res))
        else:
                return render_to_response("mungano_ke.html")
