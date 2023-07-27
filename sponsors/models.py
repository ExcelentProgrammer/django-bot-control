from django.db import models


class Sponsors(models.Model):
    link = models.CharField(max_length=255)
    name = models.CharField(max_length=1000)
    pic = models.ImageField(upload_to='chanels_pics/', default="chanels_pics/default.png")
    
    def __str__(self) -> str:
        return self.name