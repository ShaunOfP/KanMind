from django.db import models
from boards_app.models import Board
from django.contrib.auth.models import User


class Comment(models.Model):
    task = models.ForeignKey(
        'Task', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class Task(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    assignee = models.ForeignKey(
        User, related_name='assigned_tasks', on_delete=models.CASCADE, blank=True, null=True)
    reviewer = models.ForeignKey(
        User, related_name='reviewing_tasks', on_delete=models.CASCADE, blank=True, null=True)
    due_date = models.DateField()
    creator = models.ForeignKey(
        User, related_name='task_creator', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
