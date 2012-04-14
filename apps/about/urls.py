from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from about.views import what_next


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "about/about.html"}, name="about"),
    url(r"^what_next/$", what_next, name="what_next"),
)
