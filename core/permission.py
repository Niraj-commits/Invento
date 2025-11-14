from rest_framework.permissions import BasePermission,SAFE_METHODS

class ViewUserPermission(BasePermission):
     
     def has_permission(self, request, view):
          if  request.user and request.user.is_authenticated and request.method in SAFE_METHODS:
               return True
          else:
               return False