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


class PourcentageStructuresRuptureStockProduitPaluGrave(IndicatorTable):
    """ Tableau: Pourcentage de structures avec Rupture de stock en produits

    de prise en charge des cas de paludisme grave """

    name = _(u"Tableau 8")
    title = _(u" ")
    caption = _(u"Pourcentage de structures avec rupture de stock en" \
             "produits de prise en charge des cas de paludisme grave")
    type = 'table'

    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return True

    @reference
    @indicator(0)
    @label(u"Nombre total de structures dans le district")
    def nombre_total_structures_district(self, period):
        if self.entity.type.slug == 'cscom':
            return 1
        else:
            return self.entity.children.count()

    @indicator(1, "nombre_total_structures_district")
    @label(u"Structures avec rupture de stock d’Artheméter Injectable")
    def structures_rupture_stock_arthemeter_injectable(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,\
                    stockout_artemether=MalariaReport.YES).count()

    @indicator(2, "nombre_total_structures_district")
    @label(u"Structures avec rupture de stock de Quinine Injectable")
    def structures_rupture_stock_Quinine_injectable(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,\
                    stockout_quinine=MalariaReport.YES).count()

    @indicator(3, "nombre_total_structures_district")
    @label(u"Structures avec rupture de stock en Sérum Glucosé 10%")
    def structures_rupture_stock_Serum_Glucose_injectable(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,\
                    stockout_serum=MalariaReport.YES).count()


class EvolutionStructuresRuptureStockProduitPaluGrave(IndicatorTable):
    """ Gaphe: Évolution des proportions  de cas de paludisme simple

        traités par CTA Chez les moins de 5 ans et les 5 ans et plus """

    name = _(u"Figure 8")
    title = _(u" ")
    caption = _(u"Evolution du pourcentage de structures avec rupture" \
                u"de stock en produits de prise en charge des cas de" \
                u"paludisme grave")
    type = 'graph'
    graph_type = 'line'

    default_options = {'with_percentage': False, \
                       'with_reference': False, \
                       'with_data': True, \
                       'only_percent': False}

    @indicator(1)
    @label(u"Arthemeter Injactable")
    def structures_rupture_stock_arthemeter_injectable(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,\
                    stockout_artemether=MalariaReport.YES).count()

    @indicator(2)
    @label(u"Quinine Injectable")
    def structures_rupture_stock_Quinine_injectable(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,\
                    stockout_quinine=MalariaReport.YES).count()

    @indicator(3)
    @label(u"Serum Glucosé 10%")
    def structures_rupture_stock_Serum_Glucose_injectable(self, period):
        children = self.entity.get_children()
        return MalariaReport.validated.filter(entity__in=children,\
                    stockout_serum=MalariaReport.YES).count()

WIDGETS = [PourcentageStructuresRuptureStockProduitPaluGrave, \
            EvolutionStructuresRuptureStockProduitPaluGrave]
