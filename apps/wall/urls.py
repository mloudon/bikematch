from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', 'wall.views.home', name="wall_home"),
    url(r'^recent/(?P<slug>[-\w]+)/$', 'wall.views.home', { 'template_name':'wall/recent.html' }, name="wall_recent"),
    url(r'^add/(?P<slug>[-\w]+)/$', 'wall.views.add', name="add_wall_item"),
    url(r'^addcomment/(?P<wallitemid>[-\d]+)/$', 'wall.views.commentadd', name="add_wall_comment"),
    url(r'^delete/(?P<id>\d+)/$', 'wall.views.delete', name="delete_wall_item"),
    url(r'^deletecomment/(?P<id>\d+)/$', 'wall.views.commentdelete', name="delete_wall_comment"),
)
