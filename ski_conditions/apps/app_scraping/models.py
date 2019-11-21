from django.db import models
from django.utils import timezone


class SkiResort(models.Model):
    resort_name = models.CharField(max_length=200, unique=True)
    trails_open = models.IntegerField(default=0)
    lifts_open = models.IntegerField(default=0)
    acres_open = models.IntegerField(default=0)
    terrain_percent = models.IntegerField(default=0)

    total_trails = models.IntegerField(default=0)
    total_lifts = models.IntegerField(default=0)

    def __str__(self):
        return self.resort_name

