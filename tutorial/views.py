from django.shortcuts import render
from .models import FoodItems

# Create your views here.

def fooditem(request):
	return render(request, 'tutorial/fooditem.html', {'fooditem': FoodItems.objects.all()})