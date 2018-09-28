from django.db import models


# Create your models here.

class Stat(models.Model):
    path = models.TextField()
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_created=True)

    class Meta:
        unique_together = ('path', 'name')


class App(models.Model):
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, primary_key=True)
    created = models.DateTimeField(auto_created=True)
