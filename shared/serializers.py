from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='username')
    
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']