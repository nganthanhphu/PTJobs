import datetime
import json

from django.db import transaction
from django.db.models import Prefetch, Count, Q
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
    queryset = User.objects.select_related(
        'candidate_profile', 'company_profile').all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        profile_data = data.pop('profile', None)
        if isinstance(profile_data, list):
            profile_data = profile_data[0]
        try:
            profile_data = json.loads(profile_data) if profile_data and isinstance(
                profile_data, str) else None
        except json.JSONDecodeError:
            raise ValidationError("Invalid profile field")
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
                try:
                    profile_data = json.loads(profile_data) if profile_data and isinstance(
                        profile_data, str) else None
                except json.JSONDecodeError:
                    raise ValidationError("Invalid profile field")

                s = serializers.UserSerializer(user, data=data, partial=True)
                s.is_valid(raise_exception=True)
                s.save()

                if profile_data:
                    serializer_class = RoleMapper.get_serializer(user.role)
                    if serializer_class:
                        profile = user.profile
                        p = serializer_class(
                            profile, data=profile_data, partial=True)
                        p.is_valid(raise_exception=True)
                        p.save()
                    else:
                        raise ValidationError(
                            "This user type cannot have a profile")
        res_data = serializers.UserSerializer(user).data

        profile = None
        if user.profile:
            serializer_class = RoleMapper.get_serializer(user.role)
            if serializer_class:
                profile = serializer_class(user.profile).data
            else:
                raise NotFound(
                    "This user type cannot and does not have a profile")
        res_data['profile'] = profile

        return Response(res_data, status=status.HTTP_200_OK)


class ResumeViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [perms.IsResumeOwner]
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

    def create(self, request, *args, **kwargs):
        try:
            candidate_profile = self.request.user.candidate_profile
        except AttributeError:
            raise PermissionDenied()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(candidate=candidate_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        resume = self.get_object()
        setattr(resume, 'active', False)
        resume.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CompanyImageViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    serializer_class = CompanyImageSerializer
    permission_classes = [perms.IsCompanyImageOwner]
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

    def create(self, request, *args, **kwargs):
        try:
            company_profile = request.user.company_profile
        except AttributeError:
            raise PermissionDenied()
        data = request.data.copy()
        data['company'] = company_profile.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            company_profile = request.user.company_profile
        except AttributeError:
            raise PermissionDenied()
        if CompanyImage.objects.filter(company=company_profile).count() <= 3:
            raise ValidationError(
                "At least three company images are required to keep the account active.")
        image = self.get_object()
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(viewsets.GenericViewSet, generics.DestroyAPIView):
    serializer_class = serializers.FollowSerializer
    permission_classes = [perms.IsFollowingOwner]
    queryset = Follow.objects.all().order_by('-created_at')

    def list(self, request):
        try:
            candidate_profile = self.request.user.candidate_profile
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

    def create(self, request, *args, **kwargs):
        if not request.user.email:
            raise ValidationError(
                "User must have an email to follow companies")
        try:
            candidate_profile = request.user.candidate_profile
        except AttributeError:
            raise PermissionDenied()
        data = request.data.copy()
        data['candidate'] = candidate_profile.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(candidate=candidate_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobPostViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = JobPostSerializer
    queryset = JobPost.objects.filter(active=True, company__active=True).order_by(
        '-created_at').prefetch_related('work_times')
    pagination_class = paginators.ItemPaginator

    def get_permissions(self):
        if self.action in ['create', 'partial_update', 'destroy']:
            return [perms.IsJobPostOwner()]
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
            queryset = queryset.filter(
                work_times__start_time__gte=start_time, work_times__end_time__lte=end_time)

        day = self.request.query_params.get('day')
        if day:
            queryset = queryset.filter(work_times__day=day)

        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):

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
            try:
                work_times_data = json.loads(work_times_data)
            except json.JSONDecodeError:
                raise ValidationError("Invalid work_times field")

        if not work_times_data:
            raise ValidationError("Work time is required")
        data['company'] = company_profile.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        job_post = serializer.save()

        for work_time in work_times_data:
            work_time['job_post'] = job_post.id
        work_time_serializers = WorkTimeSerializer(
            data=work_times_data, many=True)
        work_time_serializers.is_valid(raise_exception=True)
        work_time_serializers.save()
        utils.EmailService.notify_via_email(job_post)
        return Response(JobPostSerializer(job_post).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            job_post = JobPost.objects.prefetch_related('work_times').select_related('company', 'company__user').get(
                pk=pk, active=True, company__active=True)
        except JobPost.DoesNotExist:
            raise NotFound('Job post not found')
        serializer = self.get_serializer(job_post)
        data = serializer.data
        company_name = job_post.company.name
        company_avatar = job_post.company.user.avatar.url if job_post.company.user.avatar else None
        data['company'] = {
            'name': company_name,
            'avatar': company_avatar
        }
        work_times = job_post.work_times.all()
        work_times_data = WorkTimeSerializer(work_times, many=True).data
        data['work_times'] = work_times_data

        return Response(data, status=status.HTTP_200_OK)

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        job_post = self.get_object()
        data = request.data.copy()
        work_times_data = data.pop('work_times', None)
        if isinstance(work_times_data, str):
            try:
                work_times_data = json.loads(work_times_data)
            except json.JSONDecodeError:
                raise ValidationError("Invalid work_times field")

        serializer = JobPostSerializer(job_post, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        job_post = serializer.save()
        if work_times_data:
            WorkTime.objects.filter(job_post=job_post).delete()
            for work_time_data in work_times_data:
                work_time_data['job_post'] = job_post.id
            work_time_serializers = WorkTimeSerializer(
                data=work_times_data, many=True)
            work_time_serializers.is_valid(raise_exception=True)
            work_time_serializers.save()

        return Response(JobPostSerializer(job_post).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        job_post = self.get_object()
        job_post.active = False
        job_post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], url_path='reviews', detail=True)
    def get_reviews(self, request, *args, **kwargs):
        job_post = self.get_object()
        reviews = Review.objects.filter(
            Q(parent__isnull=True, reply__isnull=True) |
            Q(parent__isnull=False),
            application__job_post=job_post,
            active=True
        ).select_related('user', 'user__company_profile', 'parent', 'application',
                         'parent__user', 'parent__user__company_profile').order_by('-created_at')

        paginator = paginators.ItemPaginator()
        paginated_reviews = paginator.paginate_queryset(reviews, request)

        data = serializers.ReviewSerializer(paginated_reviews, many=True).data
        for i in range(len(data)):
            reviewer = paginated_reviews[i].user
            if reviewer.role == User.Role.COMPANY:
                reviewer_name = reviewer.company_profile.name
            else:
                reviewer_name = reviewer.get_full_name()
            reviewer_avatar = reviewer.avatar.url if reviewer.avatar else None
            data[i]['user'] = {
                'name': reviewer_name,
                'avatar': reviewer_avatar
            }
            start_date = paginated_reviews[i].application.start_date.strftime('%d/%m/%Y') if paginated_reviews[
                i].application.start_date else None
            end_date = paginated_reviews[i].application.end_date.strftime('%d/%m/%Y') if paginated_reviews[
                i].application.end_date else None
            data[i]['application'] = {
                'start_date': start_date,
                'end_date': end_date
            }

            if paginated_reviews[i].parent:
                reply = data[i]
                parent_data = ReviewSerializer(
                    paginated_reviews[i].parent).data
                data[i] = parent_data
                if paginated_reviews[i].parent.user.role == User.Role.COMPANY:
                    parent_reviewer_name = paginated_reviews[i].parent.user.company_profile.name
                else:
                    parent_reviewer_name = paginated_reviews[i].parent.user.get_full_name(
                    )
                parent_reviewer_avatar = paginated_reviews[i].parent.user.avatar.url if paginated_reviews[
                    i].parent.user.avatar else None
                data[i]['user'] = {
                    'name': parent_reviewer_name,
                    'avatar': parent_reviewer_avatar
                }
                data[i]['reply'] = reply
        return paginator.get_paginated_response(data)


class JobCategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = JobCategorySerializer
    queryset = JobCategory.objects.all().order_by('name')


class ApplicationViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    serializer_class = ApplicationSerializer
    pagination_class = paginators.ItemPaginator

    def get_permissions(self):
        if self.action.__eq__('create'):
            return [perms.IsCandidateUser()]
        if self.action.__eq__('partial_update'):
            return [perms.IsApplicationBelongToCompanyUser()]
        if self.action.__eq__('destroy'):
            return [perms.IsApplicationOwner()]

        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        QUERYSET = {
            'CANDIDATE': Application.objects.filter(active=True, candidate__user=self.request.user).select_related(
                'job_post', 'job_post__company', 'job_post__company__user').order_by('-created_at'),
            'COMPANY': Application.objects.filter(active=True, job_post__company__user=self.request.user).select_related(
                'job_post', 'candidate', 'candidate__user').order_by('-created_at')
        }
        user = self.request.user
        query = QUERYSET.get(user.role)
        if not query:
            raise PermissionDenied()
        if self.action.__eq__('retrieve'):
            query = query.select_related('resume')
        if self.action.__eq__('create_review'):
            query = query.prefetch_related('reviews')

        status = self.request.query_params.get('status')
        if status:
            query = query.filter(status=status)

        return query

    def candidate_list(self, request, *args, **kwargs):
        applications = self.get_queryset()
        paginator = self.pagination_class()
        paginated_applications = paginator.paginate_queryset(
            applications, request)

        data = self.serializer_class(paginated_applications, many=True).data
        for i in range(len(data)):
            job_post = paginated_applications[i].job_post
            company_name = job_post.company.name
            company_avatar = job_post.company.user.avatar.url if job_post.company.user.avatar else None
            data[i]['job_post'] = {
                'name': job_post.name,
                'company': {
                    'name': company_name,
                    'avatar': company_avatar
                }
            }

        return paginator.get_paginated_response(data)

    def company_list(self, request, *args, **kwargs):
        applications = self.get_queryset()
        paginator = self.pagination_class()
        paginated_applications = paginator.paginate_queryset(
            applications, request)

        data = self.serializer_class(paginated_applications, many=True).data
        for i in range(len(data)):
            candidate = paginated_applications[i].candidate
            candidate_name = candidate.user.get_full_name()
            candidate_avatar = candidate.user.avatar.url if candidate.user.avatar else None
            job_post = paginated_applications[i].job_post
            data[i]['candidate'] = {
                'name': candidate_name,
                'avatar': candidate_avatar
            }
            data[i]['job_post'] = {
                'name': job_post.name
            }

        return paginator.get_paginated_response(data)

    def list(self, request, *args, **kwargs):
        LIST_METHODS = {
            'CANDIDATE': self.candidate_list,
            'COMPANY': self.company_list
        }
        list_method = LIST_METHODS.get(request.user.role)
        if not list_method:
            raise PermissionDenied()
        return list_method(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            candidate_profile = request.user.candidate_profile
        except AttributeError:
            raise PermissionDenied()

        serializer = ApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(candidate=candidate_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def candidate_retrieve(self, request, *args, **kwargs):
        application = self.get_object()
        serializer = ApplicationSerializer(application)
        data = serializer.data
        company_name = application.job_post.company.name
        company_avatar = application.job_post.company.user.avatar.url if application.job_post.company.user.avatar else None
        data['company'] = {
            'name': company_name,
            'avatar': company_avatar
        }
        job_post_name = application.job_post.name
        data['job_post'] = {'name': job_post_name}
        resume_url = application.resume.file.url if application.resume else None
        data['resume'] = resume_url
        return Response(data, status=status.HTTP_200_OK)

    def company_retrieve(self, request, *args, **kwargs):
        application = self.get_object()
        serializer = ApplicationSerializer(application)
        data = serializer.data
        candidate_name = application.candidate.user.get_full_name()
        candidate_avatar = application.candidate.user.avatar.url if application.candidate.user.avatar else None
        data['candidate'] = {
            'name': candidate_name,
            'avatar': candidate_avatar
        }
        job_post_name = application.job_post.name
        data['job_post'] = {'name': job_post_name}
        resume_url = application.resume.file.url if application.resume else None
        data['resume'] = resume_url
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        RETRIEVE_METHODS = {
            'CANDIDATE': self.candidate_retrieve,
            'COMPANY': self.company_retrieve
        }
        retrieve_method = RETRIEVE_METHODS.get(request.user.role)
        if not retrieve_method:
            raise PermissionDenied()
        return retrieve_method(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        application = self.get_object()

        new_status = request.data.get('status', None)
        if not new_status:
            raise ValidationError({'Status field is required'})

        if new_status not in Application.JobStatus.values:
            raise ValidationError('Invalid status value')

        old_status = application.status

        with transaction.atomic():
            job_post = application.job_post

            match new_status:
                case Application.JobStatus.REVIEWING:
                    raise ValidationError(
                        'Cannot change status back to reviewing')

                case Application.JobStatus.EMPLOYED:
                    if old_status != Application.JobStatus.REVIEWING:
                        raise ValidationError(
                            'Only reviewing applications can be employed')
                    if job_post.vacancy > 0:
                        job_post.vacancy -= 1
                        job_post.save()
                    else:
                        raise ValidationError('No vacancy available')
                    application.start_date = datetime.date.today()

                case Application.JobStatus.TERMINATED:
                    if old_status != Application.JobStatus.EMPLOYED:
                        raise ValidationError(
                            'Only employed applications can be terminated')
                    application.end_date = datetime.date.today()
                    job_post.vacancy += 1
                    job_post.save()

                case Application.JobStatus.REJECTED:
                    if old_status != Application.JobStatus.REVIEWING:
                        raise ValidationError(
                            'Only reviewing applications can be rejected')

            application.status = new_status
            application.save()

        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        application = self.get_object()
        if application.status != Application.JobStatus.REVIEWING:
            raise ValidationError('Only reviewing applications can be deleted')
        application.active = False
        application.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], url_path='get-reviews', detail=True, permission_classes=[perms.IsApplicationOwner | perms.IsApplicationBelongToCompanyUser])
    def get_reviews(self, request, *args, **kwargs):
        application = self.get_object()
        reviews = Review.objects.filter(
            Q(parent__isnull=True, reply__isnull=True) |
            Q(parent__isnull=False),
            application=application,
            active=True
        ).select_related('user', 'user__company_profile', 'parent',
                         'parent__user', 'parent__user__company_profile').order_by('-created_at')

        paginator = paginators.ItemPaginator()
        paginated_reviews = paginator.paginate_queryset(reviews, request)

        data = serializers.ReviewSerializer(paginated_reviews, many=True).data
        for i in range(len(data)):
            reviewer = paginated_reviews[i].user
            if reviewer.role == User.Role.COMPANY:
                reviewer_name = reviewer.company_profile.name
            else:
                reviewer_name = reviewer.get_full_name()
            reviewer_avatar = reviewer.avatar.url if reviewer.avatar else None
            data[i]['user'] = {
                'name': reviewer_name,
                'avatar': reviewer_avatar
            }
            if paginated_reviews[i].parent:
                reply = data[i]
                parent_data = ReviewSerializer(
                    paginated_reviews[i].parent).data
                data[i]= parent_data
                if paginated_reviews[i].parent.user.role == User.Role.COMPANY:
                    parent_reviewer_name = paginated_reviews[i].parent.user.company_profile.name
                else:
                    parent_reviewer_name = paginated_reviews[i].parent.user.get_full_name(
                    )
                parent_reviewer_avatar = paginated_reviews[i].parent.user.avatar.url if paginated_reviews[
                    i].parent.user.avatar else None
                data[i]['user'] = {
                    'name': parent_reviewer_name,
                    'avatar': parent_reviewer_avatar
                }
                data[i]['reply'] = reply
        return paginator.get_paginated_response(data)

    @transaction.atomic
    @action(methods=['post'], url_path='reviews', detail=True,
            permission_classes=[perms.IsApplicationOwner | perms.IsApplicationBelongToCompanyUser])
    def create_review(self, request, *args, **kwargs):
        application = self.get_object()
        if application.status != Application.JobStatus.TERMINATED:
            raise ValidationError(
                'Only terminated applications can post reviews')
        old_reviews = [review for review in application.reviews.all()]

        if len(old_reviews) == 2:
            raise ValidationError('An application can have at two reviews')

        data = request.data.copy()
        data['application'] = application.id
        data['user'] = request.user.id

        serializer = ReviewSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        if old_reviews:
            review.parent = old_reviews[0]
            review.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CompanyView(viewsets.GenericViewSet, generics.RetrieveAPIView):
    serializer_class = serializers.CompanyProfileSerializer
    queryset = CompanyProfile.objects.filter(active=True).select_related('user')

    def get_queryset(self):
        queryset = self.queryset
        if self.action.__eq__('retrieve'):
            queryset = queryset.prefetch_related('images')
        
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def list(self, request, *args, **kwargs):
        companies = self.get_queryset().annotate(
            job_post_count=Count('job_posts', filter=Q(job_posts__active=True))
        )
        paginator = paginators.ItemPaginator()
        paginated_companies = paginator.paginate_queryset(companies, request)

        data = serializers.CompanyProfileSerializer(
            paginated_companies, many=True).data
        for i in range(len(data)):
            company = paginated_companies[i]
            data[i]['avatar'] = company.user.avatar.url if company.user.avatar else None
            data[i]['job_post_count'] = company.job_post_count

        return paginator.get_paginated_response(data)

    def retrieve(self, request, *args, **kwargs):
        company = self.get_object()
        data = serializers.CompanyProfileSerializer(company).data
        image_urls = [image.image.url for image in company.images.all()]
        data['avatar'] = company.user.avatar.url if company.user.avatar else None
        data['images'] = image_urls

        if request.user.is_authenticated and request.user.role == User.Role.CANDIDATE:
            user = request.user
            is_followed = Follow.objects.filter(
                candidate__user=user, company=company).exists()
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

        paginator = paginators.ItemPaginator()
        paginated_reviews = paginator.paginate_queryset(reviews, request)

        data = serializers.ReviewSerializer(paginated_reviews, many=True).data
        for i in range(len(data)):
            job_name = paginated_reviews[i].application.job_post.name
            reviewer_name = paginated_reviews[i].user.get_full_name()
            reviewer_avatar = paginated_reviews[i].user.avatar.url if paginated_reviews[i].user.avatar else None
            start_date = paginated_reviews[i].application.start_date.strftime('%d/%m/%Y') if paginated_reviews[
                i].application.start_date else None
            end_date = paginated_reviews[i].application.end_date.strftime('%d/%m/%Y') if paginated_reviews[
                i].application.end_date else None
            data[i]['job_post'] = {
                'name': job_name
            }
            data[i]['user'] = {
                'name': reviewer_name,
                'avatar': reviewer_avatar
            }
            data[i]['application'] = {
                'start_date': start_date,
                'end_date': end_date
            }
        return paginator.get_paginated_response(data)


class CandidateView(viewsets.GenericViewSet, generics.RetrieveAPIView):
    serializer_class = serializers.CandidateProfileSerializer
    queryset = CandidateProfile.objects.select_related(
        'user').filter(active=True)

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
        ).select_related('user', 'user__company_profile', 'application', 'application__job_post')

        paginator = paginators.ItemPaginator()
        paginated_reviews = paginator.paginate_queryset(reviews, request)

        data = serializers.ReviewSerializer(paginated_reviews, many=True).data
        for i in range(len(data)):
            reviewer_name = paginated_reviews[i].user.company_profile.name
            reviewer_avatar = paginated_reviews[i].user.avatar.url if paginated_reviews[i].user.avatar else None
            data[i]['user'] = {
                'name': reviewer_name,
                'avatar': reviewer_avatar
            }
            job_name = paginated_reviews[i].application.job_post.name
            data[i]['job_post'] = {
                'name': job_name
            }
            start_date = paginated_reviews[i].application.start_date.strftime('%d/%m/%Y') if paginated_reviews[
                i].application.start_date else None
            end_date = paginated_reviews[i].application.end_date.strftime('%d/%m/%Y') if paginated_reviews[
                i].application.end_date else None
            data[i]['application'] = {
                'start_date': start_date,
                'end_date': end_date
            }
        return paginator.get_paginated_response(data)


class ReviewView(viewsets.GenericViewSet, generics.DestroyAPIView):
    serializer_class = serializers.ReviewSerializer
    queryset = Review.objects.filter(active=True)
    permission_classes = [IsReviewOwner]

    def partial_update(self, request, *args, **kwargs):
        review = self.get_object()
        s = self.get_serializer(review, data=request.data, partial=True)
        s.is_valid(raise_exception=True)
        s.save()

        return Response(s.data, status=status.HTTP_200_OK)
