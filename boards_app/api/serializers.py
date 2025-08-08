from rest_framework import serializers
from django.contrib.auth.models import User

from tasks_app.api.serializers import TaskSerializer
from shared.serializers import UserSerializer
from boards_app.models import BoardDetail, Board
from tasks_app.models import Task


class BoardSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True
    )

    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'members', 'ticket_count',
                  'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']
        read_only_fields = ['member_count', 'owner_id']

    def create(self, validated_data):
        """Assigns the members to the board and updates the counter"""
        members = validated_data.pop('members', [])
        board = Board.objects.create(**validated_data)
        board.members.set(members)
        board.member_count = board.members.count()
        board.save()
        return board

    def to_representation(self, instance):
        """Sets the default 0 for empty key-value pairs"""
        data = super().to_representation(instance)
        for key, value in data.items():
            if value is None:
                data[key] = 0
        return data


class BoardsDetailSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='members'
    )
    tasks = TaskSerializer(many=True, read_only=True)
    task_ids = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        many=True,
        source='tasks',
        write_only=True
    )

    class Meta:
        model = BoardDetail
        fields = ['id', 'title', 'owner_id',
                  'members', 'member_ids', 'tasks', 'task_ids']


class BoardsUpdateSerializer(serializers.ModelSerializer):
    owner_data = UserSerializer(source='owner', read_only=True)
    members_data = UserSerializer(many=True, read_only=True, source='members')
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True
    )

    class Meta:
        model = BoardDetail
        fields = ['id', 'title', 'owner_data', 'members_data', 'members']
        read_only_fields = ['id', 'owner_data', 'members_data']

    def update(self, instance, validated_data):
        """Assigns the members to the board when patching and updates the member count"""
        members = validated_data.pop('members', None)
        instance = super().update(instance, validated_data)
        if members is not None:
            instance.members.set(members)
        instance.member_count = instance.members.count()
        instance.save()
        return instance
