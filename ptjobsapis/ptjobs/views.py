import json
from django.forms import ValidationError
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, generics, parsers, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from . import models
from . import serializers
from .perms import IsCompanyUser, IsCompanyImageOwner, IsReviewOwner
from .utils import RoleMapper


class UserView(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.select_related('candidate_profile', 'company_profile').all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        profile_data = data.pop('profile', None)
        if isinstance(profile_data, list):
            profile_data = profile_data[0]
        profile_data = json.loads(profile_data) if profile_data and isinstance(profile_data, str) else None

        s = UserSerializer(data=data)
        s.is_valid(raise_exception=True)
        user = s.save()
        res_data = s.data

        if profile_data:
            serializer_class = RoleMapper.get_serializer(user.role)
            if serializer_class:
                p = serializer_class(data=profile_data)
                p.is_valid(raise_exception=True)
                p.save(user=user)
                res_data['profile'] = p.data
            else:
                raise ValidationError("This user type cannot have a profile")

        return Response(res_data, status=status.HTTP_201_CREATED)

    @action(methods=['get', 'patch'], url_path='current-user', detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def get_current_user(self, request):
        user = request.user

        with transaction.atomic():
            if request.method.__eq__('PATCH'):
                data = request.data.copy()

                profile_data = data.pop('profile', None)
                if isinstance(profile_data, list):
                    profile_data = profile_data[0]
                profile_data = json.loads(profile_data) if profile_data and isinstance(profile_data, str) else None

                s = serializers.UserSerializer(user, data=data, partial=True)
                s.is_valid(raise_exception=True)
                s.save()

                if profile_data:
                    serializer_class = RoleMapper.get_serializer(user.role)
                    if serializer_class:
                        profile = user.profile
                        p = serializer_class(profile, data=profile_data, partial=True)
                        p.is_valid(raise_exception=True)
                        p.save()
                    else:
                        raise ValidationError("This user type cannot have a profile")
        res_data = serializers.UserSerializer(user).data

        profile = None
        if user.profile:
            serializer_class = RoleMapper.get_serializer(user.role)
            if serializer_class:
                profile = serializer_class(user.profile).data
            else:
                raise NotFound("This user type does not have a profile")
        res_data['profile'] = profile

        return Response(res_data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post', 'get'], url_path='current-user/resumes',
            permission_classes=[permissions.IsAuthenticated], parser_classes=[MultiPartParser, FormParser])
    def resumes(self, request):
        try:
            candidate_profile = request.user.candidate_profile
        except AttributeError:
            return Response({'detail': 'User does not have a candidate profile'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
        if request.method == 'POST':
            serializer = ResumeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(candidate=candidate_profile)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        resumes = Resume.objects.filter(candidate=candidate_profile).order_by('-created_at')
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], url_path='current-user/resumes/(?P<pk>[^/.]+)',
            permission_classes=[permissions.IsAuthenticated])
    def delete_resume_detail(self, request, pk=None):
        try:
            candidate_profile = request.user.candidate_profile
            resume = Resume.objects.get(pk=pk, candidate=candidate_profile)
        except AttributeError:
            return Response({'detail': 'User does not have a candidate profile'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        except Resume.DoesNotExist:
            return Response({'detail': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)
        
        resume.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'], url_path='current-user/applications',
            permission_classes=[permissions.IsAuthenticated])
    def applications(self, request):
        user = request.user
        if user.role == 'CANDIDATE':
            applications = Application.objects.filter(candidate__user=user).order_by('-created_at')
        elif user.role == 'COMPANY':
            applications = Application.objects.filter(job_post__company__user=user).order_by('-created_at')
        else:
            return Response({'detail': 'User role is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path='current-user/images',
            permission_classes=[permissions.IsAuthenticated], parser_classes=[MultiPartParser, FormParser])
    def upload_image(self, request):
        try:
            company_profile = request.user.company_profile
        except AttributeError:
            return Response({'detail': 'User does not have a company profile'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CompanyImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=company_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['delete'], url_path='current-user/images/(?P<pk>[^/.]+)',
            permission_classes=[permissions.IsAuthenticated])
    def delete_image(self, request, pk=None):
        try:
            company_profile = request.user.company_profile
            image = CompanyImage.objects.get(pk=pk, company=company_profile)
        except AttributeError:
            return Response({'detail': 'User does not have a company profile'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        except CompanyImage.DoesNotExist:
            return Response({'detail': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
        
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
        
class UserFollowViewSet(viewsets.ModelViewSet):
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
    
class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['get', 'post', 'delete', 'head', 'options', 'patch']

    def get_queryset(self):
        return Application.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()


class CompanyView(viewsets.ViewSet, generics.RetrieveAPIView):
    serializer_class = serializers.CompanyProfileSerializer
    queryset = models.CompanyProfile.objects.filter(active=True).select_related('user').prefetch_related('images')

    @action(methods=['get'], url_path='reviews', detail=True)
    def get_reviews(self, request, pk):
        company = self.get_object()
        reviews = models.Review.objects.filter(
            application__job_post__company=company,
            user__role=models.User.Role.CANDIDATE,
            active=True
        ).select_related('user', 'user__candidate_profile')
        return Response(serializers.ReviewSerializer(reviews, many=True).data, status=status.HTTP_200_OK)


class CandidateView(viewsets.ViewSet, generics.RetrieveAPIView):
    serializer_class = serializers.CandidateProfileSerializer
    queryset = models.CandidateProfile.objects.select_related('user').filter(active=True)

    @action(methods=['get'], url_path='reviews', detail=True)
    def get_reviews(self, request, pk):
        candidate = self.get_object()
        reviews = models.Review.objects.filter(
            application__candidate=candidate,
            user__role=models.User.Role.COMPANY,
            active=True
        ).select_related('user', 'user__company_profile')
        return Response(serializers.ReviewSerializer(reviews, many=True).data, status=status.HTTP_200_OK)


class ReviewView(viewsets.ViewSet, generics.DestroyAPIView):
    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.filter(active=True)
    permission_classes = [IsReviewOwner]

    def partial_update(self, request, pk=None):
        review = self.get_object()
        s = self.get_serializer(review, data=request.data, partial=True)
        s.is_valid(raise_exception=True)
        s.save()

        return Response(s.data, status=status.HTTP_200_OK)