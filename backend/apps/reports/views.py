"""
Views for the reports app.
"""
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.conf import settings
from core.permissions import IsCompanyMember
from .models import Report
from apps.magic_links.models import MagicLink
from .serializers import (
    ReportSerializer, UpdateReportSerializer,
    PublicReportSerializer, MagicLinkValidationSerializer
)


class ReportListView(generics.ListAPIView):
    """
    API view for listing reports for the authenticated user's company.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'category', 'is_anonymous']
    ordering_fields = ['created_at', 'updated_at', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Only return reports for the user's company
        return Report.objects.filter(
            magic_link__company=self.request.user.company
        ).select_related('magic_link', 'magic_link__company')


class ReportDetailView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating a report.
    """
    permission_classes = [permissions.IsAuthenticated, IsCompanyMember]
    
    def get_queryset(self):
        return Report.objects.filter(
            magic_link__company=self.request.user.company
        ).select_related('magic_link', 'magic_link__company')
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateReportSerializer
        return ReportSerializer


class ValidateMagicLinkView(APIView):
    """
    Public API view for validating a magic link token.
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, token):
        try:
            magic_link = MagicLink.objects.select_related('company').get(token=token)
            
            if magic_link.is_valid():
                return Response({
                    'is_valid': True,
                    'company_name': magic_link.company.name,
                    'message': 'Magic link is valid'
                })
            else:
                return Response({
                    'is_valid': False,
                    'company_name': magic_link.company.name,
                    'message': 'This link has expired or is no longer active'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        except MagicLink.DoesNotExist:
            return Response({
                'is_valid': False,
                'company_name': '',
                'message': 'Invalid magic link'
            }, status=status.HTTP_404_NOT_FOUND)


class PublicReportSubmitView(APIView):
    """
    Public API view for submitting a report via magic link.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, token):
        try:
            magic_link = MagicLink.objects.select_related('company').get(token=token)
            
            if not magic_link.is_valid():
                return Response({
                    'error': 'This link has expired or is no longer active'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = PublicReportSerializer(data=request.data)
            if serializer.is_valid():
                # Create report with magic_link
                report = serializer.save(magic_link=magic_link)
                
                # Send email notification to company managers
                self._send_notification_email(magic_link.company, report)
                
                return Response({
                    'message': 'Report submitted successfully',
                    'report_id': report.id
                }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except MagicLink.DoesNotExist:
            return Response({
                'error': 'Invalid magic link'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def _send_notification_email(self, company, report):
        """
        Send email notification to company managers about new report.
        """
        try:
            # Get all managers for the company
            managers = company.users.filter(is_active=True)
            recipient_list = [user.email for user in managers]
            
            if recipient_list:
                subject = f'New Whistleblower Report - {report.get_category_display()}'
                message = f"""
A new whistleblower report has been submitted to {company.name}.

Category: {report.get_category_display()}
Status: {report.get_status_display()}
Submitted: {report.created_at.strftime('%Y-%m-%d %H:%M')}

Please log in to the dashboard to review this report.
                """
                
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipient_list,
                    fail_silently=True,
                )
        except Exception as e:
            # Log the error but don't fail the request
            print(f"Failed to send email notification: {e}")
