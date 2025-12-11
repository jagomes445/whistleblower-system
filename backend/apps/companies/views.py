"""
Views for the companies app.
"""
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Company
from .serializers import CompanySerializer, UpdateCompanySerializer


class CompanyDetailView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating user's company.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.company
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CompanySerializer
        return UpdateCompanySerializer
    
    def retrieve(self, request, *args, **kwargs):
        if not request.user.company:
            return Response(
                {'error': 'User is not associated with any company'},
                status=status.HTTP_404_NOT_FOUND
            )
        return super().retrieve(request, *args, **kwargs)
