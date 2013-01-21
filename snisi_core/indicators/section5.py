#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin


from bolibana.reporting.indicators import IndicatorTable, indicator, label
from snisi_core.models.MalariaReport import MalariaR
from snisi_core.indicators.common import get_report_for


class NombreMoustiquqiresImpregneesInsecticidesLongueDureeMILD(IndicatorTable):
    """ Tableau: Nombre de Moustiquaires imprégnées  d’Insecticides

       de Longue Durée (MILD) distribuées"""

    name = u"Tableau 16"
    title = u" "
    caption = (u"Nombre de Moustiquaires imprégnées  d’Insecticides de"
               u" Longue Durée (MILD) distribuées")
    type = 'table'

    default_options = {'with_percentage': False,
                       'with_total': False,
                       'with_reference': False}

    def period_is_valid(self, period):
        """Periode valide"""
        return MalariaR.validated.filter(entity=self.entity,
                                         period=period).count() > 0

    @indicator(0)
    @label(u"Nombre MILD distribuées aux enfants de moins de 5 ans")
    def u5_total_distributed_bednets(self, period):
        """Total des moustiquaires distribues aux moin de 5 ans"""
        report = get_report_for(self.entity, period)
        return report.u5_total_distributed_bednets

    @indicator(1)
    @label(u"Nombre de MILD distribuées aux femmes enceintes")
    def pw_total_distributed_bednets(self, period):
        """Total des moustiquaires distribues aux femmes enceintes"""
        report = get_report_for(self.entity, period)
        return report.pw_total_distributed_bednets


class EvolutionNbreMILDMoins5ansFemmesenceintes(IndicatorTable):
    """Graphe: Evolution du nombre de MILD distribuées aux moins

       de 5 ans et femmes enceintes"""

    name = u"Figure 26"
    title = u" "
    caption = (u"Evolution du nombre de MILD distribuées aux moins de "
               u"5 ans et femmes enceintes")
    type = 'graph'
    graph_type = 'spline'

    default_options = {'with_percentage': False,
                       'with_reference': True,
                       'with_data': True,
                       'only_percent': False}

    def period_is_valid(self, period):
        """Periode valide"""
        return MalariaR.validated.filter(entity=self.entity,
                                         period=period).count() > 0

    @indicator(0)
    @label(u"Nbre de MILD distribuées aux moins de 5 ans")
    def u5_total_distributed_bednets(self, period):
        """Total des moustiquaires distribues aux moin de 5 ans"""
        report = get_report_for(self.entity, period)
        return report.u5_total_distributed_bednets

    @indicator(1)
    @label(u"Nbre de MILD distribuées aux femmes enceintes")
    def pw_total_distributed_bednets(self, period):
        """Total des moustiquaires distribues aux femmes enceintes"""
        report = get_report_for(self.entity, period)
        return report.pw_total_distributed_bednets

WIDGETS = [NombreMoustiquqiresImpregneesInsecticidesLongueDureeMILD, \
           EvolutionNbreMILDMoins5ansFemmesenceintes]
