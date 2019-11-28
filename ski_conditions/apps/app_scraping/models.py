from django.db import models


class SkiResort(models.Model):
    resort_name = models.CharField(max_length=200, unique=True)

    # trail and lift data
    trails_open = models.IntegerField(default=0)
    lifts_open = models.IntegerField(default=0)
    acres_open = models.IntegerField(default=0)
    terrain_percent = models.IntegerField(default=0)
    total_trails = models.IntegerField(default=0)
    total_lifts = models.IntegerField(default=0)

    # snow report data
    overnight_snowfall = models.IntegerField(default=0)
    twenty_four_hour_snowfall = models.IntegerField(default=0)
    forty_eight_hour_snowfall = models.IntegerField(default=0)
    seven_day_snowfall = models.IntegerField(default=0)
    base_depth = models.IntegerField(default=0)
    current_season = models.IntegerField(default=0)

    def __str__(self):
        return self.resort_name
