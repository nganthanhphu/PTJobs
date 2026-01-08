from rest_framework.permissions import IsAuthenticated

from .models import User


class IsCompanyUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == User.Role.COMPANY


class IsCandidateUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == User.Role.CANDIDATE


class IsReviewOwner(IsAuthenticated):
    def has_object_permission(self, request, view, review):
        return super().has_permission(request, view) and review.user == request.user


class IsResumeOwner(IsAuthenticated):
    def has_object_permission(self, request, view, resume):
        return super().has_permission(request, view) and resume.candidate.user == request.user


class IsCompanyImageOwner(IsAuthenticated):
    def has_object_permission(self, request, view, company_image):
        return super().has_permission(request, view) and company_image.company.user == request.user


class IsFollowingOwner(IsAuthenticated):
    def has_object_permission(self, request, view, following):
        return super().has_permission(request, view) and following.candidate.user == request.user


class IsJobPostOwner(IsAuthenticated):
    def has_object_permission(self, request, view, job_post):
        return request.user.role == User.Role.COMPANY and job_post.company.user == request.user


class IsApplicationBelongToCompanyUser(IsAuthenticated):
    def has_object_permission(self, request, view, application):
        return super().has_permission(request, view) and application.job_post.company.user == request.user