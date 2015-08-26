from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
# Create your views here.


def check_username(request, username):
	response = {}
	response['result'] = 'success'
	response['exists'] = False
	if User.objects.filter(username=username).exists():
		response['exists'] = True
	return HttpResponse(json.dumps(response), content_type="application/json")
