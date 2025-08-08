from rest_framework.permissions import BasePermission


class IsBoardMemberOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Checks if the user is either the owner or a member of the board"""
        return (
            request.user == obj.owner or
            request.user in obj.members.all()
        )


class IsBoardOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Checks if the user is the owner of the board"""
        return request.user == obj.owner
