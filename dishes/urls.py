from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('dishes/', views.dish_list, name='dish_list'),
    path('dishes/details/<int:id>/', views.dish_detail, name='dish_detail'),
]

