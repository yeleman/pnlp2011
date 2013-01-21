#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.reporting.indicators import (IndicatorTable, \
                                           reference, indicator, label)
from snisi_core.models.MalariaReport import MalariaR


class TableauPromptitudeRapportage(IndicatorTable):
    name = u"Tableau 1"
    title = u" "
    caption = u"Pourcentage de structures ayant transmis leurs" \
              u" formulaires de collecte dans les délais prévus"
    type = 'table'

    default_options = {'with_percentage': False, \
                       'with_total': False, \
                       'with_reference': False}

    def period_is_valid(self, period):
        return True

    @indicator(0)
    @label(u"Nombre total de structures dans le district")
    def total_structures_in_the_district(self, period):
        if self.entity.type.slug == 'cscom':
            return 1
        else:
            return self.entity.get_descendants()\
                              .filter(type__slug='cscom').count()

    @indicator(1)
    @label(u"Nombre de structures ayant transmis leurs formulaires " \
           u"de collecte dans les délais prévus")
    def number_tautovalide(self, period):
        if self.entity.type.slug == 'cscom':
            descendants = [self.entity]
        else:
            descendants = self.entity.get_descendants()\
                                     .filter(type__slug='cscom')
        return MalariaR.objects.filter(period=period,
                                            entity__in=descendants).count()


class FigurePromptitudeRapportage(IndicatorTable):
    name = u"Figure 1"
    title = u""
    caption = u"Evolution de la promptitude de la notification dans " \
              u"le district"
    type = 'graph'
    graph_type = 'spline'

    default_options = {'with_percentage': True, \
                   'with_total': False, \
                   'with_reference': False, \
                   'with_data': False,
                   'only_percent': True}

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

    @indicator(1)
    @label(u"% de structures ayant tranmis le formulaire de collecte " \
           u"dans les délais prévus")
    def number_tautovalide(self, period):
        if self.entity.type.slug == 'cscom':
            descendants = [self.entity]
        else:
            descendants = self.entity.get_descendants()\
                                     .filter(type__slug='cscom')
        return MalariaR.objects.filter(period=period,
                                            entity__in=descendants).count()

WIDGETS = [TableauPromptitudeRapportage, FigurePromptitudeRapportage]
