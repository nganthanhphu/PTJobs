from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ptjobs import views

r = DefaultRouter()
r.register('users', views.UserView, basename='user')

urlpatterns = [
    path('', include(r.urls)),
]