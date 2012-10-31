#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.reporting.indicators import (IndicatorTable, \
                                           reference, indicator, label)
from bolibana.models import Entity
from pnlp_core.models import MalariaReport


class PromptitudeRapportageSegouBamako(IndicatorTable):
    """ Tableau: Données sur la CPN et le Traitement Préventif  Intermittent

        (TPI) """

    name = u"Tableau 30"
    title = u" "
    caption = u"Pourcentage de structures ayant transmis leurs données"
    type = 'table'

    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return True

    @reference
    @indicator(0, 'total_structures_in_bamako')
    @label(u"Structures à Bamako")
    def total_structures_in_bamako(self, period):
        entity = Entity.objects.get(slug='bamako')
        return entity.get_descendants()\
                                 .filter(type__slug='cscom').count()

    @indicator(1, 'total_structures_in_bamako')
    @label(u"Bamako")
    def number_tautovalide_bamako(self, period):
        entity = Entity.objects.get(slug='bamako')
        descendants = entity.get_descendants()\
                                 .filter(type__slug='cscom')
        return MalariaReport.objects.filter(period=period,
                                            entity__in=descendants).count()

    @reference
    @indicator(2, 'total_structures_in_segou')
    @label(u"Structures à Ségou")
    def total_structures_in_segou(self, period):
        entity = Entity.objects.get(slug='segou')
        return entity.get_descendants()\
                                 .filter(type__slug='cscom').count()

    @indicator(3, 'total_structures_in_segou')
    @label(u"Ségou")
    def number_tautovalide_segou(self, period):
        entity = Entity.objects.get(slug='segou')
        descendants = entity.get_descendants()\
                                 .filter(type__slug='cscom')
        return MalariaReport.objects.filter(period=period,
                                            entity__in=descendants).count()


