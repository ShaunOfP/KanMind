from rest_framework import generics, status
from rest_framework.exceptions import MethodNotAllowed, NotFound, APIException
from tasks_app.models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from .permissions import IsBoardMember, IsTaskCreatorOrBoardOwner, IsBoardMemberAllowedToPatch, IsBoardMemberOfTask, IsTaskCreator
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class TaskCreateView(generics.CreateAPIView):
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


class TaskUpdateAndDestroyView(generics.DestroyAPIView, generics.UpdateAPIView):
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
            permissions.append(IsBoardMemberAllowedToPatch())
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
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsTaskCreator]
    lookup_field = 'pk'
    lookup_url_kwarg = 'comment_pk'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {'detail': "Der Kommentar wurde erfolgreich gelöscht."},
                status=status.HTTP_204_NO_CONTENT
            )
        except APIException as exc:
            if exc.status_code == 404:
                return Response(
                    {'error': 'Kommentar oder Task nicht gefunden.'},
                    status=404
                )
            elif exc.status_code == 400:
                return Response({'error': 'Ungültige Anfragedaten.'}, status=400)
            elif exc.status_code == 401:
                return Response({'error': 'Nicht autorisiert. Der Benutzer muss eingeloggt sein.'}, status=401)
            elif exc.status_code == 500:
                return Response({'error': 'Interner Serverfehler.'}, status=500)
            elif exc.status_code == 403:
                return Response({'error': 'Verboten. Nur der Ersteller des Kommentars darf ihn löschen.'}, status=403)
            else:
                return Response({'error': f'Ein Fehler ist aufgetreten {exc}'})
