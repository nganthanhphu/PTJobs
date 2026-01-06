from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, CandidateProfile, CompanyProfile, Review, Application, CompanyImage, Resume, Follow, JobPost, \
    JobCategory
import cloudinary.uploader


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

    def create(self, validated_data):
        image_file = validated_data.pop('image', None)
        company_image = CompanyImage(**validated_data)

        if image_file:
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder='company_images/'
            )
            company_image.image = upload_result['secure_url']

        company_image.save()
        return company_image


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'

    def create(self, validated_data):
        file = validated_data.pop('file', None)
        resume = Resume(**validated_data)

        if file:
            upload_result = cloudinary.uploader.upload(
                file,
                resource_type='raw',
                folder='resumes/'
            )
            resume.file = upload_result['secure_url']

        resume.save()
        return resume


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

    def create(self, validated_data):
        follow = Follow(**validated_data)
        follow.save()
        return follow


class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = ['id', 'name', 'description', 'salary', 'address', 'deadline', 'vacancy', 'company', 'category',
                  'active', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        job_post = JobPost(**validated_data)
        job_post.save()
        return job_post

    def update(self, instance, validated_data):
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
        fields = '__all__'

    def create(self, validated_data):
        application = Application(**validated_data)
        application.save()
        return application


class CandidateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CandidateProfile
        fields = ['id', 'gender', 'dob', 'user']


class CompanyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    images = CompanyImageSerializer(many=True, read_only=True)

    class Meta:
        model = CompanyProfile
        fields = ['id', 'name', 'tax_number', 'address', 'user', 'images']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'comment', 'user', 'application', 'created_at']
        extra_kwargs = {
            'application': {
                'write_only': True
            }
        }

    def update(self, instance, validated_data):
        keys = set(validated_data.keys())
        if keys - {'comment'}:
            raise ValidationError('Invalid fields for update')
        return super().update(instance, validated_data)


class TreeReviewSerializer(ReviewSerializer):
    user = UserSerializer(read_only=True)
    parent = ReviewSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'comment', 'user', 'application', 'created_at', 'parent']
        extra_kwargs = {
            'application': {
                'write_only': True
            }
        }
