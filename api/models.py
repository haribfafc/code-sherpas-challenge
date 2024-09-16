from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    photo_url = models.CharField(max_length=1024, null=True)
    creator = models.ForeignKey(User, related_name="creator", on_delete=models.SET_NULL, null=True)
    last_modifier = models.ForeignKey(User, related_name="last_modifier", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
