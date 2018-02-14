from django.shortcuts import render
from . import models


def meal_table(request):
	return render(request, "mealtable/fooditem.html", {})
