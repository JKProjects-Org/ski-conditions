from django.db import models
from django.utils import timezone


# Create your models here.
class SkiResort(models.Model):
    resort_name = models.CharField(max_length=200, unique=True)
    trails_open = models.IntegerField(default=0)
    lifts_open = models.IntegerField(default=0)
    acres_open = models.IntegerField(default=0)
    terrain_percent = models.IntegerField(default=0)

    # string of total trails, ex. "/ 128"
    total_trails = models.CharField(max_length=200, default='0')
    # string of total lifts, ex. "/ 21"
    total_lifts = models.CharField(max_length=200, default='0')

    '''
    # time accessed
    created_on = models.DateTimeField(default=timezone.now())
    '''
