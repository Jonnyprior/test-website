from django.shortcuts import render, get_object_or_404
from django_tables2 import RequestConfig
from .models import FoodItems
from .models import MealBlock, MealSchedulePerDay
from .tables import FoodItemsTable
from django.views.generic import CreateView, DetailView, ListView
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

#from django_datatables_view import XEditableDatatableView
#import datatableview
#from datatableview import Datatable, ValuesDatatable, columns, SkipRecord
#from datatableview.views import DatatableView, XEditableDatatableView
#from datatableview import helpers
from .forms import AddFoodItemForm, AddMealByUserForm, DeleteFoodItemForm, DeleteMealItemForm

#from .forms import AddFoodItemForm


# Create your views here.

# TODO:
	# Allow fooditems to be edited, deleted - DONE
	# Allow meals to be edited, and deleted - DONE
	# Dynamically add fooditem meal total during meal block creation/editing
	# Create way of listing meals against a certain day - how best to display this?
	# Add 'module' to indicate workout time
	# Allow anonymous users the ability to act like normal user and POST

	# Extra: Pull nutrional data live from Google when adding
	# Extra: Add more columns, salt, sugar etc.
	# Extra: Graph food against energy levels (when best to workout)

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

	# Currently just gets total. Need to display each mealblock too?
	# Works:testobjects = MealSchedulePerDay.objects.filter(user=request.user)
	# Works:test = testobjects.values('meal_schedule_name').annotate(TotalCal=Sum('meal_block__food_item__calories'))

	#test = MealSchedulePerDay.objects.get_total_nutrition_value() # Not user specific. Need to alter Manager
	userDayObjects = MealSchedulePerDay.objects.filter(user=request.user)
	userDayMeals = userDayObjects.values('meal_block').annotate(calories=Sum('meal_block__food_item__calories'), fat=Sum('meal_block__food_item__fat'), carbs=Sum('meal_block__food_item__carbs'), protein=Sum('meal_block__food_item__protein'))

	return render(
		request,
		'tutorial/view_meal_by_user.html',
		context={'userMealObjects': userMealObjects,'userMealData': userMealData, 'test': userDayMeals},
	)

@login_required
def ViewDayMealsByUser(request):
	userDayObjects = MealSchedulePerDay.objects.filter(user=request.user)
	#userMealBlockObjects = MealSchedulePerDay.objects.filter(user=request.user, meal_block__meal_name='Monday')
	#userMealBlockObjects = userDayObjects
	userDayMeals = userDayObjects.values('meal_block__meal_name').annotate(calories=Sum('meal_block__food_item__calories'), fat=Sum('meal_block__food_item__fat'), carbs=Sum('meal_block__food_item__carbs'), protein=Sum('meal_block__food_item__protein'))
	userMealBlocks = []
	for meals in userDayObjects:
		userMealBlocks = meals.meal_block.all()

	return render(
		request,
		'tutorial/view_day_meals_by_user.html',
		context={'userDayObjects': userDayObjects,'userDayMeals': userDayMeals, 'userMealBlocks':userMealBlocks},
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
def EditFoodItemByUser(request, pk):
	"""
	View function to edit specific fooditem by users
	"""
	user_food_item=get_object_or_404(FoodItems, pk=pk)
	form = AddFoodItemForm(request.POST or None, instance=user_food_item)
	# Forces only linked user to edit page (not very elegant)
	if not user_food_item.user == request.user:
		raise ValueError("You do not have permission to edit this - Incorrect user")

	if request.method == 'POST' and form.is_valid():
		user_food_item.save()
		return HttpResponseRedirect(user_food_item.get_absolute_url())

	else:
		# Populates with current values
		form = AddFoodItemForm(instance=user_food_item)

	return render(request, 'tutorial/addfooditem.html', {'form': form})

@login_required
def DeleteFoodItemByUser(request, pk):
	"""
	View function to delete specific fooditem by users
	"""
	user_food_item=get_object_or_404(FoodItems, pk=pk)
	form = DeleteFoodItemForm(request.POST or None, instance=user_food_item)
	# Forces only linked user to edit page (not very elegant)
	if not user_food_item.user == request.user:
		raise ValueError("You do not have permission to delete this - Incorrect user")

	if request.method == 'POST' and form.is_valid():
		user_food_item.delete()
		return HttpResponseRedirect(user_food_item.get_absolute_url())

	else:
		# Populates with current values
		form = DeleteFoodItemForm(instance=user_food_item)

	return render(request, 'tutorial/delete_food_item_by_user.html',
		{'form': form})


@login_required
def AddMealByUser(request):
	if request.method == 'POST':
		form = AddMealByUserForm(request.user, request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			form.save_m2m() # Saves relationship field too

			return HttpResponseRedirect(instance.get_absolute_url())
	else:
		form = AddMealByUserForm(request.user)

	return render(request, 'tutorial/addfooditem.html', {'form': form})

@login_required
def EditMealItemByUser(request, pk):
		"""
		View function to edit specific meals by users
		"""
		user_meal_item=get_object_or_404(MealBlock, pk=pk)
		form = AddMealByUserForm(request.user, request.POST or None, instance=user_meal_item)
		# Forces only linked user to edit page
		if not user_meal_item.user == request.user:
			raise ValueError("You do not have permission to edit this - Incorrect user")

		if request.method == 'POST' and form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(user_meal_item.get_absolute_url())

		else:
			# Populates with current values
			form = AddMealByUserForm(request.user, instance=user_meal_item)

		return render(request, 'tutorial/addfooditem.html', {'form': form})

@login_required
def DeleteMealItemByUser(request, pk):
	"""
	View function to delete specific meal by users
	"""
	user_meal_item=get_object_or_404(MealBlock, pk=pk)
	form = DeleteMealItemForm(request.POST or None, instance=user_meal_item)
	# Forces only linked user to edit page (not very elegant)
	if not user_meal_item.user == request.user:
		raise ValueError("You do not have permission to delete this - Incorrect user")

	if request.method == 'POST' and form.is_valid():
		user_meal_item.delete()
		return HttpResponseRedirect(user_meal_item.get_absolute_url())

	else:
		# Populates with current values
		form = DeleteMealItemForm(instance=user_meal_item)

	return render(request, 'tutorial/delete_food_item_by_user.html',
		{'form': form})

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


# class editabletable(XEditableDatatableView):
#     model = FoodItems
#     template_name = 'tutorial/customtable.html'
#     datatable_options = {
#         'columns': [
# 			("Name", 'name', helpers.make_xeditable),
#             ("Serving", 'serving', helpers.make_xeditable),
#             ("Calories", 'calories', helpers.make_xeditable),
#             ("Fat", 'fat', helpers.make_xeditable),
#         ],
#     }

#class ZeroConfigTable(DatatableView):
#	model = FoodItems
