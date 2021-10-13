from django.db import models

from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict

User = get_user_model()

class Bin(models.Model):
    name = models.CharField(max_length=64, unique=True)

class Request(models.Model):
    bin = models.ForeignKey(
        Bin,
        on_delete=models.CASCADE,
        related_name='requests',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    url = models.TextField()
    method = models.CharField(max_length=16)
    params = models.TextField()
    headers = models.TextField()
    body = models.TextField()

    ip = models.TextField()
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()

    def as_dict(self):
        return model_to_dict(self)
