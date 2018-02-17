from django.db import models

# Create your models here.
class FoodItems(models.Model):
	name = models.CharField(max_length=100, verbose_name='Food Item')