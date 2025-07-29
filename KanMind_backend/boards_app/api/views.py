from rest_framework import generics, status
from boards_app.models import Board
from .serializers import BoardSerializer, EmailSerializer, BoardsDetailSerializer
from .permissions import IsBoardMemberOrOwner, IsBoardOwner
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q


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
    serializer_class = BoardsDetailSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsBoardOwner()]
        return [IsBoardMemberOrOwner()]
    #Tasks hinzufügen im Model


class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EmailSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                return Response({
                    'id': user.pk,
                    'email': user.email,
                    'fullname': user.username
                })
            except User.DoesNotExist:
                return Response({
                    'error': 'Email nicht gefunden'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
