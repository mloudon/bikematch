from django.template import RequestContext
from django.shortcuts import redirect,render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def what_next(request):
    error_message = ""
    try: 
        profile = request.user.get_profile()
        name = profile.name
        location = profile.location
        
        if (name == None) or ( location == None):
            return HttpResponseRedirect(reverse('profile_edit_noescape'))
        
    except:
        return HttpResponseRedirect(reverse('profile_edit_noescape'))
        
    return render_to_response('about/what_next.html', {
        'error_message': error_message,
    }, context_instance=RequestContext(request))