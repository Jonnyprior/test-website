from django.db import models


class FoodItemTable(models.Model):
	food_item = models.CharField(max_length=200)
	serving = models.CharField(max_length=200)
	calorie = models.FloatField()
	fat = models.FloatField()
	carbs = models.FloatField()
	protein = models.FloatField()
	
	def __str__(self):
		return self.food_item