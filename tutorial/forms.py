import django_tables2 as tables
from .models import FoodItems, MealBlock
from django.views.generic.edit import CreateView
from django import forms

class FoodItemsTable(tables.Table):
	class Meta:
		model = FoodItems
		template_name = 'django_tables2/bootstrap.html'

class AddFoodItemForm(forms.ModelForm):
	class Meta:
		model = FoodItems
		fields = ['name', 'serving', 'calories', 'fat', 'carbs', 'protein']

class AddMealByUserForm(forms.ModelForm):
	class Meta:
		model = MealBlock
		fields = ['meal_name', 'food_item']
