from django.db import models

# Create your models here.


class HistoryResult(models.Model):
    restaurant_name = models.CharField(max_length=255)
    date = models.CharField(max_length=100)
