from django.contrib import admin

from .models import FoodItems
from .models import MealBlock

admin.site.register(FoodItems)
admin.site.register(MealBlock)
