from rest_framework.permissions import BasePermission


class IsBoardMemberOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.owner or
            request.user in obj.members.all()
        )


class IsBoardOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
