"""
URL patterns for the reports app.
"""
from django.urls import path
from .views import (
    ReportListView, ReportDetailView,
    ValidateMagicLinkView, PublicReportSubmitView
)

app_name = 'reports'

urlpatterns = [
    # Manager endpoints (authenticated)
    path('', ReportListView.as_view(), name='report-list'),
    path('<uuid:pk>/', ReportDetailView.as_view(), name='report-detail'),
    
    # Public endpoints (no authentication)
    path('public/<uuid:token>/', ValidateMagicLinkView.as_view(), name='validate-magic-link'),
    path('public/<uuid:token>/submit/', PublicReportSubmitView.as_view(), name='submit-report'),
]
