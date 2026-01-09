import datetime
import json

from django.db import transaction
from django.db.models import Prefetch
from django.forms import ValidationError
from rest_framework import viewsets, generics, parsers, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from . import serializers, perms, paginators, utils
from .models import User, Resume, Application, CompanyImage, Follow, JobPost, JobCategory, CompanyProfile, \
    CandidateProfile, Review, WorkTime
from .perms import IsReviewOwner
from .serializers import UserSerializer, ResumeSerializer, ApplicationSerializer, \
    CompanyImageSerializer, JobPostSerializer, JobCategorySerializer, WorkTimeSerializer, ReviewSerializer
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
        if not profile_data:
            raise ValidationError("Profile data is required")

        s = UserSerializer(data=data)
        s.is_valid(raise_exception=True)
        user = s.save()
        res_data = s.data

        serializer_class = RoleMapper.get_serializer(user.role)
        if serializer_class:
            profile_data['user'] = user.id
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
                raise NotFound("This user type cannot and does not have a profile")
        res_data['profile'] = profile

        return Response(res_data, status=status.HTTP_200_OK)


class ResumeViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [perms.IsCandidateUser, perms.IsResumeOwner]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = paginators.ItemPaginator
    queryset = Resume.objects.filter(active=True).order_by('-created_at')

    def get_queryset(self):
        query = self.queryset
        try:
            candidate_profile = self.request.user.candidate_profile
            query = query.filter(candidate=candidate_profile)
            return query
        except AttributeError:
            raise PermissionDenied()

    def create(self, request):
        try:
            candidate_profile = request.user.candidate_profile
        except AttributeError:
            raise PermissionDenied()

        serializer = ResumeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(candidate=candidate_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            candidate_profile = request.user.candidate_profile
            resume = Resume.objects.get(pk=pk, candidate=candidate_profile)
        except AttributeError:
            return PermissionDenied()
        except Resume.DoesNotExist:
            raise NotFound('Resume not found')

        setattr(resume, 'active', False)
        resume.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CompanyImageViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    serializer_class = CompanyImageSerializer
    permission_classes = [perms.IsCompanyUser, perms.IsCompanyImageOwner]
    parser_classes = [MultiPartParser, FormParser]
    queryset = CompanyImage.objects.filter(active=True)

    def get_queryset(self):
        query = self.queryset
        try:
            company_profile = self.request.user.company_profile
            query = query.filter(company=company_profile)
            return query
        except AttributeError:
            return query.none()

    def create(self, request):
        try:
            company_profile = request.user.company_profile
        except AttributeError:
            raise PermissionDenied()
        data = request.data.copy()
        data['company'] = company_profile.id
        serializer = CompanyImageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            company_profile = request.user.company_profile
            image = CompanyImage.objects.get(pk=pk, company=company_profile)
        except AttributeError:
            raise PermissionDenied()
        except CompanyImage.DoesNotExist:
            raise NotFound('Company image not found')

        image.delete()
        if CompanyImage.objects.filter(company=company_profile).count() < 3:
            company_profile.active = False
            company_profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(viewsets.GenericViewSet, generics.DestroyAPIView):
    serializer_class = serializers.FollowSerializer
    permission_classes = [perms.IsCandidateUser, perms.IsFollowingOwner]
    queryset = Follow.objects.all().order_by('-created_at')

    def list(self, request):
        try:
            candidate_profile = request.user.candidate_profile
        except AttributeError:
            raise PermissionDenied()

        follows = Follow.objects.filter(candidate=candidate_profile).select_related('company',
                                                                                    'company__user').order_by(
            '-created_at')
        serializer = serializers.FollowSerializer(follows, many=True)
        data = serializer.data
        for i in range(len(data)):
            company = follows[i].company
            company_name = company.name
            company_avatar = company.user.avatar.url if company.user.avatar else None
            data[i]['company'] = {
                'name': company_name,
                'avatar': company_avatar
            }

        return Response(data)

    def create(self, request):
        if not request.user.email:
            raise ValidationError("User must have an email to follow companies")
        try:
            candidate_profile = request.user.candidate_profile
        except AttributeError:
            raise PermissionDenied()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(candidate=candidate_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobPostViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    serializer_class = JobPostSerializer
    queryset = JobPost.objects.filter(active=True, company__active=True).select_related('company', 'category').order_by(
        '-created_at')
    pagination_class = paginators.ItemPaginator

    def get_permissions(self):
        if self.action in ['create', 'partial_update', 'destroy']:
            return [perms.IsCompanyUser(), perms.IsJobPostOwner()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = self.queryset

        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        company_id = self.request.query_params.get('company')
        if company_id:
            queryset = queryset.filter(company__id=company_id)

        address = self.request.query_params.get('address')
        if address:
            queryset = queryset.filter(address__icontains=address)

        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')
        if start_time and end_time:
            start_time = datetime.time(hour=(int(start_time)))
            end_time = datetime.time(hour=(int(end_time)))
            queryset = queryset.filter(work_times__start_time__gte=start_time, work_times__end_time__lte=end_time)

        day = self.request.query_params.get('day')
        if day:
            queryset = queryset.filter(work_times__day=day)

        return queryset

    @transaction.atomic
    def create(self, request):

        try:
            company_profile = request.user.company_profile
            if not company_profile.active:
                raise PermissionDenied(
                    'Your account is not activated. Please upload at least three company images and contact support to activate your account.')
        except AttributeError:
            raise PermissionDenied()

        data = request.data.copy()
        work_times_data = data.pop('work_times', [])

        if isinstance(work_times_data, str):
            work_times_data = json.loads(work_times_data)

        serializer = JobPostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        job_post = serializer.save(company=company_profile)

        for work_time in work_times_data:
            work_time_serializer = WorkTimeSerializer(data=work_time)
            work_time_serializer.is_valid(raise_exception=True)
            work_time_serializer.save(job_post=job_post)
        utils.EmailService.notify_via_email(job_post)
        return Response(JobPostSerializer(job_post).data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def partial_update(self, request, pk=None):
        try:
            company_profile = request.user.company_profile
            job_post = JobPost.objects.get(pk=pk, company=company_profile)
        except AttributeError:
            raise PermissionDenied()
        except JobPost.DoesNotExist:
            raise NotFound('Job post not found')

        data = request.data.copy()
        work_times_data = data.pop('work_times', None)

        if isinstance(work_times_data, str):
            work_times_data = json.loads(work_times_data)

        serializer = JobPostSerializer(job_post, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if work_times_data is not None:
            WorkTime.objects.filter(job_post=job_post).delete()
            for work_time_data in work_times_data:
                work_time_serializer = WorkTimeSerializer(data=work_time_data)
                work_time_serializer.is_valid(raise_exception=True)
                work_time_serializer.save(job_post=job_post)

        return Response(JobPostSerializer(job_post).data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            company_profile = request.user.company_profile
            job_post = JobPost.objects.get(pk=pk, company=company_profile)
        except AttributeError:
            raise PermissionDenied()
        except JobPost.DoesNotExist:
            raise NotFound('Job post not found')

        job_post.active = False
        job_post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobCategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = JobCategorySerializer
    queryset = JobCategory.objects.all().order_by('name')


class ApplicationViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    serializer_class = ApplicationSerializer
    pagination_class = paginators.ItemPaginator

    def get_permissions(self):
        if self.action.__eq__('create'):
            return [perms.IsCandidateUser()]
        elif self.action.__eq__('partial_update'):
            return [perms.IsCompanyUser()]
        else:
            return [permissions.IsAuthenticated()]

    def get_queryset(self):
        QUERYSET = {
            'CANDIDATE': Application.objects.filter(active=True, candidate__user=self.request.user).select_related(
                'job_post', 'job_post__company', 'job_post__company__user'),
            'COMPANY': Application.objects.filter(active=True,
                                                  job_post__company__user=self.request.user).select_related('job_post',
                                                                                                            'candidate',
                                                                                                            'candidate__user')
        }
        user = self.request.user
        query = QUERYSET.get(user.role)
        if not query:
            raise PermissionDenied()
        if self.action.__eq__('retrieve'):
            query = query.select_related('resume')
        return query

    def create(self, request):
        try:
            candidate_profile = request.user.candidate_profile
        except AttributeError:
            raise PermissionDenied()

        serializer = ApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(candidate=candidate_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            application = self.get_queryset().get(pk=pk)
        except Application.DoesNotExist:
            raise NotFound('Application not found')
        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        try:
            application = self.get_queryset().get(pk=pk)
        except Application.DoesNotExist:
            raise NotFound('Application not found')

        new_status = request.data.get('status', None)
        if not new_status:
            raise ValidationError({'status field is required'})
        old_status = application.status

        valid_statuses = [choice[0] for choice in Application.JobStatus.choices]
        if new_status not in valid_statuses:
            raise ValidationError('Invalid status value')

        if new_status == old_status:
            return Response(ApplicationSerializer(application).data, status=status.HTTP_200_OK)

        with transaction.atomic():
            job_post = application.job_post

            if new_status == Application.JobStatus.EMPLOYED:
                if job_post.vacancy > 0:
                    job_post.vacancy -= 1
                    job_post.save()
                else:
                    raise ValidationError('No vacancy available')
                application.start_date = datetime.date.today()

            elif new_status == Application.JobStatus.TERMINATED:
                application.end_date = datetime.date.today()
                job_post.vacancy += 1
                job_post.save()

            application.status = new_status
            application.save()

        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], url_path='reviews', detail=True)
    def get_reviews(self, request, pk):
        application = self.get_object()
        reviews = Review.objects.filter(
            application=application,
            active=True
        ).select_related('user', 'user__company_profile', 'user__candidate_profile', 'application', 'parent',
                         'parent__user', 'parent__user__company_profile', 'parent__user__candidate_profile')
        data = serializers.ReviewSerializer(reviews, many=True).data
        for i in range(len(data)):
            reviewer = reviews[i].user
            if reviewer.role == User.Role.COMPANY:
                reviewer_name = reviewer.user.company_profile.name
            else:
                reviewer_name = reviewer.user.get_full_name()
            reviewer_avatar = reviewer.avatar.url if reviewer.avatar else None
            data[i]['user'] = {
                'name': reviewer_name,
                'avatar': reviewer_avatar
            }
            if reviews[i].parent:
                parent_data = ReviewSerializer(reviews[i].parent).data
                data[i]['parent'] = parent_data
                if reviews[i].parent.user.role == User.Role.COMPANY:
                    parent_reviewer_name = reviews[i].parent.user.company_profile.name
                else:
                    parent_reviewer_name = reviews[i].parent.user.get_full_name()
                parent_reviewer_avatar = reviews[i].parent.user.avatar.url if reviews[i].parent.user.avatar else None
                data[i]['parent']['user'] = {
                    'name': parent_reviewer_name,
                    'avatar': parent_reviewer_avatar
                }
        return Response(data, status=status.HTTP_200_OK)


class CompanyView(viewsets.GenericViewSet, generics.RetrieveAPIView):
    serializer_class = serializers.CompanyProfileSerializer
    queryset = CompanyProfile.objects.filter(active=True).select_related('user').prefetch_related(
        Prefetch('images', queryset=CompanyImage.objects.filter(active=True)))

    def retrieve(self, request, *args, **kwargs):
        company = self.get_object()
        data = serializers.CompanyProfileSerializer(company).data
        image_urls = [image.image.url for image in company.images.all()]
        data['avatar'] = company.user.avatar.url if company.user.avatar else None
        data['images'] = image_urls

        if request.user.is_authenticated and request.user.role == User.Role.CANDIDATE:
            candidate_profile = request.user.candidate_profile
            is_followed = Follow.objects.filter(candidate=candidate_profile, company=company).exists()
            data['is_followed'] = is_followed
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['get'], url_path='reviews', detail=True)
    def get_reviews(self, request, pk):
        company = self.get_object()
        reviews = Review.objects.filter(
            application__job_post__company=company,
            user__role=User.Role.CANDIDATE,
            active=True
        ).select_related('user', 'application', 'application__job_post')
        data = serializers.ReviewSerializer(reviews, many=True).data
        for i in range(len(data)):
            job_name = reviews[i].application.job_post.name
            reviewer_name = reviews[i].user.get_full_name()
            reviewer_avatar = reviews[i].user.avatar.url if reviews[i].user.avatar else None
            start_date = reviews[i].application.start_date.strftime('%d/%m/%Y') if reviews[
                i].application.start_date else None
            end_date = reviews[i].application.end_date.strftime('%d/%m/%Y') if reviews[i].application.end_date else None
            data[i]['job_post'] = {
                'name': job_name
            }
            data[i]['user'] = {
                'name': reviewer_name,
                'avatar': reviewer_avatar
            }
            data[i]['application_period'] = {
                'start_date': start_date,
                'end_date': end_date
            }
        return Response(data, status=status.HTTP_200_OK)


class CandidateView(viewsets.GenericViewSet, generics.RetrieveAPIView):
    serializer_class = serializers.CandidateProfileSerializer
    queryset = CandidateProfile.objects.select_related('user').filter(active=True)

    def retrieve(self, request, *args, **kwargs):
        candidate = self.get_object()
        data = serializers.CandidateProfileSerializer(candidate).data
        data['full_name'] = candidate.user.get_full_name()
        data['email'] = candidate.user.email
        data['phone'] = candidate.user.phone
        data['avatar'] = candidate.user.avatar.url if candidate.user.avatar else None
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['get'], url_path='reviews', detail=True)
    def get_reviews(self, request, pk):
        candidate = self.get_object()
        reviews = Review.objects.filter(
            application__candidate=candidate,
            user__role=User.Role.COMPANY,
            active=True
        ).select_related('user', 'user__company_profile')
        data = serializers.ReviewSerializer(reviews, many=True).data
        for i in range(len(data)):
            reviewer_name = reviews[i].user.company_profile.name
            reviewer_avatar = reviews[i].user.avatar.url if reviews[i].user.avatar else None
            data[i]['user'] = {
                'name': reviewer_name,
                'avatar': reviewer_avatar
            }
        return Response(data, status=status.HTTP_200_OK)


class ReviewView(viewsets.GenericViewSet, generics.DestroyAPIView):
    serializer_class = serializers.ReviewSerializer
    queryset = Review.objects.filter(active=True)
    permission_classes = [IsReviewOwner]

    def partial_update(self, request, pk=None):
        review = self.get_object()
        s = self.get_serializer(review, data=request.data, partial=True)
        s.is_valid(raise_exception=True)
        s.save()

        return Response(s.data, status=status.HTTP_200_OK)
