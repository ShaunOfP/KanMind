from rest_framework import serializers
from django.contrib.auth.models import User

from tasks_app.models import Task
from tasks_app.models import Comment
from shared.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        read_only = ['id', 'created_at', 'author']


class TaskSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assignee',
        write_only=True,
        required=False,
        allow_null=True
    )

    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='reviewer',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status',
                  'priority', 'assignee', 'assignee_id', 'reviewer', 'reviewer_id', 'due_date', 'comments_count']
        read_only = ['id', 'comments_count', 'reviewer', 'assignee']
        extra_kwargs = {
            'assignee': {'required': False, 'allow_null': True},
            'reviewer': {'required': False, 'allow_null': True},
        }

    def to_representation(self, instance):
        """Makes sure that assignee and reviewer are displayed as empty dictionaries when empty"""
        rep = super().to_representation(instance)
        if rep['assignee'] is None:
            rep['assignee'] = {}
        if rep['reviewer'] is None:
            rep['reviewer'] = {}
        return rep

    def validate(self, data):
        """Validates if assignee and reviewer are members of the board. If not returns error"""
        board = data.get('board') or getattr(self.instance, 'board', None)
        assignee = data.get('assignee')
        reviewer = data.get('reviewer')

        if assignee and assignee not in board.members.all():
            raise serializers.ValidationError(
                {'assignee': 'Assignee must be a member of the board.'})

        if reviewer and reviewer not in board.members.all():
            raise serializers.ValidationError(
                {'reviewer': 'Reviewer must be a member of the board.'})
        return data

    def validate_status(self, value):
        """Validates the input for the status. If a wrong value is provided it returns an error"""
        errors = []
        if value not in ['to-do', 'in-progress', 'review', 'done']:
            errors.append(
                'Als Status werden nur to-do, in-progress, review oder done akzeptiert')
        if errors:
            raise serializers.ValidationError(errors)
        return value

    def validate_priority(self, value):
        """Validates the input for the priority. If a wrong value is provided it returns an error"""
        errors = []
        if value not in ['low', 'medium', 'high']:
            errors.append(
                'Als Priorität werden nur low, medium oder high akzeptiert')
        if errors:
            raise serializers.ValidationError(errors)
        return value

    def update(self, instance, validated_data):
        """Sets the new values for the given attributes of the board instance. Calls board function to update the counters like member_count"""
        board = instance.board
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        board.update_counts()
        return instance

    def perform_destroy(self, instance):
        """Overrides the destroy function to also call the board function to update the counts of the board"""
        board = instance.board
        instance.delete()
        board.update_counts()
