from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import FoodItems
from .models import MealBlock
from .tables import FoodItemsTable
from django.views.generic import CreateView, DetailView, ListView
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

#from django_datatables_view import XEditableDatatableView
import datatableview
#from datatableview import Datatable, ValuesDatatable, columns, SkipRecord
from datatableview.views import DatatableView, XEditableDatatableView
from datatableview import helpers
from .forms import AddFoodItemForm, AddMealByUserForm

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

	# https://stackoverflow.com/questions/42820728/filter-a-drop-down-django-form-element-based-on-a-value-selected-before

	# Possible table: https://djangopackages.org/packages/p/django-jinja-knockout/
	# Maybe more suitable: https://github.com/pivotal-energy-solutions/django-datatable-view

@login_required
def FoodItemsByUser(request):
	userinfo = FoodItems.objects.filter(user=request.user)

	return render(
		request,
		'tutorial/fooditem_list_by_user.html',
		context={'userinfo': userinfo},
	)

@login_required
def ViewMealByUser(request):
	userMealObjects = MealBlock.objects.filter(user=request.user)
	userMealData = userMealObjects.values('meal_name').annotate(calories=Sum('food_item__calories'), fat=Sum('food_item__fat'), carbs=Sum('food_item__carbs'), protein=Sum('food_item__protein'))

	return render(
		request,
		'tutorial/view_meal_by_user.html',
		context={'userMealObjects': userMealObjects,'userMealData': userMealData},
	)



@login_required
def AddFoodItemByUser(request):
	if request.method == 'POST':
		form = AddFoodItemForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			#name = form.cleaned_data['name']
			#serving = form.cleaned_data['serving']

			return HttpResponseRedirect(instance.get_absolute_url())
	else:
		form = AddFoodItemForm()

	return render(request, 'tutorial/addfooditem.html', {'form': form})

@login_required
def AddMealByUser(request):
	if request.method == 'POST':
		form = AddMealByUserForm(request.user, request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			form.save_m2m()
			#https://docs.djangoproject.com/en/2.0/topics/forms/modelforms/
			# Currently does nothing with data - No Fooditems are saved

			return HttpResponseRedirect(instance.get_absolute_url())
	else:
		form = AddMealByUserForm(request.user)

	return render(request, 'tutorial/addfooditem.html', {'form': form})



def DisplayMeal(request):
	mealandfooditem = MealBlock.objects.all()

	alldata = {}
	alldata = MealBlock.objects.values('meal_name').annotate(calories=Sum('food_item__calories'), fat=Sum('food_item__fat'), carbs=Sum('food_item__carbs'), protein=Sum('food_item__protein'))

	# Look into displaying each meal (via pk)
#	https://djangobook.com/advanced-models/

	#https://docs.djangoproject.com/en/2.0/topics/auth/customizing/
	#https://docs.djangoproject.com/en/2.0/topics/http/sessions/

	#https://github.com/danfairs/django-lazysignup
	#https://github.com/bugov/django-custom-anonymous

	return render(
		request,
		'tutorial/display_meal.html',
		context={'mealandfood': mealandfooditem, 'alldata': alldata},
	)


# Creates a generic view to submit new food items to website
class AddFoodItemView(CreateView):
	model = FoodItems
	fields = ['name', 'serving', 'calories', 'fat', 'carbs', 'protein']
	template_name = 'tutorial/addfooditem.html'

class AddMealView(CreateView):
	model = MealBlock
	fields = ['meal_name', 'food_item']
	template_name = 'tutorial/addfooditem.html'
	# Add custom template - use view to name meal then drop down for selecting an already created food?


class editabletable(XEditableDatatableView):
    model = FoodItems
    template_name = 'tutorial/customtable.html'
    datatable_options = {
        'columns': [
			("Name", 'name', helpers.make_xeditable),
            ("Serving", 'serving', helpers.make_xeditable),
            ("Calories", 'calories', helpers.make_xeditable),
            ("Fat", 'fat', helpers.make_xeditable),
        ],
    }

class ZeroConfigTable(DatatableView):
	model = FoodItems
