from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatewords
from imagekit.models import ImageSpec
from imagekit.processors import resize, Adjust

from django.db.models import signals
from django.dispatch import receiver
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None
    
import HTMLParser
                        
class WallComment(models.Model):
    """
    A comment on a wall post.
    """
    wallitem   = models.ForeignKey('WallItem')
    author     = models.ForeignKey(User, related_name="wall_comment_author")
    body       = models.TextField(_('item_body'))
    created_at = models.DateTimeField(_('created at'), default=datetime.now)
    deleted = models.BooleanField(default=False)
    
    class Meta:
        verbose_name        = _('wallitemcomment')
        verbose_name_plural = _('wallitemcomments')
        ordering            = ('-created_at',) 
        get_latest_by       = 'created_at'

    def deleteable_by(self, user):
        return user == self.author or user.is_superuser
    
    def __unicode__(self):
         return 'comment on wall item created by %s on %s ( %s )' % ( self.author.username, self.created_at, truncatewords(self.body, 9 ))

class WallItem(models.Model):
    """
    A simple note to post on a shared wall.
    """
    wall       = models.ForeignKey('Wall')
    author     = models.ForeignKey(User, related_name="wall_item_author")
    body       = models.TextField(_('item_body'), help_text='Use the editor to add links; no embedded html allowed.')
    created_at = models.DateTimeField(_('created at'), default=datetime.now)
    deleted = models.BooleanField(default=False)
    item_pic = models.ImageField(upload_to='upload',null=True,)
    item_pic_800x600 = ImageSpec([Adjust(contrast=1.2, sharpness=1.1),
            resize.Fit(800,600, False)], image_field='item_pic',
            format='JPEG', options={'quality': 90})
    item_pic_resized = ImageSpec([Adjust(contrast=1.2, sharpness=1.1),
            resize.Fit(300, 300)], image_field='item_pic',
            format='JPEG', options={'quality': 90})

    class Meta:
        verbose_name        = _('wallitem')
        verbose_name_plural = _('wallitems')
        ordering            = ('-created_at',) 
        get_latest_by       = 'created_at'
        
    def deleteable_by(self, user):
        return user == self.author or user.is_superuser
    
    def active_comments_set(self):
        return WallComment.objects.filter(wallitem=self, deleted=False)

    def __unicode__(self):
        return 'wall item created by %s on %s ( %s )' % ( self.author.username, self.created_at, truncatewords(self.body, 9 ))

class Wall(models.Model):
    """
    A shared place to post items.

    The management command "trimWallItems" will trim the number of saved
    wall items back down to the limit set by max_items (although this
    command also provides an optional override of that limit.)
    Other than that, this limit is not actively enforced as users are
    generally allowed to edit or delete their previously posted items.

    At the end of the editing process, the user supplied body for an
    item is silently trimmed to 'max_item_length'.

    The allow_html setting is reflected in help_text for the user and
    injects the use of 'striptags' in the wall home template as required.
    """
    name = models.CharField(_('name'), max_length=80)
    slug = models.SlugField(_("slug"), unique=True )
    max_items = models.IntegerField( default=50 )
    max_item_length = models.IntegerField( default = None, null=True )
    allow_html = models.BooleanField( default=False )

    class Meta:
        verbose_name = _('wall')
        verbose_name_plural = _('wall')

    def __unicode__(self):
        return self.name
    
    def active_items_set(self):
        return WallItem.objects.filter(wall=self, deleted=False)

    def get_recent_items( self, amount=5, days=7):
        """
        This shortcut function allows you to get recent items.
        -- amount is the max number of items to fetch.
        -- days optionally specifies how many days to go back. 
            (if days is <= 0, don't worry abot how old the items are.)
        """
        if days <= 0:
            # get most recent items regardless of how old
            return WallItem.objects.filter(wall=self)[:amount]
        td = timedelta(days=days)
        dt = datetime.now() - td
        return WallItem.objects.filter(wall=self,created_at__gt=dt)[:amount]
    
    
@receiver(signals.post_save, sender=WallItem)
def notify_new_post(sender, **kwargs):
    
    item = kwargs['instance']
    if notification and not item.deleted:
        already_notified=[item.author]
        h = HTMLParser.HTMLParser()
        data = {'item_author': item.author.get_profile().name,}
        
        users=[]
        for u in User.objects.all():
            if (u not in already_notified):
                users.append(u)
            
        notification.send(users, "wall_new_post", data)
        

@receiver(signals.post_save, sender=WallComment)
def notify_comment(sender, **kwargs):
    
    comment = kwargs['instance']
    if notification and not comment.deleted:
        already_notified=[comment.author]
        
        data = {'comment_body': comment.body,'comment_author': comment.author.get_profile().name,}
        
        if comment.wallitem.author not in already_notified:
            notification.send([comment.wallitem.author], "wall_new_comment_your_post", data)
            #print 'notify comment! new comment your post'
            already_notified.append(comment.wallitem.author)
        
        for comm in comment.wallitem.active_comments_set():
            if comm.author not in already_notified:
                notification.send([comm.author], "wall_new_comment_your_comment", data)
                already_notified.append(comm.author)
                #print 'notify comment! new comment your comment'
 

