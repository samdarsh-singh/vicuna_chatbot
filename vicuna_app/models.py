from django.db import models
from django.contrib.auth.models import User

class License(models.Model):
    key = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
