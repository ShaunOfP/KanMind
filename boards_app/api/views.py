from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.exceptions import MethodNotAllowed

from boards_app.models import Board
from .serializers import BoardSerializer, BoardsDetailSerializer, BoardsUpdateSerializer
from .permissions import IsBoardMemberOrOwner, IsBoardOwner


class BoardListView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        """returns the boards where the user is either the owner or a member"""
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def get_permissions(self):
        """Checks if the user is authenticated when tryint to POST a new Board. When using the GET-Method it checks if the user is a Member or the owner of the board and if hes authenticated"""
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [IsBoardMemberOrOwner() and IsAuthenticated()]

    def perform_create(self, serializer):
        """When creating a new board the authenticated user is set as the owner"""
        serializer.save(owner=self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()

    def get_permissions(self):
        """Checks for different permissions when using different request methods."""
        if self.request.method == 'DELETE':
            return [IsBoardOwner()]
        elif self.request.method == 'PUT':
            raise MethodNotAllowed(
                method='PUT', detail='PUT is not allowed on this endpoint')
        return [IsBoardMemberOrOwner()]

    def get_serializer_class(self):
        """Checks which serializer to use."""
        if self.request.method == 'PATCH':
            return BoardsUpdateSerializer
        else:
            return BoardsDetailSerializer
