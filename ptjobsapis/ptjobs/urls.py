from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ptjobs import views

r = DefaultRouter()
r.register(r'user', views.UserViewSet, basename='current-user')
r.register(r'resumes', views.CurrentUserResumeViewSet, basename='user-resumes')
r.register(r'following', views.CurrentUserFollowViewSet, basename='user-follows')

urlpatterns = [
    path('', include(r.urls))
]