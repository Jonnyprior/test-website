from django.contrib import admin

from .models import FoodItems
from .models import MealBlock

#@admin.register(FoodItems)
#class FoodItemsAdmin(admin.ModelAdmin):
#    list_display = ('name', 'serving', 'calories')



admin.site.register(FoodItems)
admin.site.register(MealBlock)
