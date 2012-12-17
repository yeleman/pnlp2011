#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import reversion
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from bolibana.models import Report, MonthPeriod
from bolibana.tools.utils import generate_receipt


class ProvidedServicesReport(Report):

    """ Complies with bolibana.reporting.DataBrowser """

    class Meta:
        app_label = 'credos_core'
        verbose_name = _(u"Provided Services Report")
        verbose_name_plural = _(u"Provided Services Reports")
        unique_together = ('period', 'entity', 'type')

    # services providing CAP
    iud = models.PositiveIntegerField(_(u"IUD"))
    injectable = models.PositiveIntegerField(_(u"Injectable"))
    oral_pills = models.PositiveIntegerField(_(u"Oral Pills"))
    male_condom = models.PositiveIntegerField(_(u"Male Condom"))
    female_condom = models.PositiveIntegerField(_(u"Female Condom"))
    emergency_contraception = models.PositiveIntegerField(_(u"emergency "
                                                            u"Contraception"))
    implant = models.PositiveIntegerField(_(u"Implant"))

    # services not providing CAP
    new_client = models.PositiveIntegerField(_(u"New Clients"))
    returning_client = models.PositiveIntegerField(_(u"Returning Clients"))
    pf_visit_u25 = models.PositiveIntegerField(_(u"Visits from aged 24 max."))
    pf_visit_o25 = models.PositiveIntegerField(_(u"Visits from aged 25+."))
    pf_first_time = models.PositiveIntegerField(_(u"Clients using PF for the "
                                                  u"first time"))
    pf_visit_ams_ticket = models.PositiveIntegerField(_(u"Visits by "
                                                        u"AMS ticket"))
    pf_visit_provider_ticket = models.PositiveIntegerField(_(u"Visits by "
                                                           u"provider ticket"))
    pf_visit_short_term = models.PositiveIntegerField(_(u"Visit for short term"
                                                        u"PF method"))
    pf_visit_long_term = models.PositiveIntegerField(_(u"Visit for long term"
                                                        u"PF method"))
    client_hiv_counselling = models.PositiveIntegerField(_(u"Client receving"
                                                           u"HIV Counselling"))
    client_hiv_tested = models.PositiveIntegerField(_(u"Client tested"
                                                      u" for HIV"))
    client_hiv_positive = models.PositiveIntegerField(_(u"HIV+ Client tested"))

    implant_removal = models.PositiveIntegerField(_(u"5y implant removal"))
    iud_removal = models.PositiveIntegerField(_(u"IUD removal"))

    total_hiv_test = models.PositiveIntegerField(_(u"Total HIV tests"))

    sources = models.ManyToManyField('ProvidedServicesReport',
                                     verbose_name=_(u"Sources"), \
                                     blank=True, null=True)

    @property
    def mperiod(self):
        """ casted period to MonthPeriod """
        mp = self.period
        mp.__class__ = MonthPeriod
        return mp

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
        return generate_receipt(instance, fix='PS', add_random=True)

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
        agg_report = cls.start(period, entity, author, \
               type=Report.TYPE_AGGREGATED, *args, **kwargs)

        sources = ProvidedServicesReport.validated.filter(period=period, \
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


@receiver(pre_save, sender=ProvidedServicesReport)
def pre_save_report(sender, instance, **kwargs):
    """ change _status property of Report on save() at creation """
    if instance._status == instance.STATUS_UNSAVED:
        instance._status = instance.STATUS_CLOSED
    # following will allow us to detect failure in registration
    if not instance.receipt:
        instance.receipt = 'NO_RECEIPT'


@receiver(post_save, sender=ProvidedServicesReport)
def post_save_report(sender, instance, **kwargs):
    """ generates the receipt """
    if instance.receipt == 'NO_RECEIPT':
        instance.receipt = sender.generate_receipt(instance)
        instance.save()

reversion.register(ProvidedServicesReport)
