from django.db import models


class Tasks(models.Model):
    total = models.IntegerField(default=0)
    done = models.IntegerField(default=0)
    error = models.IntegerField(default=0)
    success = models.BooleanField(default=False)

    def __str__(self):
        return str("{}|{}|{}".format(self.total, self.done, self.error))
