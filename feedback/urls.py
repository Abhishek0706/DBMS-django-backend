from django.contrib import admin
from django.urls import path
from feedback import views

urlpatterns = [
    path('', views.get_feedback, name='get_feedback'),
    path('add', views.add_feedback, name='add_feedback'),
    path('del', views.del_feedback, name='del_feedback'),
]
