from django.urls import path

import job
from . import views

urlpatterns = [
    path('', job.views.home, name='home'),
    path('register', job.views.register, name='register'),
    path('user_login', job.views.user_login, name='login'),
    path('job_list', job.views.job_list, name='job_list'),
    path('add_job', job.views.add_job, name='add_job'),
    path('logout', job.views.logout, name='logout'),
    path('apply_job/<int:job_id>/', job.views.apply_job, name='apply_job'),
    path('admin_home', job.views.admin_home, name='admin_home'),
    path('user_home', job.views.user_home, name='user_home'),
    path('view_job_list', job.views.view_job_list, name='view_job_list'),
]