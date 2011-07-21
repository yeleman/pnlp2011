#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

INDICATOR_SECTIONS = \
    {'1': {'id': '1', 'label': u"Identification de la structure " \
                               u"ayant notifié les données", \
                                'sections': {}},
     '2a': {'id': '2a', 'label': u"Morbidité (Cas suspects, " \
                                 u"testés/confirmés)", \
          'sections': {'all': u"Tout âge confondu", \
                       'under_five': u"Moins de 5 ans", \
                       'over_five': u"5 ans et plus", \
                       'pregnant_women': u"Femmes enceintes"}},
    '2b': {'id': '2b', 'label': u"Traitement par CTA", 'sections': {}},
    '3': {'id': '3', 'label': u"Traitement", 'sections': {}},
    '4': {'id': '4', 'label': u"Hospitalisation", \
          'sections': {'all': u"Tout âge confondu", \
                       'under_five': u"Moins de 5 ans", \
                       'all_over_five': u"5 ans et plus (tous)", \
                       'pregnant_women': u"Femmes enceintes"}},
    '5': {'id': '5', 'label': u"Décès", \
          'sections': {'all': u"Tout âge confondu", \
                       'under_five': u"Moins de 5 ans", \
                       'over_five': u"5 ans et plus", \
                       'pregnant_women': u"Femmes enceintes"}},
    '6': {'id': '6', 'label': u"Moustiquaires imprégnées  " \
                              u"d’Insecticides de " \
                         u"Longue Durée (MILD)", 'sections': {}},
    '7': {'id': '7', 'label': u"Rupture de stock de CTA", \
                                'sections': {}},
    '8': {'id': '8', 'label': u"Rupture de stock des produits de PEC du " \
                         u"paludisme grave", 'sections': {}},
    '9': {'id': '9', 'label': u"Rupture de stock MILD, TDR, SP", \
          'sections': {}},
    '10': {'id': '10', 'label': u"CPN et Traitement Préventif " \
                                u"Intermittent (TPI)", \
     'sections': {}}}
