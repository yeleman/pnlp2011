#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.reporting.indicators import (IndicatorTable,
                                           reference, indicator, label)
from snisi_core.models.MalariaReport import MalariaR
from snisi_core.indicators.common import get_report_for


class CasPaludismeSimpleTraitesCTA(IndicatorTable):
    """ Tableau: Cas de paludisme simple traités par CTA """

    name = u"Tableau 7"
    title = u" "
    caption = u"Cas de paludisme simple traités par CTA"
    type = 'table'

    default_options = {'with_percentage': True, \
                       'with_total': True, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return MalariaR.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0, 'u5_total_simple_malaria_cases')
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
    @indicator(2, 'o5_total_simple_malaria_cases')
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
    """ Graphe: Nombre de cas de paludisme confirmés et nombre de cas traités

        par CTA """

    name = u"Figure 17"
    title = u" "
    caption = u"Nombre de cas de paludisme confirmés et " \
                u"nombre de cas traités par CTA"
    type = 'graph'

    default_options = {'with_percentage': False, \
                       'with_reference': True, \
                       'with_data': True, \
                       'only_percent': False}

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
    """ Graphe: Évolution des proportions  de cas de paludisme simple

        traités par CTA Chez les moins de 5 ans et les 5 ans et plus """

    name = u"Figure 18"
    title = u" "
    caption = u"Évolution des proportions  de cas de paludisme " \
                u"simple traités par CTA Chez les moins de 5 ans" \
                 u"et les 5 ans et plus"
    type = 'graph'

    default_options = {'with_percentage': False, \
                       'with_reference': False, \
                       'with_data': True, \
                       'only_percent': False}

    @indicator(0)
    @label(u"Nbre de cas traités par CTA chez les moins de 5 ans")
    def u5_total_treated_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_treated_malaria_cases

    @indicator(1)
    @label(u"Nbre de cas traités par CTA chez les plus de 5 ans")
    def o5_total_treated_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_treated_malaria_cases


class EvolutionProportionCasPaludismeSimpleTraitesu5O51(IndicatorTable):
    """ Graphe: Évolution des proportions  de cas de paludisme simple

        traités par CTA Chez les moins de 5 ans et les 5 ans et plus """

    name = u"Figure 19"
    title = u" "
    caption = u"Évolution des proportions  de cas de paludisme " \
                u"simple traités par CTA Chez les moins de 5 ans" \
                 u"et les 5 ans et plus"
    type = 'graph'
    graph_type = 'spline'
    default_options = {'with_percentage': False, \
                       'with_reference': False, \
                       'with_data': True, \
                       'only_percent': False}

    @indicator(0)
    @label(u"Nbre de cas traités par CTA chez les moins de 5 ans")
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
           EvolutionProportionCasPaludismeSimpleTraitesU5O5,
           EvolutionProportionCasPaludismeSimpleTraitesu5O51]
