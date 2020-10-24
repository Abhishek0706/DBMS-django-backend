from django.contrib import admin
from django.urls import path
from expense import views

urlpatterns = [
    path('', views.ExpenseView.as_view(), name='index') ,
   path('add', views.ExpenseAdd.as_view(), name='add')
    ]