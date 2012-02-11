from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.sites.models import Site , RequestSite
from django.contrib.auth.views import login as django_login
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.html import escape 
from django import forms

import datetime, random, sys, os

from django.conf import settings

from gmapi import maps
from bikematchapp.forms import MapForm
from profiles.models import Profile


# import the logging library
import logging

logger = logging.getLogger(__name__)

def init_logging():
    stdoutHandler = logging.StreamHandler(sys.stdout)
    if len(logger.handlers) < 1:
        logger.addHandler(stdoutHandler)

init_logging()

@login_required
def index(request):
    error_message = ""
    try: 
        profile = request.user.get_profile()
    except:
        return redirect('/profiles/create')
        
    return render_to_response('bikematchapp/mapview.html', {
        'error_message': error_message,
    }, context_instance=RequestContext(request))

def mapview(request, template_name='bikematchapp/mapview.html'):
    gmap = maps.Map(opts={
        'center': maps.LatLng(34.11, -118.27),
        'mapTypeId': maps.MapTypeId.HYBRID,
        #'size': maps.Size(800,600),
        'zoom': 10,
        'mapTypeControlOptions': {
             'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        },
    })
    
    
    
    for profile in Profile.objects.all():
        if profile.location:
            
            if profile.profile_pic_small.url:
                image = os.path.join(profile.profile_pic_small_border.url) 
            else:
                image = os.path.join(settings.STATIC_URL, "images", "bike_blue.png")
                       
            marker = maps.Marker(opts={
                                     'map': gmap,
                                     'position': maps.LatLng(profile.location.latitude, profile.location.longitude),
                                     'icon' : image,
                                     'proj_id': profile.user.id
        
                                     })
            
            maps.event.addListener(marker, 'mouseover', 'myobj.markerOver')
            maps.event.addListener(marker, 'mouseout', 'myobj.markerOut')
            maps.event.addListener(marker, 'click', 'myobj.onClick')
            
            #contentString = '<div id="infobox" class="infobox" > User: %s </div>' % escape(profile.user.username)
            contentString = '<p>user: %s</p><p><a href="messages/compose/%s">message this user</a></p>' % (escape(profile.user.username),escape(profile.user.username))
    
            info = maps.InfoWindow({
                                    'content': contentString,
                                    'disableAutoPan': True
                                    })
            info.open(gmap, marker)
    
    return render_to_response(
    template_name, {
        'form': MapForm(initial={'map': gmap})
    }, context_instance=RequestContext(request))
    

def root_index(request):
    return redirect('/') 

