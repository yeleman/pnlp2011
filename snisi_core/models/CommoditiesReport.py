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

from bolibana.models.Period import MonthPeriod
from bolibana.models.Report import ValidationMixin
from bolibana.tools.utils import generate_receipt

from common import (pre_save_report, post_save_report, report_create_from,
                    aggregated_model_report_pre_save)
from SNISIReport import SNISIReport


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


class RHProductsR(SNISIReport):

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
    male_sterilization = models.IntegerField(\
                                        verbose_name=_(u"Male sterilization"),
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

    is_late = models.BooleanField(default=False,
                                  verbose_name=_(u"Is Late?"))

    objects = StockoutManager()
    fp_stockout = FPMethodManager()

    def add_data(self, family_planning,
                       delivery_services,
                       male_condom,
                       female_condom,
                       oral_pills,
                       injectable,
                       iud,
                       implants,
                       female_sterilization,
                       male_sterilization,
                       amoxicillin_ij,
                       amoxicillin_cap_gel,
                       amoxicillin_suspension,
                       azithromycine_tab,
                       azithromycine_suspension,
                       benzathine_penicillin,
                       cefexime,
                       clotrimazole,
                       ergometrine_tab,
                       ergometrine_vials,
                       iron,
                       folate,
                       iron_folate,
                       magnesium_sulfate,
                       metronidazole,
                       oxytocine,
                       ceftriaxone_500,
                       ceftriaxone_1000):
        self.family_planning = family_planning
        self.delivery_services = delivery_services
        self.male_condom = male_condom
        self.female_condom = female_condom
        self.oral_pills = oral_pills
        self.injectable = injectable
        self.iud = iud
        self.implants = implants
        self.female_sterilization = female_sterilization
        self.male_sterilization = male_sterilization
        self.amoxicillin_ij = amoxicillin_ij
        self.amoxicillin_cap_gel = amoxicillin_cap_gel
        self.amoxicillin_suspension = amoxicillin_suspension
        self.azithromycine_tab = azithromycine_tab
        self.azithromycine_suspension = azithromycine_suspension
        self.benzathine_penicillin = benzathine_penicillin
        self.cefexime = cefexime
        self.clotrimazole = clotrimazole
        self.ergometrine_tab = ergometrine_tab
        self.ergometrine_vials = ergometrine_vials
        self.iron = iron
        self.folate = folate
        self.iron_folate = iron_folate
        self.magnesium_sulfate = magnesium_sulfate
        self.metronidazole = metronidazole
        self.oxytocine = oxytocine
        self.ceftriaxone_500 = ceftriaxone_500
        self.ceftriaxone_1000 = ceftriaxone_1000

    @property
    def mperiod(self):
        """ casted period to MonthPeriod """
        mp = self.period
        mp.__class__ = MonthPeriod
        return mp

    @classmethod
    def start(cls, period, entity, author,
               type=SNISIReport.TYPE_SOURCE, is_late=False, *args, **kwargs):
        """ creates a report object with meta data only. Object not saved """
        report = cls(period=period, entity=entity, created_by=author,
                     modified_by=author, _status=cls.STATUS_CREATED,
                     type=type)
        report.is_late = is_late
        for arg, value in kwargs.items():
            try:
                setattr(report, arg, value)
            except AttributeError:
                pass

        return report

    @classmethod
    def data_fields(cls):
        return ['family_planning',
                'delivery_services',
                'male_condom',
                'female_condom',
                'oral_pills',
                'injectable',
                'iud',
                'implants',
                'female_sterilization',
                'male_sterilization',
                'amoxicillin_ij',
                'amoxicillin_cap_gel',
                'amoxicillin_suspension',
                'azithromycine_tab',
                'azithromycine_suspension',
                'benzathine_penicillin',
                'cefexime',
                'clotrimazole',
                'ergometrine_tab',
                'ergometrine_vials',
                'iron',
                'folate',
                'iron_folate',
                'magnesium_sulfate',
                'metronidazole',
                'oxytocine',
                'ceftriaxone_500',
                'ceftriaxone_1000',
                'is_late']

    def to_dict(self):
        d = {}
        for field in self.data_fields():
            d[field] = getattr(self, field)
        return d

    @classmethod
    def generate_receipt(cls, instance):
        return generate_receipt(instance, fix='-P', add_random=True)

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
        return AggRHProductsR.create_from(period, entity,
                                          author, *args, **kwargs)

    def fp_stockout_3methods(self):
        w = 0
        for f in ('male_condom', 'female_condom', 'oral_pills', 'injectable',
                  'iud', 'implants',
                  'female_sterilization', 'male_sterilization'):
            if getattr(self, f) == 0:
                w += 1
        return w >= 3

receiver(pre_save, sender=RHProductsR)(pre_save_report)
receiver(post_save, sender=RHProductsR)(post_save_report)

reversion.register(RHProductsR)


class AggRHProductsR(SNISIReport):

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _(u"Aggregated RH Commodities Report")
        verbose_name_plural = _(u"Aggregated RH Commodities Reports")
        unique_together = ('period', 'entity', 'type')

    # Services offered
    family_planning_provided = models.PositiveIntegerField()
    delivery_services_provided = models.PositiveIntegerField()

    # Modern contraceptive methods providded at the SDP
    male_condom_provided = models.PositiveIntegerField()
    male_condom_available = models.PositiveIntegerField()
    female_condom_provided = models.PositiveIntegerField()
    female_condom_available = models.PositiveIntegerField()
    oral_pills_provided = models.PositiveIntegerField()
    oral_pills_available = models.PositiveIntegerField()
    injectable_provided = models.PositiveIntegerField()
    injectable_available = models.PositiveIntegerField()
    iud_provided = models.PositiveIntegerField()
    iud_available = models.PositiveIntegerField()
    implants_provided = models.PositiveIntegerField()
    implants_available = models.PositiveIntegerField()

    female_sterilization_available = models.PositiveIntegerField()
    female_sterilization_provided = models.PositiveIntegerField()

    male_sterilization_available = models.PositiveIntegerField()
    male_sterilization_provided = models.PositiveIntegerField()

    # Availability of live-saving maternal/RH medecine
    amoxicillin_ij_provided = models.PositiveIntegerField()
    amoxicillin_ij_available = models.PositiveIntegerField()
    amoxicillin_cap_gel_provided = models.PositiveIntegerField()
    amoxicillin_cap_gel_available = models.PositiveIntegerField()
    amoxicillin_suspension_provided = models.PositiveIntegerField()
    amoxicillin_suspension_available = models.PositiveIntegerField()
    azithromycine_tab_provided = models.PositiveIntegerField()
    azithromycine_tab_available = models.PositiveIntegerField()
    azithromycine_suspension_provided = models.PositiveIntegerField()
    azithromycine_suspension_available = models.PositiveIntegerField()
    benzathine_penicillin_provided = models.PositiveIntegerField()
    benzathine_penicillin_available = models.PositiveIntegerField()
    cefexime_provided = models.PositiveIntegerField()
    cefexime_available = models.PositiveIntegerField()
    clotrimazole_provided = models.PositiveIntegerField()
    clotrimazole_available = models.PositiveIntegerField()
    ergometrine_tab_provided = models.PositiveIntegerField()
    ergometrine_tab_available = models.PositiveIntegerField()
    ergometrine_vials_provided = models.PositiveIntegerField()
    ergometrine_vials_available = models.PositiveIntegerField()
    iron_provided = models.PositiveIntegerField()
    iron_available = models.PositiveIntegerField()
    folate_provided = models.PositiveIntegerField()
    folate_available = models.PositiveIntegerField()
    iron_folate_provided = models.PositiveIntegerField()
    iron_folate_available = models.PositiveIntegerField()
    magnesium_sulfate_provided = models.PositiveIntegerField()
    magnesium_sulfate_available = models.PositiveIntegerField()
    metronidazole_provided = models.PositiveIntegerField()
    metronidazole_available = models.PositiveIntegerField()
    oxytocine_provided = models.PositiveIntegerField()
    oxytocine_available = models.PositiveIntegerField()

    ceftriaxone_500_provided = models.PositiveIntegerField()
    ceftriaxone_500_available = models.PositiveIntegerField()
    ceftriaxone_1000_provided = models.PositiveIntegerField()
    ceftriaxone_1000_available = models.PositiveIntegerField()

    nb_prompt = models.PositiveIntegerField()

    indiv_sources = models.ManyToManyField('RHProductsR',
                                           verbose_name=_(u"Indiv. Sources"),
                                           blank=True, null=True,
                                           related_name='indiv_agg_rhcommodities_reports')

    agg_sources = models.ManyToManyField('AggRHProductsR',
                                         verbose_name=_(u"Aggr. Sources"),
                                         blank=True, null=True,
                                         related_name='aggregated_agg_rhcommodities_reports')

    @property
    def mperiod(self):
        """ casted period to MonthPeriod """
        mp = self.period
        mp.__class__ = MonthPeriod
        return mp

    @classmethod
    def start(cls, period, entity, author,
              type=SNISIReport.TYPE_AGGREGATED, *args, **kwargs):
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

    @classmethod
    def data_fields(cls):
        return ['family_planning_provided',
                'delivery_services_provided',
                'male_condom_provided',
                'male_condom_available',
                'female_condom_provided',
                'female_condom_available',
                'oral_pills_provided',
                'oral_pills_available',
                'injectable_provided',
                'injectable_available',
                'iud_provided',
                'iud_available',
                'implants_provided',
                'implants_available',
                'female_sterilization_available',
                'female_sterilization_provided',
                'male_sterilization_available',
                'male_sterilization_provided',
                'amoxicillin_ij_provided',
                'amoxicillin_ij_available',
                'amoxicillin_cap_gel_provided',
                'amoxicillin_cap_gel_available',
                'amoxicillin_suspension_provided',
                'amoxicillin_suspension_available',
                'azithromycine_tab_provided',
                'azithromycine_tab_available',
                'azithromycine_suspension_provided',
                'azithromycine_suspension_available',
                'benzathine_penicillin_provided',
                'benzathine_penicillin_available',
                'cefexime_provided',
                'cefexime_available',
                'clotrimazole_provided',
                'clotrimazole_available',
                'ergometrine_tab_provided',
                'ergometrine_tab_available',
                'ergometrine_vials_provided',
                'ergometrine_vials_available',
                'iron_provided',
                'iron_available',
                'folate_provided',
                'folate_available',
                'iron_folate_provided',
                'iron_folate_available',
                'magnesium_sulfate_provided',
                'magnesium_sulfate_available',
                'metronidazole_provided',
                'metronidazole_available',
                'oxytocine_provided',
                'oxytocine_available',
                'ceftriaxone_500_provided',
                'ceftriaxone_500_available',
                'ceftriaxone_1000_provided',
                'ceftriaxone_1000_available',
                'nb_prompt']

    def to_dict(self):
        d = {}
        for field in self.data_fields():
            d[field] = getattr(self, field)
        return d

    @classmethod
    def generate_receipt(cls, instance):
        return generate_receipt(instance, fix='-AP', add_random=True)

    def get(self, slug):
        """ [data browser] returns data for a slug variable """
        return getattr(self, slug)

    def field_name(self, slug):
        """ [data browser] returns name of field for a slug variable """
        return self._meta.get_field(slug).verbose_name

    def validate(self):
        return {}

    @classmethod
    def create_from(cls, period, entity, author):
        return report_create_from(cls, period, entity,
                                  author, indiv_cls=RHProductsR)

    @classmethod
    def update_instance_with_indiv(cls, report, instance):

        for field in instance.data_fields():
            if field in ('family_planning', 'delivery_services'):
                if getattr(instance, field):
                    agg_field = u'%s_provided' % field
                    setattr(report, agg_field,
                            getattr(report, agg_field, 0) + 1)
            elif field in ('female_sterilization', 'male_sterilization'):

                if getattr(instance, field, instance.SUPPLIES_NOT_PROVIDED) \
                    in (instance.SUPPLIES_AVAILABLE,
                        instance.SUPPLIES_NOT_AVAILABLE):

                    prov_field = u'%s_provided' % field
                    setattr(report, prov_field,
                            getattr(report, prov_field, 0) + 1)

                    if getattr(instance, field,
                               instance.SUPPLIES_NOT_PROVIDED) == \
                        instance.SUPPLIES_AVAILABLE:

                        avail_field = u'%s_available' % field
                        setattr(report, avail_field,
                            getattr(report, avail_field, 0) + 1)
            elif field == 'is_late':
                prompt_field = 'nb_prompt'
                if not getattr(instance, field):
                    setattr(report, prompt_field,
                    getattr(report, prompt_field, 0) + 1)
            else:
                if getattr(instance, field, instance.NOT_PROVIDED) != \
                    instance.NOT_PROVIDED:

                    prov_field = u'%s_provided' % field
                    setattr(report, prov_field,
                            getattr(report, prov_field, 0) + 1)

                    if getattr(instance, field, instance.NOT_PROVIDED) > 0:
                        avail_field = u'%s_available' % field
                        setattr(report, avail_field,
                            getattr(report, avail_field, 0) + 1)

    @classmethod
    def update_instance_with_agg(cls, report, instance):

        for field in cls.data_fields():
            setattr(report, field,
                    getattr(report, field, 0) + getattr(instance, field, 0))


receiver(pre_save, sender=AggRHProductsR)(pre_save_report)
receiver(pre_save,
         sender=AggRHProductsR)(aggregated_model_report_pre_save)
receiver(post_save, sender=AggRHProductsR)(post_save_report)

reversion.register(AggRHProductsR)
