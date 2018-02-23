from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import FoodItems
from .models import MealBlock
from .models import MealBlockForm
from .tables import FoodItemsTable
from django.views.generic import CreateView

#from django_datatables_view import XEditableDatatableView
import datatableview
#from datatableview import Datatable, ValuesDatatable, columns, SkipRecord
from datatableview.views import DatatableView, XEditableDatatableView
from datatableview import helpers

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


def AddMealViewWithModelForm(request):
	if request.method == 'POST':
		form  = MealBlockForm(request.POST)

		if form.is_valid():
			# Do something here
			return HttpResponseRedirect('/fooditem')

	else:
		form = MealBlockForm()

	return render(request, 'tutorial/addfooditem.html', {'form': form})

# Creates a generic view to submit new food items to website
class AddFoodItemView(CreateView):
	model = FoodItems
	fields = ['name', 'serving', 'calories', 'fat', 'carbs', 'protein']
	template_name = 'tutorial/addfooditem.html'

class AddMealView(CreateView):
	model = MealBlock
	fields = ['meal_name', 'name', 'serving', 'calories', 'fat', 'carbs', 'protein']
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
