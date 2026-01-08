from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

r = DefaultRouter()
r.register('users', views.UserView, basename='user')
r.register('companies', views.CompanyView, basename='company')
r.register('candidates', views.CandidateView, basename='candidate')
r.register('reviews', views.ReviewView, basename='review')
r.register(r'jobposts', views.JobPostViewSet, basename='job-posts')
r.register(r'job-categories', views.JobCategoryViewSet, basename='job-categories')
r.register(r'applications', views.ApplicationViewSet, basename='applications')
r.register(r'resumes', views.ResumeViewSet, basename='resumes')
r.register(r'company-images', views.CompanyImageViewSet, basename='company-images')
r.register(r'following', views.FollowViewSet, basename='following')
urlpatterns = [
    path('', include(r.urls))
]