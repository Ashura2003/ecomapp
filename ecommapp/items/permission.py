from rest_framework.permissions import BasePermission

class IsAdminOrSeller(BasePermission):
    '''
    Custom permission class that only allows access to admin users or sellers.
    '''

    def has_permission(self, request, view):
        # Allow access if the user is authenticated and is an admin or seller
        user = request.user
        if user and user.is_authenticated:
            if user.user_type == 'seller' or user.is_staff:
                return True
        return False
    
