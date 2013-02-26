#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin


from bolibana.reporting.indicators import (IndicatorTable, reference,
                                           indicator, label)
from snisi_core.indicators.common import (nb_stockout, MalariaIndicatorTable,
                                          period_is_expected)


class PourcentageStructuresRuptureStockCTADistrict(IndicatorTable,
                                                   MalariaIndicatorTable):
    """ Tableau: Pourcentage de structures avec Rupture de stock de CTA dans

        le district """

    name = u"Tableau 17"
    title = u" "
    caption = (u"Pourcentage de structures sans Rupture de stock de CTA dans"
               u" le district")
    type = 'table'

    default_options = {'with_percentage': True,
                       'with_total': False,
                       'with_reference': True}

    def period_is_valid(self, period):
        return period_is_expected(entity=self.entity, period=period)

    @reference
    @indicator(0)
    @label(u"Nombre total de structures dans le district")
    def total_structures_in_the_district(self, period):
        if self.entity.type.slug == 'cscom':
            return 1
        else:
            return self.entity.get_descendants() \
                              .filter(type__slug='cscom').count()

    @indicator(1, 'total_structures_in_the_district')
    @label(u"Structures sans rupture de stock en CTA Nourrisson - Enfant")
    def stockout_act_children(self, period):
        nb_act_children = nb_stockout(self.entity, period, 'act_children')
        return nb_act_children

    @indicator(2, 'total_structures_in_the_district')
    @label(u"Structures sans rupture de stock en CTA Adolescent")
    def stockout_act_youth(self, period):
        nb_act_youth = nb_stockout(self.entity, period, 'act_youth')
        return nb_act_youth

    @indicator(3, 'total_structures_in_the_district')
    @label(u"Structures sans rupture de stock en CTA Adulte")
    def stockout_act_adult(self, period):
        nb_act_adult = nb_stockout(self.entity, period, 'act_adult')
        return nb_act_adult


class EvolutionPourcentageStructuresRuptureStockCTA(IndicatorTable,
                                                    MalariaIndicatorTable):
    """ Graphe: Evolution du pourcentage de Structures avec rupture de stock en

        CTA """

    name = u"Figure 27"
    title = u" "
    caption = (u"Evolution du pourcentage de Structures sans rupture de "
               u"stock en CTA (Nourrisson-Enfant, Adolescent, Adulte")
    type = 'graph'
    graph_type = 'spline'

    default_options = {'with_percentage': True,
                       'with_reference': False,
                       'with_data': False,
                       'only_percent': True}

    @reference
    @indicator(0)
    def total_structures_in_the_district(self, period):
        return self.entity.get_descendants()\
                              .filter(type__slug='cscom').count()

    @indicator(1, 'total_structures_in_the_district')
    @label(u"CTA Nourrisson - Enfant")
    def stockout_act_children(self, period):
        nb_act_children = nb_stockout(self.entity, period, 'act_children')
        return nb_act_children

    @indicator(2, 'total_structures_in_the_district')
    @label(u"CTA Adolescent")
    def stockout_act_youth(self, period):
        nb_act_youth = nb_stockout(self.entity, period, 'act_youth')
        return nb_act_youth

    @indicator(3, 'total_structures_in_the_district')
    @label(u"CTA Adulte")
    def stockout_act_adult(self, period):
        nb_act_adult = nb_stockout(self.entity, period, 'act_adult')
        return nb_act_adult

WIDGETS = [PourcentageStructuresRuptureStockCTADistrict,
           EvolutionPourcentageStructuresRuptureStockCTA]
