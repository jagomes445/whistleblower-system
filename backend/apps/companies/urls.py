"""
URL patterns for the companies app.
"""
from django.urls import path
from .views import CompanyDetailView

app_name = 'companies'

urlpatterns = [
    path('me/', CompanyDetailView.as_view(), name='company-detail'),
]
