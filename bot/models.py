from django.db import models


class User(models.Model):
    user_id = models.BigIntegerField(unique=True)

    def __str__(self) -> str:
        return str(self.user_id)
