from rest_framework import serializers
from ptjobs.models import JobPost, User, Resume, Follow
import cloudinary.uploader

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'phone', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'phone': {
                'required': True
            }
        }

    def create(self, validated_data):
        u = User(**validated_data)
        u.set_password(u.password)
        u.save()

        return u

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['avatar'] = instance.avatar.url if instance.avatar else ''

        return data

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
        fields = ['id', 'name', 'description', 'salary', 'address', 'deadline', 'vacancy', 'company', 'category', 'active', 'created_at']
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