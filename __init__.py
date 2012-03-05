# -*- coding: utf-8 -*-

__about__ = """
This project takes the account_project and adds profiles and notifications.
It is a foundation suitable for many sites that have user accounts with
profiles.
"""

import sys
import traceback

from django.core.signals import got_request_exception

def exception_printer(sender, **kwargs):
    print >> sys.stderr, ''.join(traceback.format_exception(*sys.exc_info()))

got_request_exception.connect(exception_printer)
