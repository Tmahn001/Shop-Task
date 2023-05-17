from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_list, name='shop_list'),
    path('create/', views.shop_create, name='shop_create'),
    path('update/<int:pk>/', views.shop_update, name='shop_update'),
    path('search/', views.shop_search, name='shop_search'),
]
