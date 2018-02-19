import django_tables2 as tables
from .models import FoodItems

class FoodItemsTable(tables.Table):
	class Meta:
		model = FoodItems
		template_name = 'django_tables2/bootstrap.html'
