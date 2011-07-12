#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.template import RequestContext, loader
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.csrf import requires_csrf_token
from django.http import Http404
from pnlp_web.http import Http403


@requires_csrf_token
def access_forbidden(request, message=None, \
                     template_name='403.html', *args, **kwargs):
    """ renders 403.html in context to be used by Http403 Exception """
    t = loader.get_template(template_name)
    return HttpResponseForbidden(t.render(RequestContext(request, \
                                              {'request_path': request.path, \
                                               'message': message})))


@requires_csrf_token
def page_not_found(request, message=None, \
                     template_name='404.html', *args, **kwargs):
    """ renders 404.html in context to be used by Http404 Exception """
    t = loader.get_template(template_name)
    return HttpResponseForbidden(t.render(\
            RequestContext(request, \
                           {'request_path': request.path, \
                            'message': message, \
                            'referrer': request.META.get('HTTP_REFERER', \
                                                         None)})))


@requires_csrf_token
def access_error(request, message=None, \
                     template_name='500.html', *args, **kwargs):
    """ renders 500.html in context to be used by uncathed Exception """
    t = loader.get_template(template_name)
    return HttpResponseNotFound(t.render(\
            RequestContext(request, \
                           {'request_path': request.path, \
                            'message': message, \
                            'referrer': request.META.get('HTTP_REFERER', \
                                                         None)})))


class Http403Middleware(object):
    """ catches Http403 and returns access_forbidden view """
    def process_exception(self, request, exception):
        if isinstance(exception, Http403):
            return access_forbidden(request, exception.message)


class Http404Middleware(object):
    """ catches Http404 and returns page_not_found view """
    def process_exception(self, request, exception):
        # catch only Http404 exceptions
        if isinstance(exception, Http404):
            # return page_not_found with exception's message
            return page_not_found(request, exception.message)


class Http500Middleware(object):
    """ catches unhandled Exception and displays access_error view """
    def process_exception(self, request, exception):
        # catch all exception.
        # that's why we need to put it last in middleware config.
        # /!\ middlewares are processed bottom-up.
        if isinstance(exception, Exception):
            # if debug mode, just forwards it to django
            if settings.DEBUG == True:
                raise exception
            # if not, display access_error and load it with exception details
            message = u"%s: %s" % (exception.__class__.__name__, \
                                   exception.message)
            return access_error(request, message)

    def process_response(self, request, response):
        # catch non-exception HTTP 500 responses.
        if response.status_code == 500 and settings.DEBUG == False:
            # we are filling error message with whatever the response is.
            # this could be terrible if content is a webpage although not
            # that likely to happen.
            return access_error(request, u"Unknown")
        return response
