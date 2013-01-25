#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import os

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from settings import STATIC_ROOT, MEDIA_ROOT

from snisi_web import urls as pnlp_urls
from snisi_web import views

admin.autodiscover()

if hasattr(settings, 'SYSTEM_CLOSED') and settings.SYSTEM_CLOSED:
    urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
        url(r'', direct_to_template, {'template': 'closed.html'}, name='index'),

    # development only
    url(r'^static/admin/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': os.path.join(os.path.dirname(\
                                            os.path.abspath(admin.__file__)),
                               'media'), 'show_indexes': True},
             name='static_admin'),

    url(r'^static/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': STATIC_ROOT, 'show_indexes': True},
             name='static'),

    url(r'^media/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': MEDIA_ROOT, 'show_indexes': True},
             name='media'),

    )
else:
    urlpatterns = patterns('',
        url(r'', include(pnlp_urls)),
        url(r'^admin/', include(admin.site.urls)),
    )
