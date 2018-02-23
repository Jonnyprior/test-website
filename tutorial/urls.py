from django.urls import path
from django.conf.urls import url
from . import views
#from tutorial.views import AddFoodItemForm

urlpatterns = [
	path('', views.fooditem, name='fooditem'),
	path('addfooditem/', views.AddFoodItemView.as_view(), name='AddFoodItemView'),
	path('addmeal', views.AddMealView.as_view(), name='AddMeal'),
	path('addmealnew', views.AddMealViewWithModelForm, name='AddMealViewWithModelForm'),
	path('editabletable/', views.editabletable.as_view(), name='editabletable'),
	path('zero/', views.ZeroConfigTable.as_view(), name='zeroconfig'),
]
