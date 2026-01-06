import json

from django.db import transaction
from rest_framework import viewsets, generics, parsers, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from . import models
from . import serializers
from .utils import RoleMapper


class UserView(viewsets.ViewSet, generics.CreateAPIView):
    queryset = models.User.objects.select_related('candidate_profile', 'company_profile').all()
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        profile_data = data.pop('profile', None)
        if isinstance(profile_data, list):
            profile_data = profile_data[0]
        profile_data = json.loads(profile_data) if profile_data and isinstance(profile_data, str) else None

        s = serializers.UserSerializer(data=data)
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
                    ValidationError("This user type cannot have a profile")
        res_data = serializers.UserSerializer(user).data

        profile = None
        if user.profile:
            serializer_class = RoleMapper.get_serializer(user.role)
            if serializer_class:
                profile = serializer_class(user.profile).data
            else:
                NotFound("This user type does not have a profile")
        res_data['profile'] = profile

        return Response(res_data, status=status.HTTP_200_OK)
