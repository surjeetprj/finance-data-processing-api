from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Allows full access only to Admin users."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ADMIN')

class IsAnalyst(permissions.BasePermission):
    """Analysts have Read-Only access (GET, HEAD, OPTIONS)."""
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'ANALYST' and 
            request.method in permissions.SAFE_METHODS
        )

class IsEditor(permissions.BasePermission):
    """Editors can view all, create new, but only modify/delete their own records."""
    def has_permission(self, request, view):
        # Allow entry to the view if they are an Editor
        return bool(request.user and request.user.is_authenticated and request.user.role == 'EDITOR')

    def has_object_permission(self, request, view, obj):
        # All editors can read any record
        if request.method in permissions.SAFE_METHODS:
            return True
        # For UPDATE or DELETE, the editor must be the owner of the record
        return obj.user == request.user