from django.db import models

# Create your models here.
class SkiResort(models.Model):
    resort_name = models.CharField(max_length=200)
    trails_open = models.IntegerField(default=0)
    lifts_open = models.IntegerField(default=0)
    acres_open = models.IntegerField(default=0)
