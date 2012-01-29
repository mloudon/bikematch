from django.db import models

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    accuracy = models.FloatField(null=True, blank=True) #in meters
    time_zone = models.CharField(max_length=100, null=True, blank=True)
    automatic = models.BooleanField(default=False) #true if location was created
      #by an external API based just on lat/lon, and other fields were guessed at
      #automatically

    def __unicode__(self):
        coords = '(%.3f, %.3f)' % (self.latitude, self.longitude)
        return  coords

