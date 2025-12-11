"""
Serializers for the companies app.
"""
from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for Company model.
    """
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    users_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = ('id', 'name', 'created_by', 'created_by_name', 'users_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')
    
    def get_users_count(self, obj):
        return obj.users.count()


class UpdateCompanySerializer(serializers.ModelSerializer):
    """
    Serializer for updating company information.
    """
    class Meta:
        model = Company
        fields = ('name',)
