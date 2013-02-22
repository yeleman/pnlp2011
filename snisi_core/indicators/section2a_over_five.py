#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.reporting.indicators import (IndicatorTable,
                                           reference, indicator, label)
from snisi_core.models.MalariaReport import MalariaR
from snisi_core.indicators.common import get_report_for
from snisi_core.indicators.section2 import (NbreCasSuspectesTestesConfirmes,
                                            CasSimplesGraves,
                                            CasTestes, CasConfirmes)


class CasPaludismeEnfantsOverFive(IndicatorTable):
    """ Tableau: Nombre de cas de paludisme chez les personnes de 5 ans et

        plus """

    name = u"Tableau 5"
    title = u"Personnes de 5 ans et plus"
    caption = u"Nombre de cas de paludisme chez les personnes de 5 ans et plus"
    type = 'table'

    default_options = {'with_percentage': True,
                       'with_total': True,
                       'with_reference': True}

    def period_is_valid(self, period):
        return MalariaR.validated.filter(entity=self.entity,
                                              period=period).count() > 0

    @reference
    @indicator(0, 'o5_total_suspected_malaria_cases')
    @label(u"Total des cas suspects")
    def o5_total_suspected_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_suspected_malaria_cases

    @indicator(1, 'o5_total_suspected_malaria_cases')
    @label(u"Total des cas suspects testés (GE et/ou TDR)")
    def o5_total_tested_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_tested_malaria_cases

    @indicator(2, 'o5_total_tested_malaria_cases')
    @label(u"Nombre de cas suspects testés qui sont confirmés par  " \
           u"GE ou TDR")
    def o5_total_confirmed_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_confirmed_malaria_cases

    @indicator(3, 'o5_total_confirmed_malaria_cases')
    @label(u". Cas simples")
    def o5_total_simple_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_simple_malaria_cases

    @label(u". Cas graves")
    @indicator(4, 'o5_total_confirmed_malaria_cases')
    def u5_total_severe_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_severe_malaria_cases


class NbreTestesConfirmesOverFive(NbreCasSuspectesTestesConfirmes):
    """ Graphe: Evolution de la proportion des cas testés parmi les cas

       et proportion des cas confirmés parmi les cas testés  chez
       les de 5 ans et plus """

    name = u"Figure 10"
    caption = u"Nombre de cas de paludisme  par mois (cas suspects, " \
              u"cas testés,  cas confirmés)  chez les personnes de" \
              u" 5 ans et plus."

    default_options = {'with_percentage': False,
                       'with_total': False,
                       'with_reference': True,
                       'with_data': True,
                       'only_percent': False,
                       'age': 'over_five'}


class NbreTestesOverrFive(CasTestes):
    """ Graphe: Evolution de la proportion des cas testés parmi les cas

       et proportion des cas confirmés parmi les cas testés  chez les
       de 5 ans et plus """

    name = u"Figure 11"
    caption = u"Evolution de la proportion des cas testés parmi les " \
              u"cas suspects chez les personnes de 5 ans et plus"
    graph_type = 'spline'

    default_options = {'with_percentage': True,
                       'with_total': False,
                       'with_reference': False,
                       'with_data': True,
                       'only_percent': True,
                       'age': 'over_five'}


class NbreConfirmesOverrFive(CasConfirmes):
    """ Graphe: Evolution de la proportion des cas confirmés parmi

        les cas testés  chez les personnes de 5 ans et plus """

    name = u"Figure 12"
    caption = u"Evolution de la proportion des cas confirmés parmi" \
              u"les cas testés  chez les personnes de 5 ans et plus"
    graph_type = 'spline'

    default_options = {'with_percentage': True,
                       'with_total': False,
                       'with_reference': False,
                       'with_data': True,
                       'only_percent': True,
                       'age': 'over_five'}


class NbreCasSimplesGravesOverFive(CasSimplesGraves):
    """ Graphe: Evolution de la proportion des cas testés parmi les cas

       et proportion des cas confirmés parmi les cas testés  chez les
       de 5 ans et plus """

    name = u"Figure 13"
    caption = u"Evolution de la proportion des cas testés parmi" \
              u" les cas suspects et proportion des cas confirmés" \
              u" parmi les cas testés  chez les personnes de 5 ans" \
              u" et plus"
    graph_type = 'spline'

    default_options = {'with_percentage': False,
                       'with_total': False,
                       'with_reference': False,
                       'with_data': True,
                       'only_percent': False,
                       'age': 'over_five'}


WIDGETS = [CasPaludismeEnfantsOverFive, NbreTestesConfirmesOverFive,
           NbreTestesOverrFive, NbreConfirmesOverrFive,
           NbreCasSimplesGravesOverFive]
