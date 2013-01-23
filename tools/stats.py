#/usr/bin/env python

from bolibana.models.Entity import Entity
from bolibana.models.Period import Period
from snisi_core.models.MalariaReport import MalariaR


def data(slug, period):
    rep = MalariaR.objects.filter(entity__parent__slug=slug, period=period).count()
    ent = Entity.objects.get(slug=slug).get_children().count()
    percent = float(rep) / ent
    return (rep, ent, percent)


def stats(month, year):
    period = Period.find_create_from(month=month, year=year)
    for s, n in {'sego2': u"Segou",
                 'mark': u"Markala",
                 'nion': u"Niono",
                 'bla': u"Bla",
                 'tomi': u"Tominian",
                 'baro': u"Baroueli",
                 'san': u"San",
                 'maci': u"Macina",
                 'com4': u"BKO CIV",
                 'com5': u"BKO CV"}.items():
        d = data(s, period)
        print(u"%s\t%d\t%d\t%f" % (n, d[0], d[1], d[2]))
