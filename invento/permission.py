from rest_framework.permissions import BasePermission,SAFE_METHODS


class ViewPermission(BasePermission):
    
    def has_permission(self, request, view):

        if request.user and request.user.is_authenticated:
            return True
        
        return False