#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import random

from django.contrib.auth.models import ContentType

from bolibana.models.Access import Access
from bolibana.models.Role import Role

proverbs = [
    ('bm', u"dɔlɔ tɛ bɔ bɛɛ ka fɔ la",
     u"La bière n'est pas préparée à la demande de n'importe qui."),
    ('bm', u"hakilima bɛɛ ye kulu kuncɛmana dɔn fuga ye",
     u"Tout homme raisonnable sait que sur la montagne " \
     u"il y a une surface plate."),
    ('bm', u"ji ma masa dɔn", u"Le fleuve ne connaît pas le roi."),
    ('bm', u"mɔgɔ fila la tuma dɔ tɛ kelen ye",
     u"Un moment ne reflète pas la même chose pour deux personnes."),
    ('bm', u"ni warabilen bolo tɛ zaban mun sɔrɔ a ba fɔ ko a kumulen dɔ",
     u"Du zaban que le singe ne peut attraper, il dit qu'il est amère."),
    ('bm', u"seli si tɛ buranmuso sudon bɔ",
     u"Aucune prière ne vaut l'enterrement de sa belle-mère."),
    ('bm', u"tulon-ka-yɛlɛ bɛ dugu diya",
     u"Le divertissement et les rires rendent agréable la vie au village."),
    ('ses', u"amar guusu mana tii hansi huro do",
     u"Le trou de la panthère n'a pas de crotte de chien. "),
    ('ses', u"goy ra nafaw goo",
     u"C'est en travaillant que l'on devient utile."),
    ('ses', u"kaani si boro wii", u"Le plaisir ne tue pas l'homme."),
    ('ses', u"waafakay cine si bara", u"L'entente n'a pas d'égal."),
    ('ses', u"šennikoonu jew no", u"La parole sans importance, c'est la soif.")
]


def get_level_for(provider):
    """ EntityType slug of best (# of descendants) access for a provider """
    # finds best access
    # based on number of descendants
    # in the entities hierarchy
    best_access = provider.access() or Access.objects.get(
        role=Role.objects.get(slug='guest'), object_id=1,
        content_type=ContentType.objects.get(app_label='bolibana', model='entity'))

    return best_access.target.type.slug


def random_proverb():
    """ sends a (lang, original, translation) random proverb fortune """
    langs = {'ses': u"soŋay koyraboro šenni", 'bm': u"bamanakan"}
    p = proverbs[random.randint(0, len(proverbs) - 1)]
    return (langs[p[0]], p[1], p[2])
