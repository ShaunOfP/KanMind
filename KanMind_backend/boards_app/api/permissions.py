from rest_framework.permissions import BasePermission
from boards_app.models import Board


class IsBoardMemberOrOwner(BasePermission):
    message = 'Verboten. Der Benutzer muss entweder Mitglied des Boards oder der Eigentümer des Boards sein.'

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.owner or
            request.user in obj.members.all()
        )


class IsBoardOwner(BasePermission):
    message = 'Verboten. Der Benutzer muss der Eigentümer des Boards sein, um es zu löschen.'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
