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


class PourcentageStructuresRuptureStockMILDTDRSP(IndicatorTable):
    """ Tableau: Pourcentage de structures sans rupture de stock en MILD, TDR,

        SP """

    name = u"Tableau 19"
    title = u" "
    caption = u"Pourcentage de structures sans rupture de stock en" \
                u"MILD, TDR, SP"
    type = 'table'

    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return True

    @reference
    @indicator(0)
    @label(u"Nombre total de structures dans le district")
    def total_structures_in_the_district(self, period):
        if self.entity.type.slug == 'cscom':
            return 1
        else:
            return self.entity.children.count()

    @indicator(1, 'total_structures_in_the_district')
    @label(u"Structures sans rupture de stock en CTA Nourrisson - Enfant")
    def stockout_bednet(self, period):
        report = get_report_for(self.entity, period)
        if report.type == MalariaReport.TYPE_SOURCE:
            return int(report.stockout_bednet == MalariaReport.NO)
        return report.sources.filter(stockout_bednet=MalariaReport.NO).count()

    @indicator(2, 'total_structures_in_the_district')
    @label(u"Structures sans rupture de stock en CTA Adolescent")
    def stockout_rdt(self, period):
        report = get_report_for(self.entity, period)
        if report.type == MalariaReport.TYPE_SOURCE:
            return int(report.stockout_bednet == MalariaReport.NO)
        return report.sources.filter(stockout_bednet=MalariaReport.NO).count()
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,
               stockout_rdt=MalariaReport.NO).count()

    @indicator(3, 'total_structures_in_the_district')
    @label(u"Structures sans rupture de stock en CTA Adulte")
    def stockout_sp(self, period):
        report = get_report_for(self.entity, period)
        if report.type == MalariaReport.TYPE_SOURCE:
            return int(report.stockout_bednet == MalariaReport.NO)
        return report.sources.filter(stockout_bednet=MalariaReport.NO).count()
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,
               stockout_sp=MalariaReport.NO).count()


class EvolutionPourcentageStructuresRuptureStockMILDTDRSP(IndicatorTable):
    """ Graphe: Evolution du pourcentage de Structures sans rupture de stock en

        MILD, TDR, SP """

    name = u"Figure 29"
    title = u" "
    caption = u"Evolution du pourcentage de Structures sans rupture de stock" \
              u" en MILD, TDR, SP"
    type = 'graph'
    graph_type = 'line'

    default_options = {'with_percentage': True, \
                       'with_reference': False, \
                       'with_data': False,
                       'only_percent': True}

    def period_is_valid(self, period):
        return True

    @reference
    @indicator(0)
    def total_structures_in_the_district(self, period):
        if self.entity.type.slug == 'cscom':
            return 1
        else:
            return self.entity.children.count()

    @indicator(1, 'total_structures_in_the_district')
    @label(u"MILD")
    def stockout_bednet(self, period):
        report = get_report_for(self.entity, period)
        if report.type == MalariaReport.TYPE_SOURCE:
            return int(report.stockout_bednet == MalariaReport.NO)
        return report.sources.filter(stockout_bednet=MalariaReport.NO).count()

    @indicator(2, 'total_structures_in_the_district')
    @label(u"TDR")
    def stockout_rdt(self, period):
        report = get_report_for(self.entity, period)
        if report.type == MalariaReport.TYPE_SOURCE:
            return int(report.stockout_rdt == MalariaReport.NO)
        return report.sources.filter(stockout_rdt=MalariaReport.NO).count()

    @indicator(3, 'total_structures_in_the_district')
    @label(u"Serum Glucosé 10%")
    def stockout_sp(self, period):
        report = get_report_for(self.entity, period)
        if report.type == MalariaReport.TYPE_SOURCE:
            return int(report.stockout_sp == MalariaReport.NO)
        return report.sources.filter(stockout_sp=MalariaReport.NO).count()

WIDGETS = [PourcentageStructuresRuptureStockMILDTDRSP,
           EvolutionPourcentageStructuresRuptureStockMILDTDRSP]
