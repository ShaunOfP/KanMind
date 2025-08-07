from rest_framework import generics
from rest_framework.exceptions import MethodNotAllowed
from tasks_app.models import Comment, Task
from .serializers import TaskSerializer, CommentSerializer
from .permissions import IsBoardMember, IsTaskCreatorOrBoardOwner, IsBoardMemberAllowedToPatch, IsBoardMemberOfTask, IsTaskCreator
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsBoardMember, IsAuthenticated]

    def perform_create(self, serializer):
        """Assigns the currently authenticated user as the creator of a new Task. Calls board function to update counters"""
        task = serializer.save(creator=self.request.user)
        board = task.board
        board.update_counts()


class AssignedToMeView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Modifies the queryset so that only those Tasks are returned where the user is also the assignee"""
        user = self.request.user
        return Task.objects.filter(assignee=user)


class ReviewingView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Modifies the queryset so that only those Tasks are returned where the user is also the reviewer"""
        user = self.request.user
        return Task.objects.filter(reviewer=user)


class TaskUpdateAndDestroyView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        """Asks for different permission depending on the reequest method"""
        permissions = [IsAuthenticated()]
        if self.request.method == 'DELETE':
            permissions.append(IsTaskCreatorOrBoardOwner())
        elif self.request.method == 'PUT':
            raise MethodNotAllowed(
                method='PUT', detail='PUT is not allowed on this endpoint')
        else:
            permissions.append(IsBoardMemberAllowedToPatch())
        return permissions


class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsBoardMemberOfTask]

    def get_queryset(self):
        """Modifies the queryset so that only Comments with the selected Task-id are returned in descending order of creation"""
        task_id = self.kwargs['pk']
        return Comment.objects.filter(task__id=task_id).order_by('-created_at')

    def perform_create(self, serializer):
        """When creating a new Comment the currently authenticated user is assigned as the author of the comment. The task is also linked. Calls counter function to update counters"""
        task_id = self.kwargs['pk']
        task = get_object_or_404(Task, pk=task_id)
        serializer.save(author=self.request.user, task=task)
        task.update_count()


class CommentDestroyView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsTaskCreator]
    lookup_field = 'pk'
    lookup_url_kwarg = 'comment_pk'
