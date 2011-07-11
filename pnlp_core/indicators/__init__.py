#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

INDICATOR_SECTIONS = \
    [{'id': '1', 'label': u"Identification de la structure ayant notifié " \
                          u"les données", 'sections': {}},
     {'id': '2', 'label': u"Morbidité (Cas suspects, testés/confirmés)", \
          'sections': {'all': u"Tout âge confondu", \
                       'under_five': u"Moins de 5 ans", \
                       'over_five': u"5 ans et plus", \
                       'pregnant_women': u"Femmes enceintes"}},
    {'id': '3', 'label': u"Traitement", 'sections': {}},
    {'id': '4', 'label': u"Hospitalisation", \
          'sections': {'all': u"Tout âge confondu", \
                       'under_five': u"Moins de 5 ans", \
                       'all_over_five': u"5 ans et plus (tous)", \
                       'pregnant_women': u"Femmes enceintes"}},
    {'id': '5', 'label': u"Décès", \
          'sections': {'all': u"Tout âge confondu", \
                       'under_five': u"Moins de 5 ans", \
                       'over_five': u"5 ans et plus", \
                       'pregnant_women': u"Femmes enceintes"}},
    {'id': '6', 'label': u"Moustiquaires imprégnées  d’Insecticides de " \
                         u"Longue Durée (MILD)", 'sections': {}},
    {'id': '7', 'label': u"Rupture de stock de CTA", 'sections': {}},
    {'id': '8', 'label': u"Rupture de stock des produits de PEC du " \
                         u"paludisme grave", 'sections': {}},
    {'id': '9', 'label': u"Rupture de stock MILD, TDR, SP", 'sections': {}},
    {'id': '10', 'label': u"CPN et Traitement Préventif Intermittent (TPI)", \
     'sections': {}}]
