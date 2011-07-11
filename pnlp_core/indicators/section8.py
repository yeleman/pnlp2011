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
    """Pourcentage de structures avec Rupture de stock en produits
    de prise en charge des cas de paludisme grave"""

    name = _(u"Tableau 8")
    title = _(u" ")
    caption = _(u"Pourcentage de structures avec Rupture de stock en" \
             "produits de prise en charge des cas de paludisme grave")
    type = 'table'

    default_options = {'with_percentage': True, \
                       'with_total': True, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    @label(u"Nombre total de structures dans le district")
    def Nombre_total_structures_district(self, period):
        report = get_report_for(self.entity, period)
        print self.entity.children.count(),'nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn'
        return report.u5_total_simple_malaria_cases


WIDGETS = [PourcentageStructuresRuptureStockProduitPaluGrave]
