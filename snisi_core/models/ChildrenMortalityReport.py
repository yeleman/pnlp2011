#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import reversion
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils.translation import ugettext_lazy as _, ugettext

from bolibana.models import Entity, IndividualReport, Report

from common import pre_save_report, post_save_report


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

    # django manager first
    objects = models.Manager()
    periods = PeriodManager()

    def __unicode__(self):
        return ugettext(u"%(name)s/%(dod)s"
                % {'name': self.name.title(),
                   'dod': self.dod.strftime('%d-%m-%Y')})

reversion.register(ChildrenMortalityReport)


class AggregatedChildrenMortalityReport(Report):

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _(u"Aggregated Children Mortality Report")
        verbose_name_plural = _(u"Aggregated Children Mortality Reports")

    sex_male = models.PositiveIntegerField()
    sexe_female = models.PositiveIntegerField()

    age_under_1w = models.PositiveIntegerField()
    age_under_2weeks = models.PositiveIntegerField()
    age_under_1month = models.PositiveIntegerField()
    age_under_3month = models.PositiveIntegerField()
    age_under_6month = models.PositiveIntegerField()
    age_under_9month = models.PositiveIntegerField()
    age_under_1 = models.PositiveIntegerField()
    age_under_2 = models.PositiveIntegerField()
    age_under_3 = models.PositiveIntegerField()
    age_under_4 = models.PositiveIntegerField()
    age_under_5 = models.PositiveIntegerField()

    death_home = models.PositiveIntegerField()
    death_center = models.PositiveIntegerField()
    death_other = models.PositiveIntegerField()

    cause_death_fever = models.PositiveIntegerField()
    cause_death_diarrhea = models.PositiveIntegerField()
    cause_death_dyspnea = models.PositiveIntegerField()
    cause_death_anemia = models.PositiveIntegerField()
    cause_death_rash = models.PositiveIntegerField()
    cause_death_cough = models.PositiveIntegerField()
    cause_death_vomiting = models.PositiveIntegerField()
    cause_death_nuchal_rigidity = models.PositiveIntegerField()
    cause_death_red_eye = models.PositiveIntegerField()
    cause_death_eat_refusal = models.PositiveIntegerField()
    cause_death_other = models.PositiveIntegerField()

    indiv_sources = models.ManyToManyField('ChildrenMortalityReport',
                                           verbose_name=_(u"Indiv. Sources"),
                                           blank=True, null=True,
                                           related_name='indiv_agg_children_mortality_reports')

    agg_sources = models.ManyToManyField('AggregatedChildrenMortalityReport',
                                         verbose_name=_(u"Aggr. Sources"),
                                         blank=True, null=True,
                                         related_name='aggregated_agg_children_mortality_reports')

    @classmethod
    def start(cls, period, entity, author, \
              type=Report.TYPE_AGGREGATED, *args, **kwargs):
        report = cls(period=period, entity=entity, created_by=author, \
                     modified_by=author, _status=cls.STATUS_CREATED, \
                     type=type)

        report.sex_male = 0
        report.sexe_female = 0

        report.age_under_1w = 0
        report.age_under_2weeks = 0
        report.age_under_1month = 0
        report.age_under_3month = 0
        report.age_under_6month = 0
        report.age_under_9month = 0
        report.age_under_1 = 0
        report.age_under_2 = 0
        report.age_under_3 = 0
        report.age_under_4 = 0
        report.age_under_5 = 0

        report.death_home = 0
        report.death_center = 0
        report.death_other = 0

        report.cause_death_fever = 0
        report.cause_death_diarrhea = 0
        report.cause_death_dyspnea = 0
        report.cause_death_anemia = 0
        report.cause_death_rash = 0
        report.cause_death_cough = 0
        report.cause_death_vomiting = 0
        report.cause_death_nuchal_rigidity = 0
        report.cause_death_red_eye = 0
        report.cause_death_eat_refusal = 0
        report.cause_death_other = 0

        return report

    @classmethod
    def create_from(cls, period, entity, author):

        # create empty
        agg_report = cls.start(entity, period, author)

        # find list of sources
        indiv_sources = ChildrenMortalityReport \
                            .objects \
                            .filter(dod__gte=period.start_on,
                                    dod__lte=period.end_on,
                                    death_location__in=entity.get_children())
        agg_sources = cls.objects.filter(period=period,
                                         entity__in=entity.get_children())

        sources = list(indiv_sources) + list(agg_sources)

        # loop on all sources
        for source in sources:
            if isinstance(source, ChildrenMortalityReport):
                cls.update_instance_with_indiv(agg_report, source)
            elif isinstance(source, cls):
                cls.update_instance_with_agg(agg_report, source)

        # keep a record of all sources
        for report in indiv_sources:
            agg_report.indiv_sources.add(report)

        for report in agg_sources:
            agg_report.agg_sources.add(report)

        with reversion.create_revision():
            agg_report.save()
            reversion.set_user(author.user)

        return agg_report

    @classmethod
    def update_instance_with_indiv(cls, report, instance):

        # sex
        if instance.sex == instance.MALE:
            report.sex_male += 1
        elif instance.sex == instance.FEMALE:
            report.sexe_female += 1

        # death place
        if instance.death_place == instance.HOME:
            report.death_home += 1
        elif instance.death_place == instance.CENTER:
            report.death_center += 1
        else:
            report.death_other += 1

        # cause of death
        if instance.cause_of_death == instance.CAUSE_FEVER:
            report.cause_death_fever += 1
        elif instance.cause_of_death == instance.CAUSE_DIARRHEA:
            report.cause_death_diarrhea += 1
        elif instance.cause_of_death == instance.CAUSE_DYSPNEA:
            report.cause_death_dyspnea += 1
        elif instance.cause_of_death == instance.CAUSE_ANEMIA:
            report.cause_death_anemia += 1
        elif instance.cause_of_death == instance.CAUSE_RASH:
            report.cause_death_rash += 1
        elif instance.cause_of_death == instance.CAUSE_COUGH:
            report.cause_death_cough += 1
        elif instance.cause_of_death == instance.CAUSE_VOMITING:
            report.cause_death_vomiting += 1
        elif instance.cause_of_death == instance.CAUSE_NUCHAL_RIGIDITY:
            report.cause_death_nuchal_rigidity += 1
        elif instance.cause_of_death == instance.CAUSE_RED_EYE:
            report.cause_death_red_eye += 1
        elif instance.cause_of_death == instance.CAUSE_EAT_REFUSAL:
            report.cause_death_eat_refusal += 1
        else:
            report.cause_death_other += 1

        # age
        age_days = (instance.dod - instance.dob).days
        if age_days < 7:
            report.age_under_1w += 1
        if age_days < 14:
            report.age_under_2weeks += 1
        if age_days < 30:
            report.age_under_1month += 1
        if age_days / 30 < 3:
            report.age_under_3month += 1
        if age_days / 30 < 6:
            report.age_under_6month += 1
        if age_days / 30 < 9:
            report.age_under_9month += 1
        if age_days < 365:
            report.age_under_1 += 1
        if age_days / 365 < 2:
            report.age_under_2 += 1
        if age_days / 365 < 3:
            report.age_under_3 += 1
        if age_days / 365 < 4:
            report.age_under_4 += 1
        if age_days / 365 <= 5:
            report.age_under_5 += 1

    @classmethod
    def update_instance_with_agg(cls, report, instance):

        report.sex_male += instance.sex_male
        report.sexe_female += instance.sexe_female

        report.age_under_1w += instance.age_under_1w
        report.age_under_2weeks += instance.age_under_2weeks
        report.age_under_1month += instance.age_under_1month
        report.age_under_3month += instance.age_under_3month
        report.age_under_6month += instance.age_under_6month
        report.age_under_9month += instance.age_under_9month
        report.age_under_1 += instance.age_under_1
        report.age_under_2 += instance.age_under_2
        report.age_under_3 += instance.age_under_3
        report.age_under_4 += instance.age_under_4
        report.age_under_5 += instance.age_under_5

        report.death_home += instance.death_home
        report.death_center += instance.death_center
        report.death_other += instance.death_other

        report.cause_death_fever += instance.cause_death_fever
        report.cause_death_diarrhea += instance.cause_death_diarrhea
        report.cause_death_dyspnea += instance.cause_death_dyspnea
        report.cause_death_anemia += instance.cause_death_anemia
        report.cause_death_rash += instance.cause_death_rash
        report.cause_death_cough += instance.cause_death_cough
        report.cause_death_vomiting += instance.cause_death_vomiting
        report.cause_death_nuchal_rigidity += \
                                           instance.cause_death_nuchal_rigidity
        report.cause_death_red_eye += instance.cause_death_red_eye
        report.cause_death_eat_refusal += instance.cause_death_eat_refusal
        report.cause_death_other += instance.cause_death_other

receiver(pre_save, sender=AggregatedChildrenMortalityReport)(pre_save_report)
receiver(post_save, sender=AggregatedChildrenMortalityReport)(post_save_report)

reversion.register(AggregatedChildrenMortalityReport)
