from django.urls import path
from django.conf.urls import url
from . import views
#from tutorial.views import AddFoodItemForm

urlpatterns = [
	path('', views.fooditem, name='fooditem'),
	path('addfooditem/', views.AddFoodItemView.as_view(), name='AddFoodItemView'),
	path('add_food_items', views.AddFoodItemByUser, name='AddFoodItemByUser'),
	path('add_meal_by_user', views.AddMealByUser, name='AddMealByUser'),
	path('addmeal', views.AddMealView.as_view(), name='AddMeal'),
	path('display_meal', views.DisplayMeal, name="DisplayMeal"),
	path('my_food_items', views.FoodItemsByUser, name='FoodItemsByUser'),
	path('my_meals', views.ViewMealByUser, name='ViewMealByUser'),
	path('edit/<int:pk>', views.EditFoodItemByUser, name='EditFoodItemByUser'),
	path('delete/<int:pk>', views.DeleteFoodItemByUser, name='DeleteFoodItemByUser'),
	path('edit/meal/<int:pk>', views.EditMealItemByUser, name='EditMealItemByUser'),
	path('delete/meal/<int:pk>', views.DeleteMealItemByUser, name='DeleteMealItemByUser'),
	path('my_day_meals', views.ViewDayMealsByUser, name='ViewDayMealsByUser'),
]
