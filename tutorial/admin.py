from django.contrib import admin

from .models import FoodItems
from .models import MealBlock
from .models import MealSchedulePerDay

#@admin.register(FoodItems)
#class FoodItemsAdmin(admin.ModelAdmin):
#    list_display = ('name', 'serving', 'calories')



admin.site.register(FoodItems)
admin.site.register(MealBlock)
admin.site.register(MealSchedulePerDay)
