from django.db import models


class User(models.Model):
    user_id = models.BigIntegerField(unique=True)

    def __str__(self) -> str:
        return str(self.user_id)


class Videos(models.Model):
    file_id = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    video_id = models.CharField(max_length=255, blank=True, null=True)
