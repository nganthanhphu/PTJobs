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
    
    @action(detail=False, methods=['post', 'get'], url_path='current-user/resumes')
    def resumes(self, request):
        candidate_profile = request.user.candidate_profile
        
        if request.method == 'POST':
            serializer = ResumeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(candidate=candidate_profile)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        resumes = Resume.objects.filter(candidate=candidate_profile).order_by('-created_at')
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], url_path='current-user/resumes/(?P<pk>[^/.]+)')
    def delete_resume_detail(self, request, pk=None):
        try:
            candidate_profile = request.user.candidate_profile
            resume = Resume.objects.get(pk=pk, candidate=candidate_profile)
        except Resume.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        resume.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CurrentUserResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        candidate_profile = self.request.user.candidate_profile
        return Resume.objects.filter(candidate=candidate_profile).order_by('-created_at')

    def perform_create(self, serializer):
        candidate_profile = self.request.user.candidate_profile
        serializer.save(candidate=candidate_profile)
        
class CurrentUserFollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        candidate_profile = self.request.user.candidate_profile
        return Follow.objects.filter(candidate=candidate_profile).order_by('-created_at')

    def perform_create(self, serializer):
        candidate_profile = self.request.user.candidate_profile
        serializer.save(candidate=candidate_profile)
    
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