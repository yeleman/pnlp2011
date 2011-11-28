#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.utils.translation import ugettext as _

from bolibana.models import Entity
from bolibana.reporting.indicators import (IndicatorTable, NoSourceData, \
                                           reference, indicator, label)
from pnlp_core.models import MalariaReport
from pnlp_core.data import current_reporting_period
from pnlp_core.indicators.common import get_report_for


class DonneesCPNetTPI(IndicatorTable):
    """ Tableau: Données sur la CPN et le Traitement Préventif  Intermittent

        (TPI) """

    name = u"Tableau 20"
    title = u" "
    caption = u"Données sur la CPN et le Traitement Préventif" \
                u" Intermittent(TPI)"
    type = 'table'

    default_options = {'with_percentage': False, \
                       'with_total': False, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    @label(u"Nombre de femmes enceintes reçues en CPN  1")
    def pw_total_anc1(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_anc1

    @indicator(1)
    @label(u"Nombre de femmes enceintes ayant reçu la SP1")
    def pw_total_sp1(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_sp1

    @indicator(2)
    @label(u"Nombre de femmes enceintes ayant reçu la SP2")
    def pw_total_sp2(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_sp2


class EvolutionCPN1SP1SP2(IndicatorTable):
    """ Graphe: Evolution de la  CPN1, SP1 et SP2 chez les femmes enceintes"""

    name = u"Figure 30"
    title = u" "
    caption = u"Evolution de la SP1 et SP2 chez les femmes enceintes"
    type = 'graph'
    graph_type = 'line'

    default_options = {'with_percentage': False, \
                       'with_reference': False, \
                       'with_data': False,
                       'only_percent': False}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    @label(u"Nombre de femmes enceintes reçues en CPN 1")
    def pw_total_anc1(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_anc1

    @indicator(1)
    @label(u"Nombre de femmes enceintes ayant reçu la SP1")
    def pw_total_sp1(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_sp1

    @indicator(2)
    @label(u"Nombre de femmes enceintes ayant reçu la SP2")
    def pw_total_sp2(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_sp2


class NombreFemmesEnceintesCPN1NombreMILDFemmesEnceintes(IndicatorTable):
    """ Graphe: Nombre de femmes enceintes reçues en CPN1 et Nombre de

        MILD distribuées aux femmes enceintes"""

    name = u"Figure 31"
    title = u" "
    caption = u"Nombre de femmes enceintes reçues en CPN1 et Nombre " \
                u"de MILD distribuées aux femmes enceintes"
    type = 'graph'

    default_options = {'with_percentage': False, \
                       'with_reference': False, \
                       'with_data': False,
                       'only_percent': False}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @indicator(0)
    @label(u"Nbre de femmes enceintes reçues en CPN 1")
    def pw_total_anc1(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_anc1

    @indicator(1)
    @label(u"Nbre MILD distribuees aux femmes enceintes")
    def pw_total_distributed_bednets(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_distributed_bednets

WIDGETS = [DonneesCPNetTPI, EvolutionCPN1SP1SP2,
           NombreFemmesEnceintesCPN1NombreMILDFemmesEnceintes]
