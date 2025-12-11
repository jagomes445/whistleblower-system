"""
URL patterns for the magic_links app.
"""
from django.urls import path
from .views import MagicLinkListCreateView, MagicLinkDetailView

app_name = 'magic_links'

urlpatterns = [
    path('', MagicLinkListCreateView.as_view(), name='magic-link-list'),
    path('<uuid:pk>/', MagicLinkDetailView.as_view(), name='magic-link-detail'),
]
