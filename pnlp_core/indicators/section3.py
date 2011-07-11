#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.utils.translation import ugettext as _

from bolibana_reporting.models import Entity
from bolibana_reporting.indicators import (IndicatorTable, \
                                           NoSourceData, \
                                           reference, indicator, label)
from pnlp_core.models import MalariaReport
from pnlp_core.data import current_reporting_period
from pnlp_core.indicators.common import get_report_for


class CasPaludismeSimpleTraitesCTA(IndicatorTable):

    name = _(u"Tableau 3.1")
    title = _(u" ")
    caption = _(u"Cas de paludisme simple traités par CTA")
    type = 'table'

    default_options = {'with_percentage': True, \
                       'with_total': True, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    @label(u"Nombre de cas simple chez les moins de 5 ans")
    def u5_total_simple_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_simple_malaria_cases

    @indicator(1, 'u5_total_simple_malaria_cases')
    @label(u"Cas simple traités par CTA chez " \
           u"les moins de 5 ans")
    def u5_total_treated_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_treated_malaria_cases

    @reference
    @indicator(2)
    @label(u"Nombre de cas simple chez les 5 ans et plus")
    def o5_total_simple_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_simple_malaria_cases

    @indicator(3, 'o5_total_simple_malaria_cases')
    @label(u"Cas simple traités par CTA chez " \
           u"les 5 ans et plus")
    def o5_total_treated_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_treated_malaria_cases


class CasPaludismeConfirmesTraitesCTA(IndicatorTable):

    name = _(u"Figure 3.1")
    title = _(u" ")
    caption = _(u"Nombre de cas de paludisme confirmés et " \
                u"nombre de cas traités par CTA")
    type = 'graph'

    default_options = {'with_percentage': False, \
                       'with_reference': True, \
                       'with_data': True, \
                       'only_percent': False}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @indicator(0)
    @label(u"Nbre de cas confirmés")
    def total_confirmed_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_confirmed_malaria_cases

    @indicator(1)
    @label(u"Nbre de cas traités par CTA")
    def total_treated_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_treated_malaria_cases


class EvolutionProportionCasPaludismeSimpleTraitesU5O5(IndicatorTable):
    """ Évolution des proportions  de cas de paludisme simple
        traités par CTA Chez les moins de 5 ans et les 5 ans et plus"""

    name = _(u"Figure 3.2")
    title = _(u" ")
    caption = _(u"Évolution des proportions  de cas de paludisme " \
                u"simple traités par CTA Chez les moins de 5 ans" \
                 u"et les 5 ans et plus")
    type = 'graph'

    default_options = {'with_percentage': False, \
                       'with_reference': False, \
                       'with_data': True, \
                       'only_percent': False}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @indicator(0)
    @label(u"Nbre de cas traités par CTA chez les mois de 5 ans")
    def u5_total_treated_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_treated_malaria_cases

    @indicator(1)
    @label(u"Nbre de cas traités par CTA chez les plus de 5 ans")
    def o5_total_treated_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_treated_malaria_cases

WIDGETS = [CasPaludismeSimpleTraitesCTA, \
           CasPaludismeConfirmesTraitesCTA, \
           EvolutionProportionCasPaludismeSimpleTraitesU5O5]
