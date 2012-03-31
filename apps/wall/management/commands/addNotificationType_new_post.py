from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
            
    def create_notice_types(self):
        if "notification" in settings.INSTALLED_APPS:
            from notification import models as notification
            notification.create_notice_type("wall_new_post", _("New Wall Post"), _("there is a new post on the wall"))
        else:
            print "Skipping creation of NoticeTypes as notification app not found"
    
    def handle_noargs(self, **options):
        self.create_notice_types()