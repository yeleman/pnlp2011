#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import os

from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

from snisi_web.views import monitoring as monit_views
from snisi_web.views import malaria as mviews
from snisi_web.views import epidemiology as epidviews
from snisi_web.views import reproduction as repviews
from bolibana.web import views as bviews
from bolibana.web.decorators import provider_permission
from settings import STATIC_ROOT, MEDIA_ROOT

RGXP_ENTITY = '(?P<entity_code>[a-zA-Z0-9\-\_]+)'
RGXP_RECEIPT = '(?P<report_receipt>[a-zA-Z\#\-\_\.0-9\/]+)'
RGXP_PERIOD = '(?P<period_str>[0-9]{6})'
RGXP_PERIODS = '(?P<period_str>[0-9]{6}-[0-9]{6})'
RGXP_SECTION = 'section(?P<section_index>[0-9]{1,2}[ab]{0,1})'
RGXP_SUBSECTION = '(?P<sub_section>[a-z\_]+)'

urlpatterns = patterns('',

    url(r'^/?$', mviews.dashboard.dashboard, name='index'),
    url(r'^profile/$', bviews.profile.edit_profile, name='profile'),

    # login
    url(r'^login/$', 'django.contrib.auth.views.login',
         {'template_name': 'login_django.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
         {'template_name': 'logout_django.html'}, name='logout'),

    # district
    url(r'^upload/$', mviews.excel_upload.upload_form, name='upload'),

    # district, region
    url(r'^validation/$',
        mviews.validation.validation_list, name='validation'),
    url(r'^validation/do/' + RGXP_RECEIPT + '$',
        mviews.validation.report_do_validation, name='report_do_validation'),
    url(r'^validation/' + RGXP_RECEIPT + '$',
        mviews.validation.report_validation, name='report_validation'),

    # ALL
    url(r'^raw_data/' + RGXP_ENTITY + '/' + RGXP_PERIOD + '$',
        mviews.raw_data.data_browser, name='raw_data'),
    url(r'^raw_data/' + RGXP_ENTITY + '$',
        mviews.raw_data.data_browser, name='raw_data'),
    url(r'^raw_data/$', mviews.raw_data.data_browser, name='raw_data'),
    url(r'^raw_data/excel/' + RGXP_RECEIPT + '$',
        mviews.raw_data.excel_export, name='raw_data_excel'),

    # Indicator Views
    url(r'^browse/' + RGXP_ENTITY + '/' + RGXP_PERIODS + '/'
         + RGXP_SECTION + '/' + RGXP_SUBSECTION + '$',
        mviews.indicators.indicator_browser, name='indicator_data'),
    url(r'^browse/' + RGXP_ENTITY + '/' + RGXP_PERIODS + '/'
         + RGXP_SECTION + '$',
        mviews.indicators.indicator_browser, name='indicator_data'),
    url(r'^browse/' + RGXP_ENTITY + '/' + RGXP_PERIODS + '$',
        mviews.indicators.indicator_browser, name='indicator_data'),
    url(r'^browse/' + RGXP_ENTITY + '$',
        mviews.indicators.indicator_browser, name='indicator_data'),
    url(r'^browse/$', mviews.indicators.indicator_browser,
        name='indicator_data'),

    # ANTIM : Transmission
    url(r'^monitoring/source_data/?$', monit_views.source_data,
        name='monitoring_source_data'),
    url(r'^monitoring/messages_log/?$', monit_views.messages_log,
        name='monitoring_messages_log'),
    url(r'^monitoring/validation/?$', monit_views.validation,
        name='monitoring_validation'),
    url(r'^monitoring/bulk_messaging/?$', monit_views.bulk_messaging,
        name='monitoring_messaging'),

    # Reproduction
    url(r'^repod_dashboard/$', repviews.dashboard.dashboard,
       name='reprod_index'),

    # Epidemiology
    url(r'^epid_dashboard/$', epidviews.dashboard.dashboard,
        name='epid_index'),

    # ANTIM : USERS
    url(r'^users/?$',
        provider_permission('can_manage_users')(bviews.providers.
                                                ProvidersListView.as_view()),
        name='list_users'),
    url(r'^users/add$', bviews.providers.add_edit_user, name='add_user'),
    url(r'^users/edit/(?P<user_id>[0-9]+)$',
        bviews.providers.add_edit_user, name='edit_user'),
    url(r'^users/disable/(?P<user_id>[0-9]+)$',
        bviews.providers.enable_disable_user, name='disable_user',
        kwargs={'activate': False}),
    url(r'^users/enable/(?P<user_id>[0-9]+)$',
        bviews.providers.enable_disable_user, name='enable_user',
        kwargs={'activate': True}),
    url(r'^users/new_password/(?P<user_id>[0-9]+)/(?P<pwd_id>[0-9]+)$',
        bviews.providers.password_user, name='password_user'),

    # ANTIM : ENTITIES
    url(r'^entities/?$',
        provider_permission('can_manage_entities')(bviews.entities.
                                                EntitiesListView.as_view()),
        name='list_entities'),
    url(r'^entities/add$', bviews.entities.add_edit_entity, name='add_entity'),
    url(r'^entities/edit/(?P<entity_id>[0-9]+)$',
        bviews.entities.add_edit_entity, name='edit_entity'),

    # static web pages

    url(r'^help/$', direct_to_template,
         {'template': 'help.html'}, name='help'),
    url(r'^about/$', direct_to_template,
         {'template': 'about.html'}, name='about'),

    url(r'^support/$', mviews.dashboard.contact, name='support'),
    url(r'^annuaire/$', bviews.addressbook.addressbook, name='addressbook'),
    url(r'^adressbook_send_sms/$', bviews.addressbook.adressbook_send_sms,
                                   name='sms'),

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

    # demo purposes
    url(r'^date/?$', mviews.dashboard.change_date, name='date'),
)
