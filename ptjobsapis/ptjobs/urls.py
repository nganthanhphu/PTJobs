from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

r = DefaultRouter()
r.register(r'user', views.UserView, basename='current-user')
r.register(r'companies', views.CompanyViewSet, basename='companies')
r.register(r'following', views.CurrentUserFollowViewSet, basename='user-follows')
r.register(r'jobposts', views.JobPostViewSet, basename='job-posts')
r.register(r'job-categories', views.JobCategoryViewSet, basename='job-categories')
r.register(r'applications', views.ApplicationViewSet, basename='applications')

urlpatterns = [
    path('', include(r.urls))
]