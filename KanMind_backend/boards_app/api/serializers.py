from rest_framework import serializers
from boards_app.models import Board, BoardDetail
from django.contrib.auth.models import User


class BoardSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True
    )

    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'members', 'ticket_count',
                  'tasks_to_do_count', 'tasks_high_prio_count', 'owner']
        read_only_fields = ['member_count', 'owner']

    def create(self, validated_data):
        members = validated_data.pop('members', [])
        board = Board.objects.create(**validated_data)
        board.members.set(members)
        board.member_count = board.members.count()
        board.save()
        return board

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in data.items():
            if value is None:
                data[key] = 0
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']


class BoardsDetailSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='members'
    )

    class Meta:
        model = BoardDetail
        fields = ['id', 'title', 'owner_id', 'members', 'member_ids']  # , 'tasks'


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            'invalid': 'Ungültige Anfrage. Die E-Mail-Adresse fehlt oder hat ein falsches Format.'
        }
    )
