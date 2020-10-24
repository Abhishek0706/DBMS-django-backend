from django.contrib import admin
from django.urls import path
from wastage import views

urlpatterns = [
   path('', views.DailyWastageView.as_view(), name='index') ,
   path('add', views.DailyWastageAdd.as_view(), name='add')
]

