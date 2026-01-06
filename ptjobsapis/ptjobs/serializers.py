from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, CandidateProfile, CompanyProfile, Review, Application, CompanyImage


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


class CandidateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CandidateProfile
        fields = ['id', 'gender', 'dob', 'user']


class CompanyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyImage
        fields = ['image', 'company']
        extra_kwargs = {
            'company': {
                'write_only': True
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image:
            data['image'] = instance.image.url
        return data


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