"""
Custom permissions for the whistleblower system.
"""
from rest_framework import permissions


class IsManager(permissions.BasePermission):
    """
    Permission to check if user is a manager or admin.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsCompanyMember(permissions.BasePermission):
    """
    Permission to check if user belongs to the company associated with the object.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if object has a company attribute
        if hasattr(obj, 'company'):
            return obj.company == request.user.company
        
        # For reports, check through magic_link
        if hasattr(obj, 'magic_link'):
            return obj.magic_link.company == request.user.company
        
        return False
