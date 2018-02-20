from django.db import models

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

	def get_list_of_fields(self):
		return [self.name, self.serving, self.calories, self.fat, self.carbs, self.protein]
