from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import FoodItems
from .tables import FoodItemsTable

# Create your views here.

def fooditem(request):
	table = FoodItemsTable(FoodItems.objects.all())
	RequestConfig(request).configure(table)
	return render(request, 'tutorial/fooditem.html', {'table': table})
	
	#http://django-datatable-view.appspot.com/x-editable-columns/
	#https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
	#https://elo80ka.wordpress.com/2009/10/10/jquery-plugin-django-dynamic-formset/