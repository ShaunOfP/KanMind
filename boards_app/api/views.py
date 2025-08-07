from rest_framework import generics
from boards_app.models import Board
from .serializers import BoardSerializer, BoardsDetailSerializer, BoardsUpdateSerializer
from .permissions import IsBoardMemberOrOwner, IsBoardOwner
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.exceptions import MethodNotAllowed


class BoardListView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [IsBoardMemberOrOwner() and IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsBoardOwner()]
        elif self.request.method == 'PUT':
            raise MethodNotAllowed(
                method='PUT', detail='PUT is not allowed on this endpoint')
        return [IsBoardMemberOrOwner()]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return BoardsUpdateSerializer
        else:
            return BoardsDetailSerializer
