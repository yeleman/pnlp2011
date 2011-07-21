#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana_reporting.models import Entity
from bolibana_reporting.indicators import (IndicatorTable, NoSourceData, \
                                           reference, indicator, label, blank)
from pnlp_core.models import MalariaReport
from pnlp_core.data import current_reporting_period
from pnlp_core.indicators.common import get_report_for
from pnlp_core.indicators.section2 import (NbreCasSuspectesTestesConfirmes, \
                                CasSimplesGraves, CasTestes, CasConfirmes)


class CasPaludismeEnfantsMoins5ans(IndicatorTable):
    """ Tableau: Nombre de cas de paludisme chez les enfants de moins de

        5 ans """

    name = u"Tableau 4"
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
    @label(u"Nombre de cas de paludisme (tous suspectés)  ")
    def u5_total_suspected_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_suspected_malaria_cases

    @indicator(1, 'u5_total_tested_malaria_cases')
    @label(u"Total des cas suspects testés (GE et/ou TDR)")
    def u5_total_tested_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_tested_malaria_cases

    @indicator(2, 'u5_total_tested_malaria_cases')
    @label(u"Nombre de cas suspects testés qui sont confirmés par  GE" \
           u"ou TDR")
    def u5_total_confirmed_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_confirmed_malaria_cases

    @indicator(3, 'u5_total_confirmed_malaria_cases')
    @label(u". Cas simples")
    def u5_total_simple_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_simple_malaria_cases

    @label(u". Cas graves")
    @indicator(4, 'u5_total_confirmed_malaria_cases')
    def u5_total_severe_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_severe_malaria_cases


class NbreTestesConfirmesUnderFive(NbreCasSuspectesTestesConfirmes):
    """ Nombre de cas de paludisme  par mois (cas suspects, cas testés,

        cas confirmés)  chez les moins de 5 ans. """

    name = u"Figure 6"
    caption = u"Nombre de cas de paludisme  par mois (cas suspects," \
              u"cas testés,  cas confirmés)  chez les moins de 5 ans."
    default_options = {'with_percentage': False, \
                       'with_total': False, \
                       'with_reference': True, \
                       'with_data': True,
                       'only_percent': False, \
                       'age': 'under_five'}


class NbreTestesUnderFive(CasTestes):
    """ Evolution de la proportion des cas testés parmi les cas suspects

        chez les moins de 5 ans """

    name = u"Figure 7"
    caption = u"Evolution de la proportion des cas testés parmi les cas " \
              u"suspects chez les moins de 5 ans"
    graph_type = 'line'
    type = "graph"
    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': True, \
                       'age': 'under_five'}


class NbreConfirmesUnderFive(CasConfirmes):
    """ Evolution de la proportion des cas confirmés parmi les cas testés

        chez les moins de 5 ans """

    name = u"Figure 8"
    caption = u" Evolution de la proportion des cas confirmés parmi les " \
              u"cas testés  chez les moins de 5 ans"
    graph_type = 'line'
    type = "graph"
    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': True, \
                       'age': 'under_five'}


class NbreCasSimplesGravesUnderFive(CasSimplesGraves):
    """ Evolution de la proportion des cas confirmés parmi les cas testés

        chez les moins de 5 ans """

    name = u"Figure 9"
    caption = u"Proportion de cas simples et cas graves chez les moins " \
              u"de 5 ans "
    graph_type = 'line'
    type = "graph"
    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': True, \
                       'age': 'under_five'}

WIDGETS = [CasPaludismeEnfantsMoins5ans, NbreTestesConfirmesUnderFive,
           NbreTestesUnderFive, NbreConfirmesUnderFive]
