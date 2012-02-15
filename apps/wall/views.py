from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime

from wall.models import Wall, WallItem, WallComment
from wall.forms import WallItemForm, WallItemCommentForm

from django.utils import simplejson
import logging, traceback, pprint

@login_required
def home( request, slug, template_name='wall/home.html'):
    """
    A view that shows all of the wall items.
    (Use template_name of 'wall/recent.html' to see just recent items.)
    """
    wall = get_object_or_404( Wall, slug=slug )

    return render_to_response( template_name,
        {   "wall": wall,
            "form": WallItemForm(),
            'commentform':WallItemCommentForm()
        },
        context_instance = RequestContext( request ))

@login_required
def add( request, slug, form_class=WallItemForm,
            template_name='wall/home.html',
            success_url=None, can_add_check=None):
    """
    A view for adding a new WallItem.

    The optional 'can_add_check' callback passes you a user and a wall.
      Return True if the user is authorized and False otherwise.
      (Default: any user can create a wall item for the given wall.)
    """
    wall = get_object_or_404( Wall, slug=slug )
    if success_url == None:
        success_url = reverse( 'wall_home', args=(slug,))
    if request.method == 'POST':
        form = form_class(request.POST,request.FILES)
        if form.is_valid():
            posting = form.cleaned_data['posting']
            
            if len(posting) > wall.max_item_length:
                body = posting[:wall.max_item_length]
            else:
                body = posting
            item = WallItem( author=request.user, wall=wall, body=body, created_at=datetime.now() )
            item.save()
            
            if request.FILES:
                file_content = request.FILES['img']
                item.item_pic.save(file_content.name, file_content, save=True)
            
            return HttpResponseRedirect(success_url)
        else:
            print 'errors'
            print form.errors
    else:
        if can_add_check != None:
            allowed = can_add_check( request.user, wall )
        else:
            allowed = True
        if not allowed:
            request.user.message_set.create(
                message='You do not have permission to add an item to this wall.')
            return HttpResponseRedirect(success_url)
        form = form_class( help_text="Input text for a new item.<br/>(HTML tags will %sbe ignored. The item will be trimmed to %d characters.)" % ("not " if wall.allow_html else "", wall.max_item_length))
    return render_to_response(template_name,
        { 'form': form, 'wall': wall },
        context_instance = RequestContext( request ))

@login_required
def edit( request, id, form_class=WallItemForm,
            template_name='wall/edit.html',
            success_url=None, can_edit_check=None):
    """
    A view for editing a WallItem.

    The optional 'can_edit_check' callback passes you a user and an item.
      Return True if the user is authorized and False otherwise.
      (Default: only the item author is allowed to edit the item.)
    """
    item = get_object_or_404( WallItem, id=int(id) )
    if success_url == None:
        success_url = reverse( 'wall_home', args=(item.wall.slug,))
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            posting = form.cleaned_data['posting']
            if len(posting) > item.wall.max_item_length:
                body = posting[:item.wall.max_item_length]
            else:
                body = posting       
            item.body = body
            item.save()
            return HttpResponseRedirect(success_url)
    else:
        if can_edit_check != None:
            allowed = can_edit_check( request.user, item )
        else:
            allowed = (request.user == item.author)
        if not allowed:
            request.user.message_set.create(
                message='You do not have permission to edit that item.')
            return HttpResponseRedirect(success_url)
        form = form_class( help_text="Edit this item.<br/>(HTML tags will %sbe ignored. The item will be trimmed to %d characters.)" % ("not " if item.wall.allow_html else "", item.wall.max_item_length))
        form.fields['posting'].initial = item.body
    return render_to_response(template_name,
        { 'form': form, 'item': item, 'wall': item.wall },
        context_instance = RequestContext( request ))
    
@login_required
def commentadd( request, wallitemid, form_class=WallItemCommentForm,
            template_name='wall/comment.html',
            success_url='wall_home'):
    """
    A view for adding a new WallItemComment.

    """
    
    if not request.POST:
        form = form_class( help_text="Input text for a new comment.<br/>(HTML tags will be ignored.)")
        return render_to_response(template_name, { 'commentform': form, 'wallitemid': wallitemid }, context_instance = RequestContext( request ))

    else:
        form = form_class(request.POST)
        
        wallitem = get_object_or_404( WallItem, id=wallitemid )
        
        response_dict = {}
            
        if form.is_valid():
            
            commentbody = form.cleaned_data['comment']
            
            comment = WallComment( author=request.user, wallitem=wallitem, body=commentbody, created_at=datetime.now() )
            comment.save()
            
            response_dict.update({'itemid':comment.wallitem.id,'comment': comment.body, 'author': comment.author.get_profile().name,'created_at':comment.created_at.strftime('%b. %d, %Y %I:%M %p') })  #Feb. 14, 2012, 2:02 p.m
            response_dict.update({'success': True})
        else:
            print form.errors
            response_dict.update({'errors': form.errors})
            
        if request.is_ajax():
            return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
        
        return render_to_response(template_name, { 'commentform': form, 'wallitemid': wallitemid }, context_instance = RequestContext( request ))
