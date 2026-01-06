from rest_framework import serializers
from ptjobs.models import User, Resume, Follow
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
    
class FollowSerializer(serializers.Serializer):
    class Meta:
        model = Follow
        fields = '__all__'
        
    def create(self, validated_data):
        follow = Follow(**validated_data)
        follow.save()
        return follow
    
    def delete(self, instance):
        instance.delete()
        return instance