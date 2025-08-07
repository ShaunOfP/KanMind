from rest_framework.permissions import BasePermission
from boards_app.models import Board
from tasks_app.models import Task
from rest_framework.response import Response
from rest_framework import status


class IsBoardMember(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['DELETE', 'PATCH', 'POST']:
            board_id = request.data.get('board')
            if not board_id:
                return False
            try:
                board = Board.objects.get(id=board_id)
            except Board.DoesNotExist:
                return Response({'error': 'Board does not exist'}, status=status.HTTP_404_NOT_FOUND)
            return request.user in board.members.all()
        return True


class IsBoardMemberAllowedToPatch(BasePermission):
    def has_object_permission(self, request, view, obj):
        board = obj.board
        return request.user in board.members.all()


class IsTaskCreatorOrBoardOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.board.owner or
            request.user == obj.creator
        )


class IsBoardMemberOfTask(BasePermission):
    def has_permission(self, request, view):
        task_id = view.kwargs.get('pk')
        task = Task.objects.select_related('board').get(pk=task_id)
        return request.user in task.board.members.all()


class IsTaskCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
