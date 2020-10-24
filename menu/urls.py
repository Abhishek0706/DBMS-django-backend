from django.contrib import admin
from django.urls import path
from menu import views

urlpatterns = [
    path('', views.MenuByDay.as_view(), name='day'),
    path('add', views.MenuAdd.as_view(), name='add')
]
