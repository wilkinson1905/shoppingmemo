from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.TextField()
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    order = models.IntegerField()

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.text
