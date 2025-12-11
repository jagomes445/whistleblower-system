"""
Serializers for the reports app.
"""
from rest_framework import serializers
from .models import Report
from apps.magic_links.models import MagicLink


class ReportSerializer(serializers.ModelSerializer):
    """
    Serializer for Report model (manager view).
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    magic_link_name = serializers.CharField(source='magic_link.name', read_only=True)
    reporter_name = serializers.SerializerMethodField()
    reporter_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Report
        fields = (
            'id', 'magic_link', 'magic_link_name', 'category', 'category_display',
            'description', 'is_anonymous', 'reporter_name', 'reporter_email',
            'status', 'status_display', 'internal_notes', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'magic_link', 'category', 'description', 'is_anonymous',
            'reporter_name', 'reporter_email', 'created_at', 'updated_at'
        )
    
    def get_reporter_name(self, obj):
        if obj.is_anonymous:
            return None
        return obj.reporter_name
    
    def get_reporter_email(self, obj):
        if obj.is_anonymous:
            return None
        return obj.reporter_email


class UpdateReportSerializer(serializers.ModelSerializer):
    """
    Serializer for updating report status and notes.
    """
    class Meta:
        model = Report
        fields = ('status', 'internal_notes')


class PublicReportSerializer(serializers.ModelSerializer):
    """
    Serializer for public report submission.
    """
    reporter_name = serializers.CharField(required=False, allow_blank=True)
    reporter_email = serializers.EmailField(required=False, allow_blank=True)
    
    class Meta:
        model = Report
        fields = (
            'category', 'description', 'is_anonymous',
            'reporter_name', 'reporter_email'
        )
    
    def validate(self, attrs):
        # If not anonymous, require name and email
        if not attrs.get('is_anonymous', True):
            if not attrs.get('reporter_name'):
                raise serializers.ValidationError({
                    'reporter_name': 'Name is required when not submitting anonymously.'
                })
            if not attrs.get('reporter_email'):
                raise serializers.ValidationError({
                    'reporter_email': 'Email is required when not submitting anonymously.'
                })
        
        return attrs
    
    def create(self, validated_data):
        # Extract reporter info
        reporter_name = validated_data.pop('reporter_name', None)
        reporter_email = validated_data.pop('reporter_email', None)
        
        # Create report
        report = Report.objects.create(**validated_data)
        
        # Set encrypted fields if provided
        if reporter_name and not validated_data.get('is_anonymous', True):
            report.reporter_name = reporter_name
        if reporter_email and not validated_data.get('is_anonymous', True):
            report.reporter_email = reporter_email
        
        report.save()
        return report


class MagicLinkValidationSerializer(serializers.Serializer):
    """
    Serializer for magic link validation response.
    """
    is_valid = serializers.BooleanField()
    company_name = serializers.CharField()
    message = serializers.CharField()
