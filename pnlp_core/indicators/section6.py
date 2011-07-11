#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.utils.translation import ugettext as _

from bolibana_reporting.models import Entity
from bolibana_reporting.indicators import (IndicatorTable, NoSourceData, \
                                           reference, indicator, label)
from pnlp_core.models import MalariaReport
from pnlp_core.data import current_reporting_period
from pnlp_core.indicators.common import get_report_for


class NombreMoustiquqiresImpregneesInsecticidesLongueDureeMILD(IndicatorTable):
    """Tableau: Nombre de Moustiquaires imprégnées  d’Insecticides
       de Longue Durée (MILD) distribuées"""

    # Information du tableau
    name = _(u"Tableau 5.1")
    title = _(u" ")
    caption = _(u"Nombre de Moustiquaires imprégnées  d’Insecticides de" \
                u" Longue Durée (MILD) distribuées")
    type = 'table'

    # Option du tableau
    default_options = {'with_percentage': True, \
                       'with_total': True, \
                       'with_reference': True}

    def period_is_valid(self, period):
        """Periode valide"""
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
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

    # Information du tableau
    name = _(u"Figure 5.1")
    title = _(u" ")
    caption = _(u"Evolution du nombre de MILD distribuées aux moins de " \
                u"5 ans et femmes enceintes")
    type = 'graph'

    default_options = {'with_percentage': False, \
                       'with_reference': True, \
                       'with_data': True}

    def period_is_valid(self, period):
        """Periode valide"""
        return MalariaReport.validated.filter(entity=self.entity, \
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
