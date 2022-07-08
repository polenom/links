from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Links(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')
    inlink = models.CharField(max_length=400)
    onlink = models.CharField(max_length=400, blank=True, null=True, default=None)