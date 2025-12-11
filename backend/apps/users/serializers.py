"""
Serializers for the users app.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from apps.companies.models import Company


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'company', 'company_name', 'role', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at', 'company', 'role')


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    company_name = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'first_name', 'last_name', 'company_name')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        # Remove password_confirm and company_name from validated_data
        validated_data.pop('password_confirm')
        company_name = validated_data.pop('company_name')
        
        # Create company first
        company = Company.objects.create(name=company_name)
        
        # Create user with company
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            company=company,
            role='admin'
        )
        
        # Set the created_by field on the company
        company.created_by = user
        company.save()
        
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        read_only_fields = ('email',)
