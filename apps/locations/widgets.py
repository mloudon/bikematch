"""Custom Map widget."""
from django.conf import settings
from django.forms.forms import Media
from django.forms.util import flatatt
from django.forms.widgets import Widget
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.simplejson import dumps
from gmapi import maps
from urlparse import urljoin
from django import forms
from django.utils.safestring import mark_safe 
from locations.models import Location

# logging
import sys, logging
logger = logging.getLogger(__name__)

def init_logging():
    stdoutHandler = logging.StreamHandler( sys.stdout )
    if len(logger.handlers) < 1:
        logger.addHandler( stdoutHandler )

init_logging()

#constants for location fied widget
DEFAULT_WIDTH = 300
DEFAULT_HEIGHT = 300
DEFAULT_ZOOM = 12
DEFAULT_LAT = 34.013
DEFAULT_LON = -118.206


#constants for gmapi google map widget
JQUERY_URL = getattr(settings, 'GMAPI_JQUERY_URL',
                     'http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery'
                     '%s.js' % ('' if settings.DEBUG else '.min'))
MAPS_URL = getattr(settings, 'GMAPI_MAPS_URL',
                   'http://maps.google.com/maps/api/js?sensor=false')
# Same rules apply as ADMIN_MEDIA_PREFIX.
# Omit leading slash to make relative to MEDIA_URL.
MEDIA_PREFIX = getattr(settings, 'GMAPI_MEDIA_PREFIX', 'gmapi/')

    
class LocationWidget(forms.widgets.Widget):
    def __init__(self, *args, **kw):
        
        self.map_width = kw.get("map_width", DEFAULT_WIDTH)
        self.map_height = kw.get("map_height", DEFAULT_HEIGHT)
        self.map_zoom = kw.get("map_zoom", DEFAULT_ZOOM)
        
        super(LocationWidget, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        
        if not value:
            a,b = DEFAULT_LAT, DEFAULT_LON
        elif isinstance(value, Location):
            logger.info('rendering location: %s' % value)
            a, b = value.latitude, value.longitude
        elif isinstance(value, unicode):
             a, b = value.split(',')
        
        elif isinstance(value, int):
             location = Location.objects.get(id=value)
             a, b = location.latitude, location.longitude
        else:
            raise forms.ValidationError("Not a Location object %s" % value)
        
        lat, lng = float(a), float(b)
        
        js = '''
        <script type="text/javascript">
        //<![CDATA[
        
            var map_%(name)s;
            
            function savePosition_%(name)s(point)
            {
                var latitude = document.getElementById("id_%(name)s");
                //var longitude = document.getElementById("id_%(name)s_longitude");
                latitude.value = point.lat().toFixed(6) + "," + point.lng().toFixed(6);
                //longitude.value = point.lng().toFixed(6);
                map_%(name)s.panTo(point);
            }
        
            function load_%(name)s() {
                if (GBrowserIsCompatible()) {
                    map_%(name)s = new GMap2(document.getElementById("map_%(name)s"));
                    map_%(name)s.addControl(new GSmallMapControl());
                    map_%(name)s.addControl(new GMapTypeControl());
        
                    var point = new GLatLng(%(lat)f, %(lng)f);
                    map_%(name)s.setCenter(point, %(zoom)d);
                    map_%(name)s.setCenter(point, %(zoom)d);
                    map_%(name)s.enableScrollWheelZoom()
                    map_%(name)s.enableDragging() 
                    m = new GMarker(point, {draggable: true});
        
                    GEvent.addListener(m, "dragend", function() {
                            point = m.getPoint();
                            savePosition_%(name)s(point);
                    });
        
                    map_%(name)s.addOverlay(m);
        
                    /* save coordinates on clicks */
                    GEvent.addListener(map_%(name)s, "click", function (overlay, point) {
                        savePosition_%(name)s(point);
                    
                        map_%(name)s.clearOverlays();
                        m = new GMarker(point, {draggable: true});
        
                        GEvent.addListener(m, "dragend", function() {
                            point = m.getPoint();
                            savePosition_%(name)s(point);
                        });
        
                        map_%(name)s.addOverlay(m);
                    });
                }
            }
        //]]>
        </script>
        ''' % dict(name=name, lat=lat, lng=lng, zoom=self.map_zoom)
        html = self.inner_widget.render("%s" % name, "%f,%f" % (lat,lng), dict(id='id_%s' % name))
        html += "<div id=\"map_%s\" class=\"gmap\" style=\"width: %dpx; height: %dpx\"></div>" % (name, self.map_width, self.map_height)
        
        help_text = "Drag the marker to select your location"
        html +='<span class="help-block"> %s </span>' % help_text
        
        return mark_safe(js+html)


class LocationField(forms.Field):
    widget = LocationWidget

    def clean(self, value):
        if isinstance(value, unicode):
            a, b = value.split(',')
            
        else:
            a, b = value
        
        lat, lng = float(a), float(b)
        return Location.objects.create(latitude = lat, longitude = lng, automatic = True)

class GoogleMap(Widget):
    def __init__(self, attrs=None):
        self.nojquery = (attrs or {}).pop('nojquery', False)
        self.nomapsjs = (attrs or {}).pop('nomapsjs', False)
        super(GoogleMap, self).__init__(attrs)

    def render(self, name, gmap, attrs=None):
        if gmap is None:
            gmap = maps.Map()
        default_attrs = {'id': name, 'class': 'gmap'}
        if attrs:
            default_attrs.update(attrs)
        final_attrs = self.build_attrs(default_attrs)
        
        # TODO this should not be hard-coded
        style = (u'width: 100%; height: 100%')
        final_attrs['style'] = style + final_attrs.get('style', '')
        
        map_div = (u'<div class="%s" style="'
                   u'width: 940px; height: 600px; position:absolute;"></div>' %
                   (escape(dumps(gmap, separators=(',', ':')))))
        
        return mark_safe(u'<div%s>%s</div>' %
                         (flatatt(final_attrs), map_div))
    def _media(self):
        js = []
        if not self.nojquery:
            js.append(JQUERY_URL)
        if not self.nomapsjs:
            js.append(MAPS_URL)
        js.append(urljoin(MEDIA_PREFIX, 'js/jquery.gmapi%s.js' %
                  ('' if settings.DEBUG else '.min')))
        return Media(js=js)

    media = property(_media)
