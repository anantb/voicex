from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import *
import json
from engine.main import VoiceXEngine

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
