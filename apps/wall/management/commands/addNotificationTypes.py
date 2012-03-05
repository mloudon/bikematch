from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
            
    def create_notice_types(self):
        if "notification" in settings.INSTALLED_APPS:
            from notification import models as notification
            notification.create_notice_type("wall_new_comment_your_post", _("New Comment on Wall Post You Created"), _("someone has commented on your wall post"))
            notification.create_notice_type("wall_new_comment_your_comment", _("New Comment on Wall Post You Commented On"), _("someone has commented on a wall post you commented on"))
        else:
            print "Skipping creation of NoticeTypes as notification app not found"
    
    def handle_noargs(self, **options):
        self.create_notice_types()