#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import os

from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

import snisi_web.views as views
from views import index as main_index
from views import monitoring as monitoring
from views import malaria as malaria
from views import epidemiology as epidemiology
from views import reproduction as reproduction
from bolibana.web import views as bolibana
from bolibana.web.decorators import provider_permission
from settings import STATIC_ROOT, MEDIA_ROOT

PROJECT = r'(?P<project_slug>[a-z\_]+)'
RGXP_ENTITY = r'(?P<entity_code>[a-zA-Z0-9\-\_]+)'
RGXP_RECEIPT = r'(?P<report_receipt>[a-zA-Z\#\-\_\.0-9\/]+)'
RGXP_PERIOD = r'(?P<period_str>[0-9]{6})'
RGXP_PERIODS = r'(?P<period_str>[0-9]{6}-[0-9]{6})'
RGXP_SECTION = r'section(?P<section_index>[0-9]{1,2}[ab]{0,1})'
RGXP_SUBSECTION = r'(?P<sub_section>[a-z\_]+)'

"""
FORMATS:

YEAR:       2013                                [0-9]{4}
MONTH:      01-2013                             [0-9]{2}-[0-9]{4}
QUARTER:    Q1-2013                             Q[1-3]-[0-9]{4}
WEEK:       W1-2013                             W[0-9]{1,2}-[0-9]{4}
DAY:        01-01-2013                          [0-9]{2}-[0-9]{2}-[0-9]{4}
"""
RGXP_PERIOD = r'(?P<period_str>[0-9]{4}|[0-9]{2}\-[0-9]{4}|Q[1-3]\-[0-9]{4}|W[0-9]{1,2}\-[0-9]{4}|[0-9]{2}\-[0-9]{2}\-[0-9]{4})/?$'

