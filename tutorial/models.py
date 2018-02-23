from django.db import models
from django.urls import reverse
from django.forms import ModelForm

# Create your models here.
class FoodItems(models.Model):
	name = models.CharField(max_length=100, verbose_name='Food Item')
	serving = models.CharField(max_length=100, default='', verbose_name="Serving")
	calories = models.FloatField(default=0, verbose_name="Calories")
	fat = models.FloatField(default=0, verbose_name="Fat")
	carbs = models.FloatField(default=0, verbose_name="Carbs")
	protein = models.FloatField(default=0, verbose_name="Protein")

	def __str__(self):
		return self.name

	# Returns to main page once POST has been successful
	def get_absolute_url(self):
		return reverse('fooditem')

class MealBlock(models.Model):
	meal_name = models.CharField(max_length=100, default='MealBlock', verbose_name="Meal Name")
	fooditems = models.ManyToManyField(FoodItems)

	def __str__(self):
		return self.meal_name



class MealBlockForm(ModelForm):
	class Meta:
		model = MealBlock
		#meal_name = models.CharField(max_length=100, default='MealBlock', verbose_name="Meal Name")
		#fooditems = models.ManyToManyField(FoodItems, related_name='+')
		fields = ['meal_name', 'fooditems']
