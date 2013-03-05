#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from bolibana.models.Period import MonthPeriod, WeekPeriod, DayPeriod

from snisi_core.models.MalariaReport import MalariaR, AggMalariaR
from snisi_core.data.malaria import MalariaRForm, AggMalariaRForm
from snisi_core.models.BednetReport import BednetR
from snisi_core.data.bednet import BednetRForm, AggBednetRForm
from snisi_core.models.CommoditiesReport import RHProductsR, AggRHProductsR
from snisi_core.models.MaternalMortalityReport import (MaternalDeathR,
                                                       AggMaternalDeathR)
from snisi_core.models.ChildrenMortalityReport import (ChildrenDeathR,
                                                       AggChildrenDeathR)
from snisi_core.data.reproduction import (RHProductsRForm, AggRHProductsRForm,
                                          ChildrenDeathRForm,
                                          AggChildrenDeathRForm,
                                          MaternalDeathRForm,
                                          AggMaternalDeathRForm)
from snisi_core.models.Epidemiology import EpidemiologyR
from snisi_core.data.epidemiology import AggEpidemiologyRForm, EpidemiologyRForm
from snisi_core.data import current_reporting_period

INDIVIDUAL = 'individual'
COMPILED = 'compiled'

MALARIA_PROJECT = {'category': 'malaria',
                   'slug': 'malaria',
                   'src_cls': MalariaR,
                   'agg_cls': AggMalariaR,
                   'src_form': MalariaRForm,
                   'agg_form': AggMalariaRForm,
                   'period_cls': MonthPeriod,
                   'get_reporting_period': current_reporting_period,
                   'type': COMPILED}

BEDNET_PROJECT = {'category': 'bednet',
                  'slug': 'bednet',
                  'src_cls': BednetR,
                  'agg_cls': BednetR,
                  'src_form': BednetRForm,
                  'agg_form': AggBednetRForm,
                  'period_cls': WeekPeriod,
                  'get_reporting_period':
                       lambda: WeekPeriod.current().previous(),
                       'type': COMPILED}

RH_COMMODITIES_PROJECT = {'category': 'reproduction',
                          'slug': 'reproduction_commodities',
                          'src_cls': RHProductsR,
                          'agg_cls': AggRHProductsR,
                          'src_form': RHProductsRForm,
                          'agg_form': AggRHProductsRForm,
                          'period_cls': MonthPeriod,
                          'get_reporting_period': current_reporting_period,
                          'type': COMPILED}

RH_MATERNAL_PROJECT = {'category': 'reproduction',
                          'slug': 'reproduction_maternal',
                          'src_cls': MaternalDeathR,
                          'agg_cls': AggMaternalDeathR,
                          'src_form': MaternalDeathRForm,
                          'agg_form': AggMaternalDeathRForm,
                          'period_cls': DayPeriod,
                          'get_reporting_period': lambda: DayPeriod.current(),
                          'type': INDIVIDUAL}

RH_CHILDREN_PROJECT = {'category': 'reproduction',
                          'slug': 'reproduction_children',
                          'src_cls': ChildrenDeathR,
                          'agg_cls': AggChildrenDeathR,
                          'src_form': ChildrenDeathRForm,
                          'agg_form': AggChildrenDeathRForm,
                          'period_cls': DayPeriod,
                          'get_reporting_period': lambda: DayPeriod.current(),
                          'type': INDIVIDUAL}

REPRODUCTION_PROJECT = {'category': 'reproduction',
                        'slug': 'reproduction_children'}

SNISI_PROJECT = {'category': 'snisi',
                 'slug': 'snisi',
                 'get_reporting_period': current_reporting_period}

EPIDEMIOLOGY_PROJECT = {'category': 'epidemiology',
                        'slug': 'epidemiology',
                        'src_cls': EpidemiologyR,
                        'agg_cls': EpidemiologyR,
                        'src_form': EpidemiologyRForm,
                        'agg_form': AggEpidemiologyRForm,
                        'period_cls': WeekPeriod,
                        'get_reporting_period':
                            lambda: WeekPeriod.current().previous(),
                            'type': COMPILED}

PROJECTS = {
    'malaria': MALARIA_PROJECT,
    'epidemiology': EPIDEMIOLOGY_PROJECT,
    'bednet': BEDNET_PROJECT,
    'reproduction_commodities': RH_COMMODITIES_PROJECT,
    'reproduction_maternal': RH_MATERNAL_PROJECT,
    'reproduction_children': RH_CHILDREN_PROJECT,
    'reproduction': REPRODUCTION_PROJECT,
    'snisi': SNISI_PROJECT}
