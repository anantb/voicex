from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import *
import json

def index(request):
	return render_to_response("index.html")
	

@csrf_exempt
def trish(request):
	if(request.POST):
		res = {'status':True, 'request':request.POST, 'msg':'response sent to your number'}
		return HttpResponse(json.dumps(res))
	else:
		return render_to_response("trish.html")
		


@csrf_exempt
def mungano(request):
        if(request.POST):
                res = {'status':True, 'request':request.POST, 'msg':'response sent to your number'}
                return HttpResponse(json.dumps(res))
        else:
                return render_to_response("mungano.html")
