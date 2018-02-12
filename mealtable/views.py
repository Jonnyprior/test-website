from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("YO, table page, not sure why its a page")
