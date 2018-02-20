from django.urls import path
from django.conf.urls import url
from . import views
#from tutorial.views import AddFoodItemForm

urlpatterns = [
	path('', views.fooditem, name='fooditem'),
	path('addfooditem/', views.AddFoodItemView.as_view(), name='AddFoodItemView'),
]
