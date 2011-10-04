#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import os

from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from pnlp_web import views
from pnlp_web.decorators import provider_permission
from settings import STATIC_ROOT, MEDIA_ROOT

RGXP_ENTITY = '(?P<entity_code>[a-zA-Z0-9\-\_]+)'
RGXP_RECEIPT = '(?P<report_receipt>[a-zA-Z\#\-\_\.0-9\/]+)'
RGXP_PERIOD = '(?P<period_str>[0-9]{6})'
RGXP_PERIODS = '(?P<period_str>[0-9]{6}-[0-9]{6})'
RGXP_SECTION = 'section(?P<section_index>[0-9]{1,2}[ab]{0,1})'
RGXP_SUBSECTION = '(?P<sub_section>[a-z\_]+)'

urlpatterns = patterns('',
    (r'^nosms/', include('nosms.urls')),

    url(r'^/?$', views.dashboard.dashboard, name='index'),
    url(r'^profile/$', views.profile.edit_profile, name='profile'),

    # login
    url(r'^login/$', 'django.contrib.auth.views.login', \
         {'template_name': 'login_django.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', \
         {'template_name': 'logout_django.html'}, name='logout'),

    # district
    url(r'^upload/$', views.excel_upload.upload_form, name='upload'),

    # district, region
    url(r'^validation/$', \
        views.validation.validation_list, name='validation'),
    url(r'^validation/do/' + RGXP_RECEIPT + '$', \
        views.validation.report_do_validation, name='report_do_validation'),
    url(r'^validation/' + RGXP_RECEIPT + '$', \
        views.validation.report_validation, name='report_validation'),

    # ALL
    url(r'^raw_data/' + RGXP_ENTITY + '/' + RGXP_PERIOD + '$', \
        views.raw_data.data_browser, name='raw_data'),
    url(r'^raw_data/' + RGXP_ENTITY + '$', \
        views.raw_data.data_browser, name='raw_data'),
    url(r'^raw_data/$', views.raw_data.data_browser, name='raw_data'),
    url(r'^raw_data/excel/' + RGXP_RECEIPT + '$', \
        views.raw_data.excel_export, name='raw_data_excel'),

    # Indicator Views
    url(r'^browse/' + RGXP_ENTITY + '/' + RGXP_PERIODS + '/' \
         + RGXP_SECTION + '/' + RGXP_SUBSECTION + '$', \
        views.indicators.indicator_browser, name='indicator_data'),
    url(r'^browse/' + RGXP_ENTITY + '/' + RGXP_PERIODS + '/' \
         + RGXP_SECTION + '$', \
        views.indicators.indicator_browser, name='indicator_data'),
    url(r'^browse/' + RGXP_ENTITY + '/' + RGXP_PERIODS + '$', \
        views.indicators.indicator_browser, name='indicator_data'),
    url(r'^browse/' + RGXP_ENTITY + '$', \
        views.indicators.indicator_browser, name='indicator_data'),
    url(r'^browse/$', views.indicators.indicator_browser, \
        name='indicator_data'),

    # ANTIM : USERS
    url(r'^users/?$', \
        provider_permission('can_manage_users')(views.providers. \
                                                ProvidersListView.as_view()), \
        name='list_users'),
    url(r'^users/add$', views.providers.add_edit_user, name='add_user'),
    url(r'^users/edit/(?P<user_id>[0-9]+)$', \
        views.providers.add_edit_user, name='edit_user'),
    url(r'^users/disable/(?P<user_id>[0-9]+)$', \
        views.providers.enable_disable_user, name='disable_user', \
        kwargs={'activate': False}),
    url(r'^users/enable/(?P<user_id>[0-9]+)$', \
        views.providers.enable_disable_user, name='enable_user', \
        kwargs={'activate': True}),
    url(r'^users/new_password/(?P<user_id>[0-9]+)$', \
        views.providers.password_user, name='password_user'),

    # ANTIM : ENTITIES
    url(r'^entities/?$', \
        provider_permission('can_manage_entities')(views.entities. \
                                                EntitiesListView.as_view()), \
        name='list_entities'),
    url(r'^entities/add$', views.entities.add_edit_entity, name='add_entity'),
    url(r'^entities/edit/(?P<entity_id>[0-9]+)$', \
        views.entities.add_edit_entity, name='edit_entity'),

    # static web pages
     url(r'^support/$', views.dashboard.contact, name='support'),
     url(r'^help/$', direct_to_template, \
         {'template': 'help.html'}, name='help'),
     url(r'^about/$', direct_to_template, \
         {'template': 'about.html'}, name='about'),

     url(r'^annuaire/$', views.addressbook.addressbook, name='addressbook'),

    # CSCOM credit
     url(r'^malitel/$', direct_to_template, \
         {'template': 'malitel.html'}, name='malitel'),

    # development only
    url(r'^static/admin/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': os.path.join(os.path.dirname(\
                                            os.path.abspath(admin.__file__)), \
                               'media'), 'show_indexes': True}, \
             name='static_admin'),

    url(r'^static/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': STATIC_ROOT, 'show_indexes': True}, \
             name='static'),

    url(r'^media/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': MEDIA_ROOT, 'show_indexes': True}, \
             name='media'),

    # demo purposes
    url(r'^date/?$', views.dashboard.change_date, name='date'),
)
