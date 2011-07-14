#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.utils.translation import ugettext as _

from bolibana_reporting.models import Entity
from bolibana_reporting.indicators import (IndicatorTable, NoSourceData, \
                                           reference, indicator, label)
from pnlp_core.models import MalariaReport
from pnlp_core.data import current_reporting_period


class PourcentageStructuresRuptureStockMILDTDRSP(IndicatorTable):
    """ Tableau: Pourcentage de structures avec Rupture de stock en MILD, TDR,

        SP """

    name = _(u"Tableau 9")
    title = _(u" ")
    caption = _(u"Pourcentage de structures avec Rupture de stock en" \
                u"MILD, TDR, SP")
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
    @label(u"Structures avec rupture de stock en CTA Nourrisson - Enfant")
    def stockout_bednet(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,
               stockout_bednet=MalariaReport.YES).count()

    @indicator(2, 'total_structures_in_the_district')
    @label(u"Structures avec rupture de stock en CTA Adolescent")
    def stockout_rdt(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,
               stockout_rdt=MalariaReport.YES).count()

    @indicator(3, 'total_structures_in_the_district')
    @label(u"Structures avec rupture de stock en CTA Adulte")
    def stockout_sp(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,
               stockout_sp=MalariaReport.YES).count()


class EvolutionPourcentageStructuresRuptureStockMILDTDRSP(IndicatorTable):
    """ Graphe: Evolution du pourcentage de Structures avec rupture de stock en

        MILD, TDR, SP """

    name = _(u"Figure 9")
    title = _(u" ")
    caption = _(u"Evolution du pourcentage de Structures avec rupture " \
                u"de stock en MILD, TDR, SP")
    type = 'graph'
    graph_type = 'line'

    default_options = {'with_percentage': True, \
                       'with_reference': False, \
                       'with_data': False,
                       'only_percent': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    def total_structures_in_the_district(self, period):
        return self.entity.children.count()

    @indicator(1, 'total_structures_in_the_district')
    @label(u"MILD")
    def stockout_bednet(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,
               stockout_bednet=MalariaReport.YES).count()

    @indicator(2, 'total_structures_in_the_district')
    @label(u"TDR")
    def stockout_rdt(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,
               stockout_rdt=MalariaReport.YES).count()

    @indicator(3, 'total_structures_in_the_district')
    @label(u"Serum Glucosé 10%")
    def stockout_sp(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,
               stockout_sp=MalariaReport.YES).count()

WIDGETS = [PourcentageStructuresRuptureStockMILDTDRSP,
           EvolutionPourcentageStructuresRuptureStockMILDTDRSP]
