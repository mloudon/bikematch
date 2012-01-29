from django.conf.urls.defaults import *

from profiles.views import ProfileListView, ProfileDetailView


urlpatterns = patterns("profiles.views",
    url(r"^profile/(?P<username>[\w\._-]+)/$", ProfileDetailView.as_view(), name="profile_detail"),
    url(r"^(?P<profile_slug>[\w\._-]+)/profile/(?P<profile_pk>\d+)/$", ProfileDetailView.as_view(), name="profile_detail"),
    url(r"^all/$", ProfileListView.as_view(all_profiles=True), 
            name="profile_list_all"),
    url(r"", include("profiles.urls_base")),
    url(r"^(?P<profile_slug>[\w\._-]+)/", include("profiles.urls_base")),
)
