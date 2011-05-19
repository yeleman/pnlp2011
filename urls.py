#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from pnlp_web import urls as pnlp_urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include(pnlp_urls)),
    url(r'^admin/', include(admin.site.urls)),
)
