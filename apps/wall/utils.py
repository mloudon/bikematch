from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

import html5lib
from html5lib import sanitizer

@register.filter
@stringfilter
def sanitize(value):
    p = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)
    return p.parseFragment(value).toxml()