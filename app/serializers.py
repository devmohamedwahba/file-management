from rest_framework import serializers
from .models import FileManagementModel


class UploadSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FileManagementModel
        fields = ['name', 'file', 'created_at', 'updated_at']
