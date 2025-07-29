from rest_framework import serializers
from tasks_app.models import Task, Comment
from boards_app.api.serializers import UserSerializer
from django.contrib.auth.models import User


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        read_only = ['id', 'created_at', 'author']


class TaskSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

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
        rep = super().to_representation(instance)
        if rep['assignee'] is None:
            rep['assignee'] = {}
        if rep['reviewer'] is None:
            rep['reviewer'] = {}
        return rep

    def get_comments_count(self, obj):
        return obj.comments.count()

    def validate(self, data):
        board = data.get('board')
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
        errors = []
        if value not in ['to-do', 'in-progress', 'review', 'done']:
            errors.append(
                'Als Status werden nur to-do, in-progress, review oder done akzeptiert')
        if errors:
            raise serializers.ValidationError(errors)
        return value

    def validate_priority(self, value):
        errors = []
        if value not in ['low', 'medium', 'high']:
            errors.append(
                'Als Priorität werden nur low, medium oder high akzeptiert')
        if errors:
            raise serializers.ValidationError(errors)
        return value
