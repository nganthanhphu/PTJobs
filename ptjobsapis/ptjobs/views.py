from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from ptjobs.serializers import ResumeSerializer, FollowSerializer, UserSerializer, JobPostSerializer, JobCategorySerializer
from ptjobs.models import Resume, Follow, JobPost, JobCategory

class UserViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'], url_path='current-user')
    def current_user(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], url_path='current-user')
    def update_current_user(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrentUserResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class CurrentUserFollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
class JobPostViewSet(viewsets.ModelViewSet):
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['get', 'post', 'delete', 'head', 'options', 'patch']

    def get_queryset(self):
        return JobPost.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()
        
class JobCategoryViewSet(viewsets.ViewSet):
    serializer_class = JobCategorySerializer
    http_method_names = ['get', 'head', 'options']

    def list(self, request):
        categories = JobCategory.objects.all().order_by('name')
        serializer = JobCategorySerializer(categories, many=True)
        return Response(serializer.data)