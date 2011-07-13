#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana_reporting.models import Entity
from bolibana_reporting.indicators import (IndicatorTable, NoSourceData, \
                                           reference, indicator, label, blank)
from pnlp_core.models import MalariaReport
from pnlp_core.data import current_reporting_period
from pnlp_core.indicators.common import get_report_for
from pnlp_core.indicators.section2 import NbreCasSuspectesTestesConfirmes


class CasPaludismeEnfantsMoins5ans(IndicatorTable):
    """ Tableau: Nombre de cas de paludisme chez les enfants de moins de

        5 ans """

    name = u"Tableau 2.1b"
    title = u"Enfants moins de 5 ans"
    caption = u"Nombre de cas de paludisme chez les enfants de moins de 5 ans"
    type = 'table'

    default_options = {'with_percentage': True, \
                       'with_total': True, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    @label(u"Total des cas suspects")
    def u5_total_suspected_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_suspected_malaria_cases

    @indicator(1, 'u5_total_suspected_malaria_cases')
    @label(u". Cas simples")
    def u5_total_simple_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_simple_malaria_cases

    @label(u". Cas graves")
    @indicator(2, 'u5_total_suspected_malaria_cases')
    def u5_total_severe_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_severe_malaria_cases

    def blank(self):
        pass
    blank._is_blank = True
    blank._index = 3
    blank._is_indicator = True

    @reference
    @indicator(4, 'u5_total_tested_malaria_cases')
    @label(u"Total des cas suspects testés (GE et/ou TDR)")
    def u5_total_tested_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_tested_malaria_cases

    @indicator(5, 'u5_total_tested_malaria_cases')
    @label(u"Nombre de cas suspects testés qui sont confirmés par  GE ou TDR")
    def u5_total_confirmed_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_confirmed_malaria_cases


class NbreTestesConfirmesUnderFive(NbreCasSuspectesTestesConfirmes):
    """ Evolution de la proportion de cas testés parmi les cas suspects et

        proportion de cas confirmés parmi les cas testés  chez les enfants de
        moins de 5 ans """

    name = u"Figure 2.2a"
    caption = u"Evolution de la proportion de cas testés parmi les " \
              u"cas suspects et proportion de cas confirmés parmi les" \
              u" cas testés  chez les enfants de moins de 5 ans"
    graph_type = 'line'
    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': True, \
                       'age': 'under_five'}

WIDGETS = [CasPaludismeEnfantsMoins5ans, NbreTestesConfirmesUnderFive]
