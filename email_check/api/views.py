from rest_framework import status, generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class EmailCheckView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """retrieves the email from the kwags and returns the object of the user if it exists"""
        email = kwargs['email']
        if not email:
            return Response({'error': 'Email query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            return Response({
                'id': user.pk,
                'email': user.email,
                'fullname': user.username
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
