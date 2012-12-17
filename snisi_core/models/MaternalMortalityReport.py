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


class MaternalMortalityReport(IndividualReport):

    UNFPA = 'U'
    CREDOS = 'C'
    SOURCES = ((UNFPA, u"UNFPA"),
               (CREDOS, u"CREDOS"))

    CAUSE_BLEEDING = 'b'
    CAUSE_FEVER = 'f'
    CAUSE_HTN = 'h'
    CAUSE_DIARRHEA = 'd'
    CAUSE_CRISIS = 'c'
    CAUSE_MISCARRIAGE = 'm'
    CAUSE_ABORTION = 'a'
    CAUSE_OTHER = 'o'
    DEATH_CAUSES_t = ((CAUSE_BLEEDING, u"Bleeding"),
                    (CAUSE_FEVER, u"Fever"),
                    (CAUSE_HTN, u"High Blood Pressure"),
                    (CAUSE_DIARRHEA, u"Diarrhea"),
                    (CAUSE_CRISIS, u"Crisis"),
                    (CAUSE_MISCARRIAGE, u"Miscarriage"),
                    (CAUSE_ABORTION, u"Abortion"),
                    (CAUSE_OTHER, u"Other"))
    DEATH_CAUSES = {
                    CAUSE_BLEEDING: u"Bleeding",
                    CAUSE_FEVER: u"Fever",
                    CAUSE_HTN: u"High Blood Pressure",
                    CAUSE_DIARRHEA: u"Diarrhea",
                    CAUSE_CRISIS: u"Crisis",
                    CAUSE_MISCARRIAGE: u"Miscarriage",
                    CAUSE_ABORTION: u"Abortion",
                    CAUSE_OTHER: u"Other"}

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _(u"Maternal Mortality Report")
        verbose_name_plural = _(u"Maternal Mortality Reports")

    reporting_location = models.ForeignKey(Entity,
                                           related_name='maternal_reported_in',
                                           verbose_name=_(u"Reporting "
                                                          u"location"))
    name = models.CharField(max_length=100,
                            verbose_name=_(u"Name of the deceased"))
    dob = models.DateField(verbose_name=_(u"Date of birth"))
    dob_auto = models.BooleanField(default=False,
                                   verbose_name=_(u"DOB is an estimation?"))
    dod = models.DateField(verbose_name=_(u"Date of death"))
    death_location = models.ForeignKey(Entity,
                                       related_name='maternal_dead_in',
                                       verbose_name=_(u"Place of death"))
    living_children = models.PositiveIntegerField(verbose_name=_(u"Living "
                                                 u"children of the deceased"))
    dead_children = models.PositiveIntegerField(verbose_name=_(u"Dead children"
                                                u" of the deceased"))
    pregnant = models.BooleanField(verbose_name=_(u"Pregnant?"))
    pregnancy_weeks = models.PositiveIntegerField(null=True, blank=True,
                                                  verbose_name=_(u"Duration "
                                                  u"of the pregnancy (weeks)"))
    pregnancy_related_death = models.BooleanField(default=False,
                                                  verbose_name=_(u"Pregnancy "
                                                  u"related death"))

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


reversion.register(MaternalMortalityReport)
