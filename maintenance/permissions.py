from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Project


class  IsUserManager(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_manager is True
    

class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser is True