urlpatterns = patterns('',

    url(r'^/?$', main_index, name='index'),
    url(r'^profile/$', bolibana.profile.edit_profile, name='profile'),

    # login
    url(r'^login/$', 'django.contrib.auth.views.login',
         {'template_name': 'login_django.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
         {'template_name': 'logout_django.html'}, name='logout'),

    # SNISI
    url(r'^snisi/dashboard/?$', views.generic_dashboard,
        {'project_slug': 'snisi'}, name='snisi_dashboard'),

    # Malaria
    url(r'^malaria/dashboard/?$', malaria.dashboard.dashboard,
        name='malaria_dashboard'),
    url(r'^malaria/upload/?$', malaria.excel_upload.upload_form, name='upload'),

    # district, region
    url(r'^validation/$',
        malaria.validation.validation_list, name='validation'),
    url(r'^validation/do/' + RGXP_RECEIPT + '$',
        malaria.validation.report_do_validation, name='report_do_validation'),
    url(r'^validation/' + RGXP_RECEIPT + '$',
        malaria.validation.report_validation, name='report_validation'),

    # ALL
    # url(r'^raw_data/' + RGXP_ENTITY + '/' + RGXP_PERIOD + '$', malaria.raw_data.data_browser, name='raw_data'),
    # url(r'^raw_data/' + RGXP_ENTITY + '$', malaria.raw_data.data_browser, name='raw_data'),
    # url(r'^raw_data/$', malaria.raw_data.data_browser, name='raw_data'),
    # url(r'^raw_data/excel/' + RGXP_RECEIPT + '$', malaria.raw_data.excel_export, name='raw_data_excel'),

    url(r'^' + PROJECT + '/raw_data/' + RGXP_ENTITY + '/' + RGXP_PERIOD + '$', views.generic_raw_data.data_browser, name='raw_data'),
    url(r'^' + PROJECT + '/raw_data/' + RGXP_ENTITY + '$', views.generic_raw_data.data_browser, name='raw_data'),
    url(r'^' + PROJECT + '/raw_data/?$', views.generic_raw_data.data_browser, name='raw_data'),
    url(r'^' + PROJECT + '/raw_data/excel/' + RGXP_RECEIPT + '$', views.generic_raw_data.excel_export, name='raw_data_excel'),

    # Indicator Views
    url(r'^malaria/browse/' + RGXP_ENTITY + '/' + RGXP_PERIODS + '/'
         + RGXP_SECTION + '/' + RGXP_SUBSECTION + '$',
        malaria.indicators.indicator_browser, name='malaria_indicator_data'),
    url(r'^malaria/browse/' + RGXP_ENTITY + '/' + RGXP_PERIODS + '/'
         + RGXP_SECTION + '$',
        malaria.indicators.indicator_browser, name='malaria_indicator_data'),
    url(r'^malaria/browse/' + RGXP_ENTITY + '/' + RGXP_PERIODS + '$',
        malaria.indicators.indicator_browser, name='malaria_indicator_data'),
    url(r'^malaria/browse/' + RGXP_ENTITY + '$',
        malaria.indicators.indicator_browser, name='malaria_indicator_data'),
    url(r'^malaria/browse/$', malaria.indicators.indicator_browser,
        name='malaria_indicator_data'),

    # ANTIM : Transmission
    url(r'^monitoring/source_data/?$', monitoring.source_data,
        name='monitoring_source_data'),
    url(r'^monitoring/messages_log/?$', monitoring.messages_log,
        name='monitoring_messages_log'),
    url(r'^monitoring/validation/?$', monitoring.validation,
        name='monitoring_validation'),
    url(r'^monitoring/bulk_messaging/?$', monitoring.bulk_messaging,
        name='monitoring_messaging'),

    # Reproduction
    url(r'^reproduction/dashboard/?$', views.generic_dashboard,
        {'project_slug': 'reproduction'}, name='reproduction_dashboard'),

    # Epidemiology
    url(r'^epidemiology/dashboard/?$', views.generic_dashboard,
        {'project_slug': 'epidemiology'}, name='epidemiology_dashboard'),

    # Bednet
    url(r'^bednet/dashboard/?$', views.generic_dashboard,
        {'project_slug': 'bednet'}, name='bednet_dashboard'),

    # ANTIM : USERS
    url(r'^users/?$',
        provider_permission('can_manage_users')(bolibana.providers.
                                                ProvidersListView.as_view()),
        name='list_users'),
    url(r'^users/add$', bolibana.providers.add_edit_user, name='add_user'),
    url(r'^users/edit/(?P<user_id>[0-9]+)$',
        bolibana.providers.add_edit_user, name='edit_user'),
    url(r'^users/disable/(?P<user_id>[0-9]+)$',
        bolibana.providers.enable_disable_user, name='disable_user',
        kwargs={'activate': False}),
    url(r'^users/enable/(?P<user_id>[0-9]+)$',
        bolibana.providers.enable_disable_user, name='enable_user',
        kwargs={'activate': True}),
    url(r'^users/new_password/(?P<user_id>[0-9]+)/(?P<pwd_id>[0-9]+)$',
        bolibana.providers.password_user, name='password_user'),

    # ANTIM : ENTITIES
    url(r'^entities/?$',
        provider_permission('can_manage_entities')(bolibana.entities.
                                                EntitiesListView.as_view()),
        name='list_entities'),
    url(r'^entities/add$', bolibana.entities.add_edit_entity, name='add_entity'),
    url(r'^entities/edit/(?P<entity_id>[0-9]+)$',
        bolibana.entities.add_edit_entity, name='edit_entity'),

    # static web pages

    url(r'^help/$', direct_to_template,
         {'template': 'help.html'}, name='help'),
    url(r'^about/$', direct_to_template,
         {'template': 'about.html'}, name='about'),

    url(r'^support/$', views.contact, name='support'),
    url(r'^annuaire/$', bolibana.addressbook.addressbook, name='addressbook'),
    url(r'^adressbook_send_sms/$', bolibana.addressbook.adressbook_send_sms,
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
    url(r'^date/?$', malaria.dashboard.change_date, name='date'),
)
