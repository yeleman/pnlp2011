#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin


from bolibana.reporting.indicators import (IndicatorTable,
                                           reference, indicator, label)
from snisi_core.indicators.common import nb_stockout


class PourcentageStructuresRuptureStockMILDTDRSP(IndicatorTable):
    """ Tableau: Pourcentage de structures sans rupture de stock en MILD, TDR,

        SP """

    name = u"Tableau 19"
    title = u" "
    caption = u"Pourcentage de structures sans rupture de stock en" \
                u" MILD, TDR, SP"
    type = 'table'

    default_options = {'with_percentage': True,
                       'with_total': False,
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
            return self.entity.get_descendants()\
                              .filter(type__slug='cscom').count()

    @indicator(1, 'total_structures_in_the_district')
    @label(u"Structures sans rupture de stock de MILD")
    def stockout_bednet(self, period):
        nb_bednet = nb_stockout(self.entity, period, 'bednet')
        return nb_bednet

    @indicator(2, 'total_structures_in_the_district')
    @label(u"Structures sans rupture de stock de Test de Dépistage " \
           u"Rapide (TDR)")
    def stockout_rdt(self, period):
        nb_rdt = nb_stockout(self.entity, period, 'rdt')
        return nb_rdt

    @indicator(3, 'total_structures_in_the_district')
    @label(u"Structures sans rupture de stock en Sulfadoxine "\
           u"Pyriméthamine (SP)")
    def stockout_sp(self, period):
        nb_sp = nb_stockout(self.entity, period, 'sp')
        return nb_sp


class EvolutionPourcentageStructuresRuptureStockMILDTDRSP(IndicatorTable):
    """ Graphe: Evolution du pourcentage de Structures sans rupture de stock en

        MILD, TDR, SP """

    name = u"Figure 29"
    title = u" "
    caption = u"Evolution du pourcentage de Structures sans rupture de stock" \
              u" en MILD, TDR, SP"
    type = 'graph'
    graph_type = 'spline'

    default_options = {'with_percentage': True,
                       'with_reference': False,
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
            return self.entity.get_descendants()\
                              .filter(type__slug='cscom').count()

    @indicator(1, 'total_structures_in_the_district')
    @label(u"MILD")
    def stockout_bednet(self, period):
        nb_bednet = nb_stockout(self.entity, period, 'bednet')
        return nb_bednet

    @indicator(2, 'total_structures_in_the_district')
    @label(u"TDR")
    def stockout_rdt(self, period):
        nb_rdt = nb_stockout(self.entity, period, 'rdt')
        return nb_rdt

    @indicator(3, 'total_structures_in_the_district')
    @label(u"SP")
    def stockout_sp(self, period):
        nb_sp = nb_stockout(self.entity, period, 'sp')
        return nb_sp

WIDGETS = [PourcentageStructuresRuptureStockMILDTDRSP,
           EvolutionPourcentageStructuresRuptureStockMILDTDRSP]
