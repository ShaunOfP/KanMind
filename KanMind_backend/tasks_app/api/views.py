from rest_framework import generics
from rest_framework.exceptions import MethodNotAllowed
from tasks_app.models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from .permissions import IsBoardMember, IsTaskCreatorOrBoardOwner, IsBoardMemberOfTask
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class TaskListView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsBoardMember, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class AssignedToMeView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user)


class ReviewingView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(reviewer=user)


class TaskDetailView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        if self.request.method == 'DELETE':
            permissions.append(IsTaskCreatorOrBoardOwner())
        elif self.request.method == 'PUT':
            raise MethodNotAllowed(
                method='PUT', detail='PUT is not allowed on this endpoint')
        else:
            permissions.append(IsBoardMember())
        return permissions


class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsBoardMemberOfTask]

    def get_queryset(self):
        task_id = self.kwargs['pk']
        return Comment.objects.filter(task__id=task_id).order_by('-created_at')

    def perform_create(self, serializer):
        task_id = self.kwargs['pk']
        task = get_object_or_404(Task, pk=task_id)
        serializer.save(author=self.request.user, task=task)


class CommentDestroyView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = []

    def get_queryset(self):
        comment_id = self.kwargs['pk']
        return Comment.objects.filter(comment__id=comment_id)