class FigurePromptitudeRapportageSegouBamako(PromptitudeRapportageSegouBamako):
    """ Graphe: Evolution de la  CPN1, SP1 et SP2 chez les femmes enceintes"""

    name = u"Figure 40"
    title = u" "
    caption = u"Pourcentage de structures ayant transmis leurs données"
    type = 'graph'
    graph_type = 'spline'

    default_options = {'with_percentage': True, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': True}

    @indicator(0, 'total_structures_in_bamako')
    @label(u"% de structures ayant transmis à Bamako")
    def number_tautovalide_bamako(self, period):
        return super(FigurePromptitudeRapportageSegouBamako,
                     self).number_tautovalide_bamako(period)

    @indicator(1, 'total_structures_in_segou')
    @label(u"% de structures ayant transmis à Ségou")
    def number_tautovalide_segou(self, period):
        return super(FigurePromptitudeRapportageSegouBamako,
                     self).number_tautovalide_segou(period)


class PromptitudeNionoMacinaAutres(IndicatorTable):
    """ Tableau: Données sur la CPN et le Traitement Préventif  Intermittent

        (TPI) """

    name = u"Tableau 31"
    title = u" "
    caption = u"Pourcentage de structures ayant transmis leurs données"
    type = 'table'

    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return True

    @reference
    @indicator(0, 'total_structures_in_niono')
    @label(u"Structures à Niono")
    def total_structures_in_niono(self, period):
        entity = Entity.objects.get(slug='nion')

        return entity.get_descendants()\
                                 .filter(type__slug='cscom').count()

    @indicator(1, 'total_structures_in_niono')
    @label(u"structures ayant transmis à Niono")
    def number_tautovalide_niono(self, period):
        entity = Entity.objects.get(slug='nion')
        descendants = entity.get_descendants()\
                                 .filter(type__slug='cscom')

        return MalariaReport.objects.filter(period=period,
                                            entity__in=descendants).count()

    @reference
    @indicator(2, 'total_structures_in_macina')
    @label(u"Structures à Macina")
    def total_structures_in_macina(self, period):
        entity = Entity.objects.get(slug='maci')

        return entity.get_descendants()\
                                 .filter(type__slug='cscom').count()

    @indicator(3, 'total_structures_in_macina')
    @label(u"structures ayant transmis à Macina")
    def number_tautovalide_macina(self, period):
        entity = Entity.objects.get(slug='maci')
        descendants = entity.get_descendants()\
                                 .filter(type__slug='cscom')

        return MalariaReport.objects.filter(period=period,
                                            entity__in=descendants).count()

    @reference
    @indicator(4, 'other_structures')
    @label(u"Les 8 autres districts")
    def other_structures(self, period):
        markala = Entity.objects.get(slug='mark').get_descendants()\
                                 .filter(type__slug='cscom').count()
        baroueli = Entity.objects.get(slug='baro').get_descendants()\
                                 .filter(type__slug='cscom').count()
        commune4 = Entity.objects.get(slug='com4').get_descendants()\
                                 .filter(type__slug='cscom').count()
        commune5 = Entity.objects.get(slug='com5').get_descendants()\
                                 .filter(type__slug='cscom').count()
        bla = Entity.objects.get(slug='bla').get_descendants()\
                                 .filter(type__slug='cscom').count()
        san = Entity.objects.get(slug='san').get_descendants()\
                                 .filter(type__slug='cscom').count()
        tominian = Entity.objects.get(slug='tomi').get_descendants()\
                                 .filter(type__slug='cscom').count()
        segou = Entity.objects.get(slug='sego2').get_descendants()\
                                 .filter(type__slug='cscom').count()

        return markala + baroueli + commune4 + commune5 + bla + san + \
                tominian + segou

    @indicator(5, 'other_structures')
    @label(u"structures ayant transmis dans les 8 autres districts")
    def other_structures1(self, period):
        descendants = []
        markala = Entity.objects.get(slug='mark').get_descendants()\
                                 .filter(type__slug='cscom')
        descendants.append(markala)
        baroueli = Entity.objects.get(slug='baro').get_descendants()\
                                 .filter(type__slug='cscom')
        descendants.append(baroueli)
        commune4 = Entity.objects.get(slug='com4').get_descendants()\
                                 .filter(type__slug='cscom')
        descendants.append(commune4)
        commune5 = Entity.objects.get(slug='com5').get_descendants()\
                                 .filter(type__slug='cscom')
        descendants.append(commune5)
        bla = Entity.objects.get(slug='bla').get_descendants()\
                                 .filter(type__slug='cscom')
        descendants.append(bla)
        san = Entity.objects.get(slug='san').get_descendants()\
                                 .filter(type__slug='cscom')
        descendants.append(san)
        tominian = Entity.objects.get(slug='tomi').get_descendants()\
                                 .filter(type__slug='cscom')
        descendants.append(tominian)
        segou = Entity.objects.get(slug='sego2').get_descendants()\
                                 .filter(type__slug='cscom')
        descendants.append(segou)
        nb = 0

        for descendant in descendants:
            nb += MalariaReport.objects.filter(period=period,
                                            entity__in=descendant).count()

        return nb


class GraphePromptitudeNionoMacinaAutres(PromptitudeNionoMacinaAutres):
    """ Graphe: Nombre de femmes enceintes reçues en CPN1 et Nombre de

        MILD distribuées aux femmes enceintes"""

    name = u"Figure 31"
    title = u" "
    caption = u"Pourcentage de structures ayant transmis leurs données"
    graph_type = 'spline'
    type = 'graph'

    default_options = {'with_percentage': True, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': True}

    @indicator(0, 'total_structures_in_niono')
    @label(u"% de structures ayant transmis à Niono")
    def number_tautovalide_niono(self, period):
        return super(GraphePromptitudeNionoMacinaAutres,
                     self).number_tautovalide_niono(period)

    @indicator(1, 'total_structures_in_macina')
    @label(u"% de structures ayant transmis à Macina")
    def number_tautovalide_macina(self, period):
        return super(GraphePromptitudeNionoMacinaAutres,
                     self).number_tautovalide_macina(period)

    @indicator(2, 'other_structures')
    @label(u"% de structures ayant transmis dans les 8 autres districts")
    def other_structures1(self, period):
        return super(GraphePromptitudeNionoMacinaAutres,
                     self).other_structures1(period)


WIDGETS = [PromptitudeRapportageSegouBamako,
           FigurePromptitudeRapportageSegouBamako,
           PromptitudeNionoMacinaAutres, GraphePromptitudeNionoMacinaAutres]
