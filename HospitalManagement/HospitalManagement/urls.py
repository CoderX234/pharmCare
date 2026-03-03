"""HospitalManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hospital.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('', Index, name='home'),
    path('admin_login/', Login, name='login'),
    path('logout/', logout_admin, name='logout'),
    path('view_doctor/', view_doctor, name='view_doctor'),
    path('add_doctor/', add_doctor, name='add_doctor'),
    path('delete_doctor/<int:pid>/', delete_doctor, name='delete_doctor'),
    path('create_user/', create_user, name='create_user'),
    path('view_users/', view_users, name='view_users'),
    path('edit_user/<int:uid>/', edit_user_role, name='edit_user'),
    path('view_patient/', view_patient, name='view_patient'),
    path('add_patient/', add_patient, name='add_patient'),
    path('delete_patient/<int:pid>/', delete_patient, name='delete_patient'),
    path('view_appointment/', view_appointment, name='view_appointment'),
    path('add_appointment/', add_appointment, name='add_appointment'),
    path('delete_appointment/<int:pid>/', delete_appointment, name='delete_appointment'),
    path('view_prescription/', view_prescription, name='view_prescription'),
    path('add_prescription/', add_prescription, name='add_prescription'),
    path('delete_prescription/<int:pid>/', delete_prescription, name='delete_prescription'),
]
