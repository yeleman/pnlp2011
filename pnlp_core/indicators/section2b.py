#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana_reporting.models import Entity
from bolibana_reporting.indicators import (IndicatorTable, NoSourceData, \
                                           reference, indicator, label, blank)
from pnlp_core.models import MalariaReport
from pnlp_core.data import current_reporting_period
from pnlp_core.indicators.common import get_report_for, find_report_attr_age


class CasPaludismeSimpleTraitesCTA(IndicatorTable):
    """ Tableau: Nombre de cas de paludisme chez les personnes de 5 ans et

        plus """

    name = u"Tableau 5"
    title = u"Personnes de 5 ans et plus"
    caption = u"Cas de paludisme simple traités par CTA"
    type = 'table'

    default_options = {'with_percentage': True, \
                       'with_total': True, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    @label(u"Nombre de cas de paludisme simple chez les moins de 5 ans")
    def u5_total_simple_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_simple_malaria_cases

    @indicator(1)
    @label(u"Cas de paludisme simple traités par CTA chez les " \
           u"enfants de moins de 5 ans")
    def u5_total_treated_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_treated_malaria_cases

    @reference
    @indicator(2)
    @label(u"Nombre de cas de paludisme simple chez les personnes " \
           u"de 5 ans et plus")
    def o5_total_simple_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_simple_malaria_cases

    @indicator(3, 'o5_total_simple_malaria_cases')
    @label(u"Cas de paludisme simple traités par CTA chez les " \
           u"personnes de 5 ans et plus ")
    def o5_total_treated_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_treated_malaria_cases


class NbreCasPaludismeConfirmesTraites(IndicatorTable):
    """ Tableau: Nombre de cas de paludisme chez les personnes de 5

        ans et plus """

    name = u"Figure 17"
    title = u" "
    caption = u"Nombre de cas de paludisme confirmés et nombre de" \
              u" cas traités par CTA"
    type = 'graph'

    default_options = {'with_percentage': False, \
                       'with_total': False, \
                       'with_reference': False}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                          period=period).count() > 0

    @indicator(0)
    @label(u"Nbre de Cas Comfirmés")
    def total_confirmed_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_confirmed_malaria_cases

    @indicator(1)
    @label(u"Nbre de Cas traites par CTA")
    def total_treated_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_treated_malaria_cases

WIDGETS = [CasPaludismeSimpleTraitesCTA,
          NbreCasPaludismeConfirmesTraites]
