from django.forms import ValidationError
from django.views.generic.dates import timezone_today
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, CandidateProfile, CompanyProfile, Review, Application, CompanyImage, Resume, Follow, JobPost, \
    JobCategory, WorkTime


class UserSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'phone', 'role', 'avatar', 'old_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

    def update(self, instance, validated_data):
        old_password = validated_data.pop('old_password', None)
        keys = set(validated_data.keys())
        if keys - {'first_name', 'last_name', 'email', 'phone', 'avatar', 'password'}:
            raise ValidationError('Invalid fields for update')
        if 'password' in validated_data:
            if not old_password or not instance.check_password(old_password):
                raise ValidationError('Incorrect old password')
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.avatar:
            data['avatar'] = instance.avatar.url
        return data


class CompanyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyImage
        fields = ['id', 'image', 'company', 'created_at']
        read_only_fields = ['id', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image:
            data['image'] = instance.image.url
        return data


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id','file', 'candidate']
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.file:
            data['file'] = instance.file.url
        return data


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'created_at', 'candidate', 'company']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'created_at': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        follow = Follow(**validated_data)
        follow.save()
        return follow


class WorkTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTime
        fields = ['day', 'start_time', 'end_time', 'job_post']


class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = ['id', 'name', 'description', 'salary', 'address', 'deadline', 'vacancy', 'company', 'category',
                  'created_at', 'active']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'active': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        job_post = JobPost(**validated_data)
        job_post.save()
        return job_post

    def update(self, instance, validated_data):
        if 'created_at' in validated_data or 'company' in validated_data:
            raise ValidationError('Invalid field for update')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['id', 'name']

    def create(self, validated_data):
        category = JobCategory(**validated_data)
        category.save()
        return category

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'start_date', 'end_date', 'status', 'resume', 'candidate', 'job_post']
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        application = Application(**validated_data)
        application.save()
        return application

    def validate(self, attrs):
        job_post = attrs.get('job_post')
        if job_post.deadline < timezone_today() and job_post.vacancy <= 0:
            raise ValidationError('Invalid job post for application')
        return attrs


class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = ['id', 'gender', 'dob', 'user']
        extra_kwargs = {
            'user': {
                'write_only': True
            }
        }


class CompanyProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = ['id', 'name', 'tax_number', 'address', 'user']
        extra_kwargs = {
            'user': {
                'write_only': True
            }
        }


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'comment', 'user', 'application', 'created_at']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'created_at': {
                'read_only': True
            },
            'application': {
                'write_only': True
            }
        }

    def update(self, instance, validated_data):
        keys = set(validated_data.keys())
        if keys - {'comment'}:
            raise ValidationError('Invalid fields for update')
        return super().update(instance, validated_data)

