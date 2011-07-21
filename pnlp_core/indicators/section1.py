#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.utils.translation import ugettext as _

from bolibana_reporting.models import Entity
from bolibana_reporting.indicators import (IndicatorTable, NoSourceData, \
                                           reference, indicator, label, blank)
from pnlp_core.models import MalariaReport
from pnlp_core.data import current_reporting_period, contact_for
from pnlp_core.indicators.common import get_report_for


class Tableau1(IndicatorTable):
    name = u"Tableau 1"
    title = u" "
    caption = u"Pourcentage de structures ayant transmis leurs" \
              u" formulaires de collecte dans les délais prévus"
    type = 'table'

    default_options = {'with_percentage': False, \
                       'with_total': False, \
                       'with_reference': False}

    def period_is_valid(self, period):
        return True

    @indicator(0)
    @label(u"Nombre total de structures dans le district")
    def total_structures_in_the_district(self, period):
        if self.entity.type.slug == 'cscom':
            return 1
        else:
            return self.entity.children.count()

    @indicator(1)
    @label(u"Nombre de structures ayant transmis leurs formulaires " \
           u"de collecte dans les délais prévus")
    def number_tautovalide(self, period):
        return self.entity.reports.count()


    #~ @indicator(2, 'total_structures_in_the_district')
    #~ @label(u"SMS")
    #~ def number_sms(self, period):
        #~ children = self.entity.get_children()
        #~ sms = 0
        #~ for source in self.entity.sources.all():
            #~ if source.created_by.first_role() == 'cscom':
                #~ sms += 1
        #~ return report.sources.filter(created_by)

class Figure1(IndicatorTable):
    name = u"Figure 1"
    title = u""
    caption = u"Evolution de la promptitude de la notification dans " \
              u"le district"
    type = 'graph'

    default_options = {'with_percentage': False, \
                   'with_total': False, \
                   'with_reference': False, \
                   'with_data': True,
                   'only_percent': False}


class Tableau2(IndicatorTable):
    name = u"Tableau 2"
    title = u" "
    caption = u"Pourcentage de structures ayant transmis leurs " \
              u"formulaires de collecte"
    type = 'table'

    default_options = {'with_percentage': False, \
                       'with_total': False, \
                       'with_reference': False}

    def period_is_valid(self, period):
        return True

    @indicator(0)
    @label(u"Nombre total de structures dans le district (nombre de" \
           u" formulaires de collecte attendu)")
    def total_structures_in_the_district(self, period):
        if self.entity.type.slug == 'cscom':
            return 1
        else:
            return self.entity.children.count()

    @indicator(1)
    @label(u"Nombre de structures ayant transmis leurs formulaires " \
           u"de collecte")
    def number_tautovalide(self, period):
        return self.entity.reports.count()


class Figure2(IndicatorTable):
    name = u"Figure 2"
    title = u""
    caption = u"Evolution de la complétude de la notification dans " \
              u"le district"
    type = 'graph'

    default_options = {'with_percentage': False, \
                   'with_total': False, \
                   'with_reference': False, \
                   'with_data': True,
                   'only_percent': False}


WIDGETS = [Tableau1, Figure1, Tableau2, Figure2]
