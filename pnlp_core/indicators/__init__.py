#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

INDICATOR_SECTIONS = \
    {'1': {'id': '1', 'label': u"Identification de la structure ayant notifié les données", \
          'sections': {'all': u"Tout âge confondu", \
                       'under_five': u"Moins de 5 ans", \
                       'over_five': u"5 ans et plus", \
                       'pregnant_women': u"Femmes enceintes"}},
    '2': {'id': '2', 'label': u"Traitement", 'sections': {}},
    '3': {'id': '3', 'label': u"Hospitalisation", \
          'sections': {'all': u"Tout âge confondu", \
                       'under_five': u"Moins de 5 ans", \
                       'all_over_five': u"5 ans et plus (tous)", \
                       'pregnant_women': u"Femmes enceintes"}},
    '4': {'id': '4', 'label': u"Décès", \
          'sections': {'all': u"Tout âge confondu", \
                       'under_five': u"Moins de 5 ans", \
                       'over_five': u"5 ans et plus", \
                       'pregnant_women': u"Femmes enceintes"}},
    '5': {'id': '5', 'label': u"Moustiquaires imprégnées  d’Insecticides de Longue Durée (MILD)", 'sections': {}},
    '6': {'id': '6', 'label': u"Rupture de stock de CTA", 'sections': {}},
    '7': {'id': '7', 'label': u"Rupture de stock des produits de PEC du paludisme grave", 'sections': {}},
    '8': {'id': '8', 'label': u"Rupture de stock MILD, TDR, SP", 'sections': {}},
    '9': {'id': '9', 'label': u"CPN et Traitement Préventif  Intermittent  (TPI)", 'sections': {}}}
