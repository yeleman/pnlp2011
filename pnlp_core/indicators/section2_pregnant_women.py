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


class CasPaludismeFemmesEnceintes(IndicatorTable):
    """ Nombre de cas de paludisme chez les femmes enceintes """
    name = u"Tableau 2.1d"
    title = u"Femmes enceintes"
    caption = u"Nombre de cas de paludisme chez les femmes enceintes"
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

    @label(u". Cas graves")
    @indicator(1, 'total_suspected_malaria_cases')
    def pw_total_severe_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_severe_malaria_cases

    def blank(self):
        pass
    blank._is_blank = True
    blank._index = 2
    blank._is_indicator = True

    @reference
    @indicator(3, 'total_tested_malaria_cases')
    @label(u"Total des cas suspects testés (GE et/ou TDR)")
    def total_tested_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_tested_malaria_cases

    @indicator(4, 'total_tested_malaria_cases')
    @label(u"Nombre de cas suspects testés qui sont confirmés par  GE ou TDR")
    def pw_total_confirmed_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_confirmed_malaria_cases


class EvolutionTestesConfirmesFemmesEnceintes(NbreCasSuspectesTestesConfirmes):
    """ Evolution de la proportion des cas testés parmi les cas

        suspects et proportion des cas confirmés parmi les cas
        testés  chez les femmes enceintes """

    name = u"Figure 2.2d"
    caption = u"Evolution de la proportion des cas testés parmi les cas" \
              u" suspects et proportion des cas confirmés parmi les cas" \
              u" testés  chez les femmes enceintes "

    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': True, \
                       'age': 'pregnant_women'}
WIDGETS = [CasPaludismeFemmesEnceintes, EvolutionTestesConfirmesFemmesEnceintes]
