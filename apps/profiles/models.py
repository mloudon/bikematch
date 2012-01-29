from django.db import models
from django.utils.translation import ugettext_lazy as _

from idios.models import ProfileBase
from locations.models import Location

DAYS_PER_WEEK_CHOICES = (
    (0, "none, but I'd like to start!"),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
)

class Profile(ProfileBase):
    name = models.CharField(_("Name"), max_length=50, null=True, blank=True)
    about = models.TextField(_("About"), null=True, blank=True)
    zip_code = models.CharField("* Zip code",max_length=10, null=True, blank=True)
    
    #TODO use postgis?
    location = models.ForeignKey(Location, null=True, blank=True)
    
    days_per_week = models.DecimalField("How many days per week do you commute by bike?",max_digits=1, decimal_places=0, choices=DAYS_PER_WEEK_CHOICES, null=True, blank=True)
    oneway_dist = models.DecimalField("How many miles is your one-way commute",max_digits=4, decimal_places=2, null=True, blank=True)
    oneway_time =models.DecimalField("How many minutes does your one-way commute typically take?",max_digits=3, decimal_places=0, null=True, blank=True)
    
