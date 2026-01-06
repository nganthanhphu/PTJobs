from rest_framework.permissions import IsAuthenticated

from .models import User


class IsCompanyUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == User.Role.COMPANY


class IsCandidateUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == User.Role.CANDIDATE


class IsCompanyImageOwner(IsAuthenticated):
    def has_object_permission(self, request, view, company_image):
        return super().has_permission(request, view) and company_image.company.user == request.user


class IsReviewOwner(IsAuthenticated):
    def has_object_permission(self, request, view, review):
        return super().has_permission(request, view) and review.user == request.user