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


class PourcentageStructuresRuptureStockCTADistrict(IndicatorTable):
    """ Tableau: Pourcentage de structures avec Rupture de stock de CTA dans

        le district """

    name = _(u"Tableau 7")
    title = _(u" ")
    caption = _(u"Pourcentage de structures avec Rupture de stock de " \
                u"CTA dans le district")
    type = 'table'

    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    @label(u"Nombre total de structures dans le district")
    def total_structures_in_the_district(self, period):
        return self.entity.children.count()

    @indicator(1, 'total_structures_in_the_district')
    @label(u"Structures avec rupture de stock en CTA Nourrisson - Enfant")
    def stockout_act_children(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,
               stockout_act_children=MalariaReport.YES).count()

    @indicator(2, 'total_structures_in_the_district')
    @label(u"Structures avec rupture de stock en CTA Adolescent")
    def stockout_act_youth(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,
               stockout_act_youth=MalariaReport.YES).count()

    @indicator(3, 'total_structures_in_the_district')
    @label(u"Structures avec rupture de stock en CTA Adulte")
    def stockout_act_adult(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,
               stockout_act_adult=MalariaReport.YES).count()


class EvolutionPourcentageStructuresRuptureStockCTA(IndicatorTable):
    """ Graphe: Evolution du pourcentage de Structures avec rupture de stock en

        CTA """

    name = _(u"Figure 7")
    title = _(u" ")
    caption = _(u"Evolution du pourcentage de Structures avec rupture" \
                u" de stock en CTA")
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
    @label(u"CTA Nourrisson - Enfant")
    def stockout_act_children(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,
               stockout_act_children=MalariaReport.YES).count()

    @indicator(2, 'total_structures_in_the_district')
    @label(u"CTA Adolescent")
    def stockout_act_youth(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,
               stockout_act_youth=MalariaReport.YES).count()

    @indicator(3, 'total_structures_in_the_district')
    @label(u"CTA Adulte")
    def stockout_act_adult(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,
               stockout_act_adult=MalariaReport.YES).count()

WIDGETS = [PourcentageStructuresRuptureStockCTADistrict,
           EvolutionPourcentageStructuresRuptureStockCTA]
