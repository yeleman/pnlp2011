#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad

import reversion
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils.translation import ugettext_lazy as _, ugettext


from bolibana.models import Report, WeekPeriod, EntityType


class EpidemiologyReport(Report):

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _(u"Epidemiology Report")
        verbose_name_plural = _(u"Epidemiology Reports")

    acute_flaccid_paralysis_case = models.IntegerField(_(u"PFA cas"))
    acute_flaccid_paralysis_death = models.IntegerField(_(u"PFA décès"))

    influenza_a_h1n1_case = models.IntegerField(_(u"Grippe A H1N1"))
    influenza_a_h1n1_death = models.IntegerField(_(u"Grippe A H1N1"))

    cholera_case = models.IntegerField(_(u"Choléra cas"))
    cholera_death = models.IntegerField(_(u"Choléra décès"))

    red_diarrhea_case = models.IntegerField(_(u"Diarrhée rouge cas décès"))
    red_diarrhea_death = models.IntegerField(_(u"Diarrhée rouge cas décès"))

    measles_case = models.IntegerField(_(u"Rougeole cas décès"))
    measles_death = models.IntegerField(_(u"Rougeole cas décès"))

    yellow_fever_case = models.IntegerField(_(u"Fievere jaune cas"))
    yellow_fever_death = models.IntegerField(_(u"Fievere jaune décès"))

    neonatal_tetanus_case = models.IntegerField(_(u"TNN cas"))
    neonatal_tetanus_death = models.IntegerField(_(u"TNN décès"))

    meningitis_case = models.IntegerField(_(u"Meningite cas"))
    meningitis_death = models.IntegerField(_(u"Meningite décès"))

    rabies_case = models.IntegerField(_(u"Rage cas"))
    rabies_death = models.IntegerField(_(u"Rage décès"))

    acute_measles_diarrhea_case = models.IntegerField(_(u"Diarrhée severe rougeole cas"))
    acute_measles_diarrhea_death = models.IntegerField(_(u"Diarrhée severe rougeole décès"))

    other_notifiable_disease_case = models.IntegerField(_(u"Autres MADOS cas"))
    other_notifiable_disease_death = models.IntegerField(_(u"Autres MADOS décès"))

    @property
    def mperiod(self):
        """ casted period to MonthPeriod """
        wp = self.period
        wp.__class__ = WeekPeriod
        return wp

    def __unicode__(self):
        return ugettext(u"%(cscom)s / %(period)s / %(receipt)s"
            % {'cscom': self.entity.display_full_name(),
               'period': self.period,
               'receipt': self.receipt})

    @classmethod
    def start(cls, period, entity, author, \
               type=Report.TYPE_SOURCE, *args, **kwargs):
        """ creates a report object with meta data only. Object not saved """
        report = cls(period=period, entity=entity, created_by=author, \
                     modified_by=author, _status=cls.STATUS_CREATED, \
                     type=type)
        for arg, value in kwargs.items():
            try:
                setattr(report, arg, value)
            except AttributeError:
                pass

        return report

    def fill_blank(self):
        pass

    def to_dict(self):
        d = {}
        return d

    @classmethod
    def generate_receipt(cls, instance):
        """ generates a reversable text receipt for a MalariaReport

        FORMAT:
            RR000/sss-111-D
            RR: region code on two letters
            000: internal report ID
            sss: entity slug
            111: sent day in year
            D: sent day of week """

        DOW = ['D', 'L', 'M', 'E', 'J', 'V', 'S']
        region_type = EntityType.objects.get(slug='region')

        def region_id(slug):
            return slug.upper()[0:2]

        region = 'ML'
        for ent in instance.entity.get_ancestors().reverse():
            if ent.type == region_type:
                region = region_id(ent.slug)
                break
        receipt = '%(region)s%(id)d/%(entity)s-%(day)s-%(dow)s' \
                  % {'day': instance.created_on.strftime('%j'), \
                     'dow': DOW[int(instance.created_on.strftime('%w'))], \
                     'entity': instance.entity.slug, \
                     'id': instance.id, \
                     'period': instance.period.id, \
                     'region': region}
        return receipt

    def get(self, slug):
        """ [data browser] returns data for a slug variable """
        return getattr(self, slug)

    def field_name(self, slug):
        """ [data browser] returns name of field for a slug variable """
        return self._meta.get_field(slug).verbose_name

    def validate(self):
        return {}

    @classmethod
    def create_aggregated(cls, period, entity, author, *args, **kwargs):
        agg_report = cls.start(period, entity, author,
                               type=Report.TYPE_AGGREGATED, *args, **kwargs)

        sources = EpidemiologyReport.validated\
                                     .filter(period=period,
                                             entity__in=entity.get_children())

        if sources.count() == 0:
            agg_report.fill_blank()
            agg_report.save()

        for report in sources:
            for key, value in report.to_dict().items():
                pv = getattr(agg_report, key)
                if not pv:
                    nv = value
                elif pv in (cls.YES, cls.NO):
                    if pv == cls.YES:
                        nv = pv
                    else:
                        nv = value
                else:
                    nv = pv + value
                setattr(agg_report, key, nv)
            agg_report.save()

        for report in sources:
            agg_report.sources.add(report)

        with reversion.create_revision():
            agg_report.save()
            reversion.set_user(author.user)

        return agg_report


@receiver(pre_save, sender=EpidemiologyReport)
def pre_save_report(sender, instance, **kwargs):
    """ change _status property of Report on save() at creation """
    if instance._status == instance.STATUS_UNSAVED:
        instance._status = instance.STATUS_CLOSED
    # following will allow us to detect failure in registration
    if not instance.receipt:
        instance.receipt = 'NO_RECEIPT'


@receiver(post_save, sender=EpidemiologyReport)
def post_save_report(sender, instance, **kwargs):
    """ generates the receipt """
    if instance.receipt == 'NO_RECEIPT':
        instance.receipt = sender.generate_receipt(instance)
        instance.save()

reversion.register(EpidemiologyReport)
