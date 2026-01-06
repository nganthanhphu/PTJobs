from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

r = DefaultRouter()
r.register('users', views.UserView, basename='user')
r.register('companies', views.CompanyView, basename='company')
r.register('candidates', views.CandidateView, basename='candidate')
r.register('reviews', views.ReviewView, basename='review')
urlpatterns = [
    path('', include(r.urls)),
]