from django.db import models

# Create your models here.
class Acc(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class Parsing(models.Model):
    currentState = models.BooleanField(default=False)
    currentTotal = models.IntegerField(default=0)
    currentVar = models.IntegerField(default=0)
    result = models.TextField(default='[]')
    info = models.TextField(default='[]', blank=True, null=True)