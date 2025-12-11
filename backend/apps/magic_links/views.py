"""
Views for the magic_links app.
"""
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from core.permissions import IsCompanyMember
from .models import MagicLink
from .serializers import MagicLinkSerializer, CreateMagicLinkSerializer


class MagicLinkListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating magic links.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return MagicLink.objects.filter(company=self.request.user.company)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateMagicLinkSerializer
        return MagicLinkSerializer


class MagicLinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a magic link.
    """
    permission_classes = [permissions.IsAuthenticated, IsCompanyMember]
    
    def get_queryset(self):
        return MagicLink.objects.filter(company=self.request.user.company)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CreateMagicLinkSerializer
        return MagicLinkSerializer
