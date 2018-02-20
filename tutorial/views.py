from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import FoodItems
from .tables import FoodItemsTable
from django.views.generic import CreateView
#from .forms import AddFoodItemForm


# Create your views here.

def fooditem(request):
	table = FoodItemsTable(FoodItems.objects.all())
	RequestConfig(request).configure(table)
	obj_list = FoodItems.objects.all()
	args = {'table': table, 'food_list': obj_list}
	return render(request, 'tutorial/fooditem.html', args)

	#http://django-datatable-view.appspot.com/x-editable-columns/
	#https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
	#https://elo80ka.wordpress.com/2009/10/10/jquery-plugin-django-dynamic-formset/

	# Use form to add new food items
	# Find way to dynamically get food item and display in new list

class AddFoodItemView(CreateView):
	model = FoodItems
	fields = ['name', 'serving', 'calories', 'fat', 'carbs', 'protein']
	template_name = 'tutorial/addfooditem.html'
