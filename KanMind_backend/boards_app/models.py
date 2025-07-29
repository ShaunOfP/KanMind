from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    title = models.CharField(max_length=30)
    member_count = models.PositiveIntegerField(default=0)
    members = models.ManyToManyField(User, related_name='boards', blank=True)
    ticket_count = models.IntegerField(blank=True, null=True)
    tasks_to_do_count = models.IntegerField(blank=True, null=True)
    tasks_high_prio_count = models.IntegerField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk:
            self.member_count = self.members.count()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BoardDetail(models.Model):
    title = models.CharField(max_length=30)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(
        User, related_name='boards_detail', blank=True)
    # tasks = models.ForeignKey(
    #     Task, related_name='boards_tasks', blank=True)

    # kommentare und tasks werden gelöscht wenn board gelöscht wird
