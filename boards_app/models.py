from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    title = models.CharField(max_length=30)
    member_count = models.PositiveIntegerField(default=0)
    members = models.ManyToManyField(
        User, related_name='boards', blank=True)
    ticket_count = models.IntegerField(blank=True, null=True, default=0)
    tasks_to_do_count = models.IntegerField(blank=True, null=True, default=0)
    tasks_high_prio_count = models.IntegerField(
        blank=True, null=True, default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk:
            self.member_count = self.members.count()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def update_counts(self):
        from tasks_app.models import Task
        self.ticket_count = Task.objects.filter(board=self).count()
        self.tasks_high_prio_count = Task.objects.filter(
            board=self, priority='high').count()
        self.tasks_to_do_count = Task.objects.filter(
            board=self, status='to-do').count()
        self.save()


class BoardDetail(models.Model):
    title = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(
        User, related_name='boards_detail')
