#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin


from bolibana.reporting.indicators import (IndicatorTable,
                                           reference, indicator, label)
from snisi_core.indicators.common import (nb_stockout, MalariaIndicatorTable,
                                          period_is_expected)


class PourcentageStructuresRuptureStockProduitPaluGrave(IndicatorTable,
                                                        MalariaIndicatorTable):
    """ Tableau: Pourcentage de structures avec Rupture de stock en produits

    de prise en charge des cas de paludisme grave """

    name = u"Tableau 18"
    title = u" "
    caption = u"Pourcentage de structures avec rupture de stock en" \
             "produits de prise en charge des cas de paludisme grave"
    type = 'table'

    default_options = {'with_percentage': True,
                       'with_total': False,
                       'with_reference': True}

    def period_is_valid(self, period):
        return period_is_expected(entity=self.entity, period=period)

    @reference
    @indicator(0)
    @label(u"Nombre total de structures dans le district")
    def nombre_total_structures_district(self, period):
        if self.entity.type.slug == 'cscom':
            return 1
        else:
            return self.entity.get_descendants()\
                              .filter(type__slug='cscom').count()

    @indicator(1, "nombre_total_structures_district")
    @label(u"Structures sans rupture de stock d’Artheméter Injectable")
    def structures_rupture_stock_arthemeter_injectable(self, period):
        nb_artemether = nb_stockout(self.entity, period, 'artemether')
        return nb_artemether

    @indicator(2, "nombre_total_structures_district")
    @label(u"Structures sans rupture de stock de Quinine Injectable")
    def structures_rupture_stock_Quinine_injectable(self, period):
        nb_quinine = nb_stockout(self.entity, period, 'quinine')
        return nb_quinine

    @indicator(3, "nombre_total_structures_district")
    @label(u"Structures sans rupture de stock en Sérum Glucosé 10%")
    def structures_rupture_stock_Serum_Glucose_injectable(self, period):
        nb_serum = nb_stockout(self.entity, period, 'serum')
        return nb_serum


class EvolutionStructuresRuptureStockProduitPaluGrave(IndicatorTable):
    """ Gaphe: Évolution des proportions  de cas de paludisme simple

        traités par CTA Chez les moins de 5 ans et les 5 ans et plus """

    name = u"Figure 28"
    title = u" "
    caption = u"Evolution du pourcentage de structures sans rupture de stock" \
              u" en produits de prise en charge des cas de paludisme grave"
    type = 'graph'
    graph_type = 'spline'

    default_options = {'with_percentage': True,
                       'with_reference': False,
                       'with_data': False,
                       'only_percent': True}

    @reference
    @indicator(0)
    def total_structures_in_the_district(self, period):
        if self.entity.type.slug == 'cscom':
            return 1
        else:
            return self.entity.get_descendants()\
                              .filter(type__slug='cscom').count()

    @indicator(1, 'total_structures_in_the_district')
    @label(u"Arthemeter Injectable")
    def structures_rupture_stock_arthemeter_injectable(self, period):
        nb_artemether = nb_stockout(self.entity, period, 'artemether')
        return nb_artemether

    @indicator(2, 'total_structures_in_the_district')
    @label(u"Quinine Injectable")
    def structures_rupture_stock_Quinine_injectable(self, period):
        nb_quinine = nb_stockout(self.entity, period, 'quinine')
        return nb_quinine

    @indicator(3, 'total_structures_in_the_district')
    @label(u"Serum Glucosé 10%")
    def structures_rupture_stock_Serum_Glucose_injectable(self, period):
        nb_serum = nb_stockout(self.entity, period, 'serum')
        return nb_serum

WIDGETS = [PourcentageStructuresRuptureStockProduitPaluGrave,
            EvolutionStructuresRuptureStockProduitPaluGrave]
