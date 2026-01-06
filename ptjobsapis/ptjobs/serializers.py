from rest_framework import serializers
from ptjobs.models import Resume
import cloudinary.uploader


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