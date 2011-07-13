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


class CasPaludismeEnfantsOverFive(IndicatorTable):
    """ Tableau: Nombre de cas de paludisme chez les personnes de 5 ans et

        plus """

    name = u"Tableau 2.3"
    title = u"Personnes de 5 ans et plus"
    caption = u"Nombre de cas de paludisme chez les personnes de 5 ans et plus"
    type = 'table'

    default_options = {'with_percentage': True, \
                       'with_total': True, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0, 'total_suspected_malaria_cases')
    @label(u"Total des cas suspects")
    def total_suspected_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_suspected_malaria_cases

    @indicator(1, 'total_suspected_malaria_cases')
    @label(u". Cas simples")
    def o5_total_simple_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_simple_malaria_cases

    @label(u". Cas graves")
    @indicator(2, 'total_suspected_malaria_cases')
    def u5_total_severe_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_severe_malaria_cases

    def blank(self):
        pass
    blank._is_blank = True
    blank._index = 3
    blank._is_indicator = True

    @reference
    @indicator(4, 'total_tested_malaria_cases')
    @label(u"Total des cas suspects testés (GE et/ou TDR)")
    def total_tested_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_tested_malaria_cases

    @indicator(5, 'total_tested_malaria_cases')
    @label(u"Nombre de cas suspects testés qui sont confirmés par  GE ou TDR")
    def u5_total_confirmed_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_confirmed_malaria_cases


class NbreCasSuspectesTestesConfirmesOverFive(NbreCasSuspectesTestesConfirmes):
    """ Graphe: Nombre de cas de paludisme (cas suspects, cas testés,

        cas confirmés) chez les personnes de 5 ans et plus """

    name = u"Figure 2.3"
    caption = u"Nombre de cas de paludisme (cas suspects, cas testés, " \
              u"cas confirmés) chez les personnes de 5 ans et plus."

    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': True, \
                       'with_data': True,
                       'only_percent': False, \
                       'age': 'over_five'}


class EvolutionTestesConfirmesOverFive(NbreCasSuspectesTestesConfirmes):
    """ Graphe: Evolution de la proportion des cas testés parmi les cas

       et proportion des cas confirmés parmi les cas testés  chez les de 5 ans
       et plus """

    name = u"Figure 2.4"
    caption = u"Evolution de la proportion des cas testés parmi" \
              u" les cas suspects et proportion des cas confirmés" \
              u" parmi les cas testés  chez les personnes de 5 ans et plus"

    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': True, \
                       'age': 'over_five'}


WIDGETS = [CasPaludismeEnfantsOverFive,
           NbreCasSuspectesTestesConfirmesOverFive,
           EvolutionTestesConfirmesOverFive]
