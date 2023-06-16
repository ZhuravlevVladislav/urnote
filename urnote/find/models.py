from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=200, default='')
    artist = models.CharField(max_length=200, default='')
    youtube_link = models.CharField(max_length=300, default='')
    bpm = models.IntegerField(default=0)
