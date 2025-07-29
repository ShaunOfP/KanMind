from rest_framework.permissions import BasePermission
from boards_app.models import Board


class IsBoardMember(BasePermission):
    message = 'Verboten. Der Benutzer muss Mitglied des Boards sein, um eine Task zu erstellen.'

    def has_permission(self, request, view):
        if request.method in ['DELETE', 'PATCH', 'POST']:
            board_id = request.data.get('board')
            if not board_id:
                return False
            try:
                board = Board.objects.get(id=board_id)
            except Board.DoesNotExist:
                return False
            return request.user in board.members.all()
        return True


class IsTaskCreatorOrBoardOwner(BasePermission):
    message = 'Verboten. Nur der Ersteller der Task oder der Board-Eigentümer kann die Task löschen.'

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.board.owner or
            request.user == obj.creator
        )


class IsBoardMemberOfTask(BasePermission):
    message = 'Verboten. Der Benutzer muss Mitglied des Boards sein, zu dem die Task gehört.'

    def has_object_permission(self, request, view, obj):
        # return request.user in obj.board.members
        pass    
