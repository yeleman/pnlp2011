#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import reversion
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from bolibana.models import Report, MonthPeriod
from bolibana.models.Report import ValidationMixin
from bolibana.tools.utils import generate_receipt


class FPMethodManager(models.Manager):

    def get_query_set(self):
        return super(FPMethodManager, self).get_query_set() \
                                           .filter(Q(male_condom=0) |
                                                   Q(female_condom=0) |
                                                   Q(oral_pills=0) |
                                                   Q(injectable=0) |
                                                   Q(iud=0) |
                                                   Q(implants=0) |
                                                   Q(female_sterilization=0) |
                                                   Q(male_sterilization=0))


class StockoutMixin(object):
    def has_stockouts(self):
        return self.filter(Q(male_condom=0) |
                           Q(female_condom=0) |
                           Q(oral_pills=0) |
                           Q(injectable=0) |
                           Q(iud=0) |
                           Q(implants=0) |
                           Q(female_sterilization=0) |
                           Q(male_sterilization=0))


class StockoutQuerySet(QuerySet, ValidationMixin, StockoutMixin):
    pass


class StockoutManager(models.Manager, ValidationMixin, StockoutMixin):
    def get_query_set(self):
        return StockoutQuerySet(self.model, using=self._db)


class RHCommoditiesReport(Report):

    """ Complies with bolibana.reporting.DataBrowser """

    YES = 'Y'
    NO = 'N'
    YESNO = ((YES, _(u"Yes")), (NO, _(u"No")))
    NOT_PROVIDED = -1
    SUPPLIES_AVAILABLE = 1
    SUPPLIES_NOT_AVAILABLE = 0
    SUPPLIES_NOT_PROVIDED = -1
    YESNOAVAIL = ((SUPPLIES_AVAILABLE, _(u"Yes. Supplies available")),
                  (SUPPLIES_NOT_AVAILABLE, _(u"Yes. Supplies not available")),
                  (SUPPLIES_NOT_PROVIDED, _(u"No")))

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _(u"RH Commodities Report")
        verbose_name_plural = _(u"RH Commodities Reports")
        unique_together = ('period', 'entity', 'type')

    # Services offered
    family_planning = models.BooleanField()
    delivery_services = models.BooleanField()

    # Modern contraceptive methods providded at the SDP
    male_condom = models.IntegerField(_(u"Male condom. Quantity in hand "
                                        u"(pieces) or -1."))
    female_condom = models.IntegerField(_(u"Female condom. Quantity in hand "
                                          u"(pieces) or -1."))
    oral_pills = models.IntegerField(_(u"Oral pills. Quantity in hand "
                                       u"(cycles) or -1."))
    injectable = models.IntegerField(_(u"Injectable. Quantity in hand "
                                       u"(vials) or -1."))
    iud = models.IntegerField(_(u"IUD. Quantity in hand "
                                u"(unit) or -1."))
    implants = models.IntegerField(_(u"Implants. Quantity in hand "
                                     u"(unit) or -1."))
    female_sterilization = models.IntegerField(verbose_name=_(u"Female"
                                               u"sterilization"),
                                               choices=YESNOAVAIL)
    male_sterilization = models.IntegerField(verbose_name=_(u"Male sterilization"),
                                             choices=YESNOAVAIL)

    # Availability of live-saving maternal/RH medecine
    amoxicillin_ij = models.IntegerField(_(u"Amoxicillin (Injectable). "
                                           u"Quantity in hand "
                                           u"(vials) or -1."))
    amoxicillin_cap_gel = models.IntegerField(_(u"Amoxicillin (capsule/gel). "
                                                u"Quantity in hand "
                                                u"(capsules) or -1."))
    amoxicillin_suspension = models.IntegerField(_(u"Amoxicillin (Suspension)."
                                                   u" Quantity in hand "
                                                   u"(vials) or -1."))
    azithromycine_tab = models.IntegerField(_(u"Azithromicine (tablet/gel). "
                                              u"Quantity in hand "
                                              u"(tablets) or -1."))
    azithromycine_suspension = models.IntegerField(_(u"Azithromicine "
                                                     u"(Suspension). "
                                                     u"Quantity in hand "
                                                     u"(bottles) or -1."))
    benzathine_penicillin = models.IntegerField(_(u"Benzatine penicillin. "
                                                  u"Quantity in hand "
                                                  u"(vials) or -1."))
    cefexime = models.IntegerField(_(u"Cefexime. "
                                     u"Quantity in hand "
                                     u"(tablets) or -1."))
    clotrimazole = models.IntegerField(_(u"Clotrimazole. "
                                         u"Quantity in hand "
                                         u"(tablets) or -1."))
    ergometrine_tab = models.IntegerField(_(u"Ergometrine (tablets). "
                                            u"Quantity in hand "
                                            u"(tablets) or -1."))
    ergometrine_vials = models.IntegerField(_(u"Ergometrine (vials). "
                                              u"Quantity in hand "
                                              u"(vials) or -1."))
    iron = models.IntegerField(_(u"Iron. "
                                 u"Quantity in hand "
                                 u"(tablets) or -1."))
    folate = models.IntegerField(_(u"Folate. "
                                   u"Quantity in hand "
                                   u"(tablets) or -1."))
    iron_folate = models.IntegerField(_(u"Iron/Folate. "
                                        u"Quantity in hand "
                                        u"(tablets) or -1."))
    magnesium_sulfate = models.IntegerField(_(u"Magnesium Sulfate. "
                                              u"Quantity in hand "
                                              u"(vials) or -1."))
    metronidazole = models.IntegerField(_(u"Metronidazole (injectable). "
                                          u"Quantity in hand "
                                          u"(vials) or -1."))
    oxytocine = models.IntegerField(_(u"Oxytocine. "
                                      u"Quantity in hand "
                                      u"(vials) or -1."))

    ceftriaxone_500 = models.IntegerField(_(u"Ceftriaxone 500mg. "
                                      u"Quantity in hand "
                                      u"(tablets) or -1."))

    ceftriaxone_1000 = models.IntegerField(_(u"Ceftriaxone 1g. "
                                      u"Quantity in hand "
                                      u"(tablets) or -1."))

    sources = models.ManyToManyField('RHCommoditiesReport', \
                                     verbose_name=_(u"Sources"), \
                                     blank=True, null=True)

    objects = StockoutManager()
    fp_stockout = FPMethodManager()

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
        return generate_receipt(instance, fix='P', add_random=True)

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

        sources = RHCommoditiesReport.validated\
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

    def fp_stockout_3methods(self):
        w = 0
        for f in ('male_condom', 'female_condom', 'oral_pills', 'injectable',
                  'iud', 'implants',
                  'female_sterilization', 'male_sterilization'):
            if getattr(self, f) == 0:
                w += 1
        return w >= 3


@receiver(pre_save, sender=RHCommoditiesReport)
def pre_save_report(sender, instance, **kwargs):
    """ change _status property of Report on save() at creation """
    if instance._status == instance.STATUS_UNSAVED:
        instance._status = instance.STATUS_CLOSED
    # following will allow us to detect failure in registration
    if not instance.receipt:
        instance.receipt = 'NO_RECEIPT'


@receiver(post_save, sender=RHCommoditiesReport)
def post_save_report(sender, instance, **kwargs):
    """ generates the receipt """
    if instance.receipt == 'NO_RECEIPT':
        instance.receipt = sender.generate_receipt(instance)
        instance.save()

reversion.register(RHCommoditiesReport)
