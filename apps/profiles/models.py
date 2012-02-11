from django.db import models
from django.utils.translation import ugettext_lazy as _

from idios.models import ProfileBase
from locations.models import Location
from imagekit.models import ImageSpec
from imagekit.processors import resize, Adjust
import Image

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

class Border(object):
    
    def process(self, img):
        x,y = img.size
        brdrs=[(1, "Grey"), (2, "Black")]
        width = sum([ z[0] for z in brdrs ])
        bordered = Image.new("RGB", (x+(2*width), y+(2*width)), "Grey")
        offset = 0
        print offset
            
        for b_width, b_color in brdrs:
            bordered.paste(Image.new("RGB", (x+2*(width-offset),y+2*(width-offset)), b_color), (offset, offset))
            offset = offset + b_width
    
        bordered.paste(img, (offset, offset))
        return bordered
    

class Profile(ProfileBase):
    name = models.CharField(_("Name"), max_length=50, null=True, blank=True)
    about = models.TextField(_("About"), null=True, blank=True)
    zip_code = models.CharField("* Zip code",max_length=10, null=True, blank=True)
    
    profile_pic = models.ImageField(upload_to='upload',null=True,)
    profile_pic_small = ImageSpec([Adjust(contrast=1.2, sharpness=1.1),
            resize.Crop(40, 40)], image_field='profile_pic',
            format='JPEG', options={'quality': 90})
    profile_pic_small_border = ImageSpec([Adjust(contrast=1.2, sharpness=1.1),
            resize.Crop(40, 40), Border()], image_field='profile_pic',
            format='JPEG', options={'quality': 90})
    
    #TODO use postgis?
    location = models.ForeignKey(Location, null=True, blank=True)
    
    days_per_week = models.DecimalField("How many days per week do you commute by bike?",max_digits=1, decimal_places=0, choices=DAYS_PER_WEEK_CHOICES, null=True, blank=True)
    oneway_dist = models.DecimalField("How many miles is your one-way commute",max_digits=4, decimal_places=2, null=True, blank=True)
    oneway_time =models.DecimalField("How many minutes does your one-way commute typically take?",max_digits=3, decimal_places=0, null=True, blank=True)

        
