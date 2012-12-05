#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

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
            return self.get_query_set().filter(dod__gte=period.start_on,
                                               dod__lte=period.end_on)


class ChildrenMortalityReport(IndividualReport):

    HOME = 'D'
    CENTER = 'C'
    OTHER = 'A'
    DEATHPLACE = ((HOME, _(u"Domicile")),
                  (CENTER, _(u"Centre")),
                  (OTHER, _(u"Autre")))

    UNFPA = 'U'
    CREDOS = 'C'
    SOURCES = ((UNFPA, u"UNFPA"),
               (CREDOS, u"CREDOS"))

    MALE = 'M'
    FEMALE = 'F'
    SEX = ((FEMALE, _(u"F")), (MALE, _(u"M")))

    CAUSE_FEVER = 'f'
    CAUSE_DIARRHEA = 'd'
    CAUSE_DYSPNEA = 'b'
    CAUSE_ANEMIA = 'a'
    CAUSE_RASH = 'r'
    CAUSE_COUGH = 'c'
    CAUSE_VOMITING = 'v'
    CAUSE_NUCHAL_RIGIDITY = 'n'
    CAUSE_RED_EYE = 'e'
    CAUSE_EAT_REFUSAL = 't'
    CAUSE_OTHER = 'o'
    DEATH_CAUSES_t = (
                      (CAUSE_FEVER, u"Fever"),
                      (CAUSE_DIARRHEA, u"Diarrhea"),
                      (CAUSE_DYSPNEA, u"Dyspnea"),
                      (CAUSE_ANEMIA, u"Anemia"),
                      (CAUSE_RASH, u"Rash"),
                      (CAUSE_COUGH, u"Cough"),
                      (CAUSE_VOMITING, u"Vomiting"),
                      (CAUSE_NUCHAL_RIGIDITY, u"Nuchal Rigidity"),
                      (CAUSE_RED_EYE, u"Red Eye"),
                      (CAUSE_EAT_REFUSAL, u"Eat Refusal"),
                      (CAUSE_OTHER, u"Other")
        )

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _(u"Children Mortality Report")
        verbose_name_plural = _(u"Children Mortality Reports")

    reporting_location = models.ForeignKey(Entity,
                                         related_name='children_reported_in',
                                         verbose_name=_(u"Reporting location"))
    name = models.CharField(max_length=100,
                            verbose_name=_(u"Name of the deceased"))
    sex = models.CharField(max_length=1,
                           choices=SEX,
                           verbose_name=_(u"Sex"))
    dob = models.DateField(verbose_name=_(u"Date of birth"))
    dob_auto = models.BooleanField(default=False,
                                   verbose_name=_(u"DOB is an estimation?"))
    dod = models.DateField(verbose_name=_(u"Date of death"))
    death_location = models.ForeignKey(Entity,
                                       related_name='children_dead_in',
                                       verbose_name=_(u"Death Location"))
    death_place = models.CharField(max_length=1,
                                   choices=DEATHPLACE,
                                   verbose_name=_(u"Place of death"))

    cause_of_death = models.CharField(max_length=1, choices=DEATH_CAUSES_t)

    source = models.CharField(max_length=1, null=True,
                              blank=True, choices=SOURCES)

    # django manager first
    objects = models.Manager()
    periods = PeriodManager()

    def __unicode__(self):
        return ugettext(u"%(name)s/%(dod)s"
                % {'name': self.name.title(),
                   'dod': self.dod.strftime('%d-%m-%Y')})


reversion.register(ChildrenMortalityReport)
