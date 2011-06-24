#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.template import RequestContext, loader
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, HttpResponse

from pnlp_web.http import Http403


def access_forbidden(request, template_name='403.html', *args, **kwargs):
    """ renders 403.html in context to be used by Http403 Exception """
    t = loader.get_template(template_name)
    return HttpResponseForbidden(t.render(RequestContext(request, \
                                              {'request_path': request.path})))


class Http403Middleware(object):
    """ catches Http403 and returns access_forbidden view """
    def process_exception(self, request, exception):
        if isinstance(exception, Http403):
            if settings.DEBUG:
                raise PermissionDenied
            return access_forbidden(request)
