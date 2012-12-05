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
            return self.get_query_set().filter(created_on__gte=period.start_on,
                                               created_on__lte=period.end_on)


class PregnancyReport(IndividualReport):

    NONE = 0
    ALIVE = 1
    STILLBORN = 2
    ABORTION = 3

    RESULT = ((NONE, "None"),
              (ALIVE, "Né vivant"),
              (STILLBORN, "Mort-né"),
              (ABORTION, "Avortement"))

    UNFPA = 'U'
    CREDOS = 'C'
    SOURCES = ((UNFPA, u"UNFPA"),
               (CREDOS, u"CREDOS"))

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _(u"Pregnancy Report")
        verbose_name_plural = _(u"Pregnancy Reports")

    reporting_location = models.ForeignKey(Entity,
                                         related_name='pregnancy_reported_in',
                                         verbose_name=_(u"Reporting location"))
    householder_name = models.CharField(max_length=100,
                                        verbose_name=_(u"Householder name"))
    mother_name = models.CharField(max_length=100,
                                   verbose_name=_(u"Mother name"))
    dob = models.DateField(verbose_name=_(u"Date of birth"))
    dob_auto = models.BooleanField(default=False,
                                   verbose_name=_(u"DOB is an estimation?"))
    pregnancy_age = models.IntegerField(max_length=2,
                                        verbose_name=_(u"Pregnancy age"))
    expected_delivery_date = models.DateField(verbose_name=_(u"Expected "
                                                             u"delivery date"))
    delivery_date = models.DateField(blank=True, null=True,
                                     verbose_name=_(u"Delivery date"))
    pregnancy_result = models.IntegerField(max_length=1, choices=RESULT,
                                        verbose_name=_(u"Pregnancy result"))

    source = models.CharField(max_length=1, null=True,
                              blank=True, choices=SOURCES)

    # django manager first
    objects = models.Manager()
    periods = PeriodManager()

    def __unicode__(self):
        return ugettext(u"%(mother_name)s/%(dob)s"
                % {'mother_name': self.mother_name.title(),
                   'dob': self.dob.strftime('%d-%m-%Y')})


reversion.register(PregnancyReport)
