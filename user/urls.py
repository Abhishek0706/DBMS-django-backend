from django.contrib import admin
from django.urls import path
from user import views

# 1. Add/update worker
# 2. Add/update student
# 5. View all students
# 6. View all workers


urlpatterns = [
    path('student/', views.get_student, name='get_student'),
    path('student/add/', views.add_student, name='add_student'),
    path('worker/', views.get_worker, name='get_worker'),
    path('worker/add/', views.add_worker, name='add_worker'),
    path('workerrole/', views.get_workerrole, name='get_workerrole'),
    path('workerrole/add/', views.add_workerrole, name='add_workerrole'),
    path('workerrole/del/', views.del_workerrole, name='del_workerrole'),
    path('workerrole/update/', views.update_workerrole, name='update_workerrole'),
    path('login/', views.get_login_info, name='get_login_info'),
]
