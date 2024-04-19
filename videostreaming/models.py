from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    name = models.CharField(max_length=100)
    video_url = models.URLField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
