"""
Serializers for the magic_links app.
"""
from rest_framework import serializers
from .models import MagicLink


class MagicLinkSerializer(serializers.ModelSerializer):
    """
    Serializer for MagicLink model.
    """
    company_name = serializers.CharField(source='company.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    is_valid = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = MagicLink
        fields = (
            'id', 'token', 'company', 'company_name', 'created_by', 'created_by_name',
            'name', 'is_active', 'expires_at', 'created_at', 'is_valid', 'url'
        )
        read_only_fields = ('id', 'token', 'company', 'created_by', 'created_at')
    
    def get_is_valid(self, obj):
        return obj.is_valid()
    
    def get_url(self, obj):
        request = self.context.get('request')
        if request:
            frontend_url = request.build_absolute_uri('/').rstrip('/')
            # In production, this would use FRONTEND_URL from settings
            from django.conf import settings
            frontend_url = settings.FRONTEND_URL
            return f"{frontend_url}/report/{obj.token}"
        return f"/report/{obj.token}"


class CreateMagicLinkSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a magic link.
    """
    class Meta:
        model = MagicLink
        fields = ('name', 'is_active', 'expires_at')
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['company'] = request.user.company
        validated_data['created_by'] = request.user
        return super().create(validated_data)
