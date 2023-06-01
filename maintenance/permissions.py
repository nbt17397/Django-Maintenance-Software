# from django.shortcuts import get_object_or_404
# from django.utils.translation import gettext_lazy as _
# from rest_framework.permissions import BasePermission, SAFE_METHODS

# from .models import Project


# class IsStaffOrAdmin(BasePermission):

#     def has_permission(self, request, view):
#         return request.user.is_authenticated is True
    
#     def has_object_permission(self, request, view, obj):
        
#         if request.method in SAFE_METHODS:
#             return True

#         return obj.staff == request.user or request.user.is_admin