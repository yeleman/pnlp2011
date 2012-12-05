#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou

import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from bolibana.models import Entity, IndividualReport


class PeriodManager(models.Manager):

    def get_query_set(self):
        return super(PeriodManager, self).get_query_set()

    def within(self, period=None):
        if not period:
            return self.get_query_set()
        else:
            return self.get_query_set().filter(dob__gte=period.start_on,
                                               dob__lte=period.end_on)


class BirthReport(IndividualReport):

    HOME = 'H'
    CENTER = 'C'
    OTHER = 'O'
    BIRTHPLACE = ((HOME, _(u"Home")),
                  (CENTER, _(u"Center")),
                  (OTHER, _(u"Other")))

    MALE = 'M'
    FEMALE = 'F'
    SEX = ((FEMALE, _(u"F")), (MALE, _(u"M")))

    UNFPA = 'U'
    CREDOS = 'C'
    SOURCES = ((UNFPA, u"UNFPA"),
               (CREDOS, u"CREDOS"))

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _(u"Birth Report")
        verbose_name_plural = _(u"Birth Reports")

    reporting_location = models.ForeignKey(Entity,
                                        related_name='birth_reported_in',
                                        verbose_name=_(u"Reporting location"))
    family_name = models.CharField(max_length=100,
                                   verbose_name=_(u"Family name"))
    surname_mother = models.CharField(max_length=100, blank=True, null=True,
                                      verbose_name=_(u"Surname of mother"))
    surname_child = models.CharField(max_length=100, blank=True, null=True,
                                     verbose_name=_(u"Surname of child"))
    sex = models.CharField(max_length=1,
                           choices=SEX,
                           verbose_name=_(u"Sex"))
    dob = models.DateField(verbose_name=_(u"Date of birth"))
    dob_auto = models.BooleanField(default=False,
                                   verbose_name=_(u"DOB is an estimation?"))
    born_alive = models.BooleanField(verbose_name=_(u"Born alive"))
    birth_location = models.CharField(max_length=1,
                                     choices=BIRTHPLACE,
                                     verbose_name=_(u"Place of birth"))
    source = models.CharField(max_length=1, null=True,
                              blank=True, choices=SOURCES)

    # django manager first
    objects = models.Manager()
    periods = PeriodManager()

    def __unicode__(self):
        return ugettext(u"%(family_name)s/%(dob)s"
                % {'family_name': self.family_name.title(),
                   'dob': self.dob.strftime('%d-%m-%Y')})

    def full_name(self):
        if self.surname_child:
            return (u"%(surname_child)s %(family_name)s" %
            {'surname_child': self.surname_child,
            'family_name': self.family_name
            })
        elif self.surname_mother:
            return (u"%(surname_child)s %(family_name)s" %
            {'surname_mother': self.surname_mother,
            'family_name': self.family_name
            })
        else:
            return (u"%(family_name)s" %
            {'family_name': self.family_name})

    def full_name_dob(self):
        return self.full_name() + "/%(dob)s" % \
            {'dob': self.dob.strftime('%d-%m-%Y')}

reversion.register(BirthReport)
