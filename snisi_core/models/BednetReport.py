#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad

import reversion
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils.translation import ugettext_lazy as _, ugettext

from bolibana.models.Period import WeekPeriod
from bolibana.tools.utils import generate_receipt

from common import pre_save_report, post_save_report
from SNISIReport import SNISIReport


class BednetR(SNISIReport):

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _(u"MILD Report")
        verbose_name_plural = _(u"MILD Reports")

    initial_mild = models.IntegerField(_(u"Initial"))
    received_mild = models.IntegerField(_(u"Reçues"))

    distributed_mild = models.IntegerField(_(u"Distribuées"))
    remaining_mild = models.IntegerField(_(u"Restantes"))

    difference_mild = models.IntegerField(_(u"Différence"))

    sources = models.ManyToManyField('self',
                                     verbose_name=_(u"Sources"),
                                     blank=True, null=True)

    def add_data(self, initial_mild,
                 received_mild,
                 distributed_mild,
                 remaining_mild,
                 difference_mild):
        self.initial_mild = initial_mild
        self.received_mild = received_mild
        self.distributed_mild = distributed_mild
        self.remaining_mild = remaining_mild
        self.difference_mild = difference_mild

    @property
    def wperiod(self):
        """ casted period to WeekPeriod """
        wp = self.period
        wp.__class__ = WeekPeriod
        return wp

    def __unicode__(self):
        return ugettext(u"%(cscom)s / %(period)s / %(receipt)s"
                        % {'cscom': self.entity.display_full_name(),
                           'period': self.period,
                           'receipt': self.receipt})

    @classmethod
    def start(cls, period, entity, author,
              type=SNISIReport.TYPE_SOURCE, *args, **kwargs):
        """ creates a report object with meta data only. Object not saved """
        report = cls(period=period, entity=entity, created_by=author,
                     modified_by=author, _status=cls.STATUS_CREATED,
                     type=type)
        for arg, value in kwargs.items():
            try:
                setattr(report, arg, value)
            except AttributeError:
                pass

        return report

    def fill_blank(self):
        for field in self.to_dict().keys():
            setattr(self, field, 0)

    def to_dict(self):
        d = {}
        for field in self._meta.get_all_field_names():
            d[field] = getattr(self, field)
        return d

    @classmethod
    def generate_receipt(cls, instance):
        return generate_receipt(instance, fix='-B', add_random=True)

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
                               type=SNISIReport.TYPE_AGGREGATED,
                               *args, **kwargs)

        sources = BednetR.validated.filter(period=period,
                                           entity__in=entity.get_children())

        if sources.count() == 0:
            agg_report.fill_blank()
            agg_report.save()

        for report in sources:
            for key, value in report.to_dict().items():
                pv = getattr(agg_report, key)
                if not pv:
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


receiver(pre_save, sender=BednetR)(pre_save_report)
receiver(post_save, sender=BednetR)(post_save_report)

reversion.register(BednetR)
