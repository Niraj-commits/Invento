from rest_framework.permissions import BasePermission,SAFE_METHODS


class ViewPermission(BasePermission):
    
    def has_permission(self, request, view):

        if request.user and request.user.is_authenticated:
            return True
        
        return False

class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user