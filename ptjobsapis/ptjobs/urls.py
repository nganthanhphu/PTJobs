from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

r = DefaultRouter()
r.register(r'user', views.UserViewSet, basename='current-user')
r.register(r'resumes', views.CurrentUserResumeViewSet, basename='user-resumes')
r.register(r'following', views.CurrentUserFollowViewSet, basename='user-follows')
r.register(r'jobposts', views.JobPostViewSet, basename='job-posts')
r.register(r'job-categories', views.JobCategoryViewSet, basename='job-categories')

urlpatterns = [
    path('', include(r.urls))
]