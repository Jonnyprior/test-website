from django.db import models
from django.urls import reverse
from django.forms import ModelForm
from django.contrib.auth.models import User

# Create your models here.

class FoodItems(models.Model):
	name = models.CharField(max_length=100, verbose_name='Food Item')
	serving = models.CharField(max_length=100, default='', verbose_name="Serving")
	calories = models.FloatField(default=0, verbose_name="Calories")
	fat = models.FloatField(default=0, verbose_name="Fat")
	carbs = models.FloatField(default=0, verbose_name="Carbs")
	protein = models.FloatField(default=0, verbose_name="Protein")
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return self.name

	# Returns to main page once POST has been successful
	def get_absolute_url(self):
		return reverse('fooditem')


class MealBlock(models.Model):
	meal_name = models.CharField(max_length=100, default="My Meal", verbose_name="Meal Name")
	food_item = models.ManyToManyField(FoodItems)

	def __str__(self):
		return self.meal_name

	def get_absolute_url(self):
		return reverse('fooditem')
