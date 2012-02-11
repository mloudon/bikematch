from profiles.models import Profile
from locations.widgets import LocationField
from django.forms import ModelForm

DAYS_PER_WEEK_CHOICES = (
    ('none, but I\'d like to start!', 0),
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
    ('6', 6),
    ('7', 7),
)

class EditProfileForm(ModelForm):
    location = LocationField(label="Location")
    
    class Meta:
        model = Profile
        fields = ('name',
                  'profile_pic',
                  'about',
                  'location',
                  'days_per_week',
                  'oneway_dist',
                  'oneway_time',
                  )
      
class CreateProfileForm(ModelForm):
    location = LocationField(label="Location")
    
    class Meta:
        model = Profile
        fields = ('name',
                  'profile_pic',
                  'about',
                  'location',
                  'days_per_week',
                  'oneway_dist',
                  'oneway_time',
                  )