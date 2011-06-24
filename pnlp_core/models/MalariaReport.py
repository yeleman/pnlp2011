#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import reversion
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib import admin
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _, ugettext

from bolibana_reporting.models import EntityType, Entity, Report


class MalariaReport(Report):

    """ Complies with bolibana_reporting.DataBrowser """

    YES = 1
    NO = 0
    YESNO = ((YES, _(u"Yes")), (NO, _(u"No")))

    class Meta:
        app_label = 'pnlp_core'
        verbose_name = _(u"Malaria Report")
        verbose_name_plural = _(u"Malaria Reports")

    u5_total_consultation_all_causes = models.PositiveIntegerField( \
                                           _(u"Total Consultation All Causes"))
    u5_total_suspected_malaria_cases = models.PositiveIntegerField( \
                                           _(u"Total Suspected Malaria Cases"))
    u5_total_simple_malaria_cases = models.PositiveIntegerField( \
                                              _(u"Total Simple Malaria Cases"))
    u5_total_severe_malaria_cases = models.PositiveIntegerField( \
                                              _(u"Total Severe Malaria Cases"))
    u5_total_tested_malaria_cases = models.PositiveIntegerField( \
                                              _(u"Total Tested Malaria Cases"))
    u5_total_confirmed_malaria_cases = models.PositiveIntegerField( \
                                           _(u"Total Confirmed Malaria Cases"))
    u5_total_treated_malaria_cases = models.PositiveIntegerField( \
                                             _(u"Total Treated Malaria Cases"))
    u5_total_inpatient_all_causes = models.PositiveIntegerField( \
                                              _(u"Total Inpatient All Causes"))
    u5_total_malaria_inpatient = models.PositiveIntegerField( \
                                                 _(u"Total Malaria Inpatient"))
    u5_total_death_all_causes = models.PositiveIntegerField( \
                                                  _(u"Total Death All Causes"))
    u5_total_malaria_death = models.PositiveIntegerField( \
                                                     _(u"Total Malaria Death"))
    u5_total_distributed_bednets = models.PositiveIntegerField( \
                                               _(u"Total Distributed Bednets"))

    o5_total_consultation_all_causes = models.PositiveIntegerField( \
                                           _(u"Total Consultation All Causes"))
    o5_total_suspected_malaria_cases = models.PositiveIntegerField( \
                                           _(u"Total Suspected Malaria Cases"))
    o5_total_simple_malaria_cases = models.PositiveIntegerField( \
                                              _(u"Total Simple Malaria Cases"))
    o5_total_severe_malaria_cases = models.PositiveIntegerField( \
                                              _(u"Total Severe Malaria Cases"))
    o5_total_tested_malaria_cases = models.PositiveIntegerField( \
                                              _(u"Total Tested Malaria Cases"))
    o5_total_confirmed_malaria_cases = models.PositiveIntegerField( \
                                           _(u"Total Confirmed Malaria Cases"))
    o5_total_treated_malaria_cases = models.PositiveIntegerField( \
                                             _(u"Total Treated Malaria Cases"))
    o5_total_inpatient_all_causes = models.PositiveIntegerField( \
                                              _(u"Total Inpatient All Causes"))
    o5_total_malaria_inpatient = models.PositiveIntegerField( \
                                                 _(u"Total Malaria Inpatient"))
    o5_total_death_all_causes = models.PositiveIntegerField( \
                                                  _(u"Total Death All Causes"))
    o5_total_malaria_death = models.PositiveIntegerField( \
                                                     _(u"Total Malaria Death"))

    pw_total_consultation_all_causes = models.PositiveIntegerField( \
                                           _(u"Total Consultation All Causes"))
    pw_total_suspected_malaria_cases = models.PositiveIntegerField( \
                                           _(u"Total Suspected Malaria Cases"))
    pw_total_severe_malaria_cases = models.PositiveIntegerField( \
                                              _(u"Total Severe Malaria Cases"))
    pw_total_tested_malaria_cases = models.PositiveIntegerField( \
                                              _(u"Total Tested Malaria Cases"))
    pw_total_confirmed_malaria_cases = models.PositiveIntegerField( \
                                           _(u"Total Confirmed Malaria Cases"))
    pw_total_treated_malaria_cases = models.PositiveIntegerField( \
                                             _(u"Total Treated Malaria Cases"))
    pw_total_inpatient_all_causes = models.PositiveIntegerField( \
                                              _(u"Total Inpatient All Causes"))
    pw_total_malaria_inpatient = models.PositiveIntegerField( \
                                                 _(u"Total Malaria Inpatient"))
    pw_total_death_all_causes = models.PositiveIntegerField( \
                                                  _(u"Total Death All Causes"))
    pw_total_malaria_death = models.PositiveIntegerField( \
                                                     _(u"Total Malaria Death"))
    pw_total_distributed_bednets = models.PositiveIntegerField( \
                                               _(u"Total Distributed Bednets"))
    pw_total_anc1 = models.PositiveIntegerField(_(u"Total ANC1 Visits"))
    pw_total_sp1 = models.PositiveIntegerField(_(u"Total SP1 given"))
    pw_total_sp2 = models.PositiveIntegerField(_(u"Total SP2 given"))

    stockout_act_children = models.CharField(_(u"ACT Children"), \
                                             max_length=1, choices=YESNO)
    stockout_act_youth = models.CharField(_(u"ACT Youth"), \
                                          max_length=1, choices=YESNO)
    stockout_act_adult = models.CharField(_(u"ACT Adult"), \
                                          max_length=1, choices=YESNO)
    stockout_arthemeter = models.CharField(_(u"Arthemeter"), \
                                           max_length=1, choices=YESNO)
    stockout_quinine = models.CharField(_(u"Quinine"), \
                                        max_length=1, choices=YESNO)
    stockout_serum = models.CharField(_(u"Serum"), max_length=1, choices=YESNO)
    stockout_bednet = models.CharField(_(u"Bednets"), \
                                       max_length=1, choices=YESNO)
    stockout_rdt = models.CharField(_(u"RDTs"), max_length=1, choices=YESNO)
    stockout_sp = models.CharField(_(u"SPs"), max_length=1, choices=YESNO)

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

    def add_underfive_data(self, total_consultation_all_causes, \
                                 total_suspected_malaria_cases, \
                                 total_simple_malaria_cases, \
                                 total_severe_malaria_cases, \
                                 total_tested_malaria_cases, \
                                 total_confirmed_malaria_cases, \
                                 total_treated_malaria_cases, \
                                 total_inpatient_all_causes, \
                                 total_malaria_inpatient, \
                                 total_death_all_causes, \
                                 total_malaria_death, \
                                 total_distributed_bednets):
        self.u5_total_consultation_all_causes = total_consultation_all_causes
        self.u5_total_suspected_malaria_cases = total_suspected_malaria_cases
        self.u5_total_simple_malaria_cases = total_simple_malaria_cases
        self.u5_total_severe_malaria_cases = total_severe_malaria_cases
        self.u5_total_tested_malaria_cases = total_tested_malaria_cases
        self.u5_total_confirmed_malaria_cases = total_confirmed_malaria_cases
        self.u5_total_treated_malaria_cases = total_treated_malaria_cases
        self.u5_total_inpatient_all_causes = total_inpatient_all_causes
        self.u5_total_malaria_inpatient = total_malaria_inpatient
        self.u5_total_death_all_causes = total_death_all_causes
        self.u5_total_malaria_death = total_malaria_death
        self.u5_total_distributed_bednets = total_distributed_bednets

    def add_overfive_data(self, total_consultation_all_causes, \
                                 total_suspected_malaria_cases, \
                                 total_simple_malaria_cases, \
                                 total_severe_malaria_cases, \
                                 total_tested_malaria_cases, \
                                 total_confirmed_malaria_cases, \
                                 total_treated_malaria_cases, \
                                 total_inpatient_all_causes, \
                                 total_malaria_inpatient, \
                                 total_death_all_causes, \
                                 total_malaria_death):
        self.o5_total_consultation_all_causes = total_consultation_all_causes
        self.o5_total_suspected_malaria_cases = total_suspected_malaria_cases
        self.o5_total_simple_malaria_cases = total_simple_malaria_cases
        self.o5_total_severe_malaria_cases = total_severe_malaria_cases
        self.o5_total_tested_malaria_cases = total_tested_malaria_cases
        self.o5_total_confirmed_malaria_cases = total_confirmed_malaria_cases
        self.o5_total_treated_malaria_cases = total_treated_malaria_cases
        self.o5_total_inpatient_all_causes = total_inpatient_all_causes
        self.o5_total_malaria_inpatient = total_malaria_inpatient
        self.o5_total_death_all_causes = total_death_all_causes
        self.o5_total_malaria_death = total_malaria_death

    def add_pregnantwomen_data(self, total_consultation_all_causes, \
                                 total_suspected_malaria_cases, \
                                 total_severe_malaria_cases, \
                                 total_tested_malaria_cases, \
                                 total_confirmed_malaria_cases, \
                                 total_treated_malaria_cases, \
                                 total_inpatient_all_causes, \
                                 total_malaria_inpatient, \
                                 total_death_all_causes, \
                                 total_malaria_death, \
                                 total_distributed_bednets, \
                                 total_anc1, \
                                 total_sp1, \
                                 total_sp2):
        self.pw_total_consultation_all_causes = total_consultation_all_causes
        self.pw_total_suspected_malaria_cases = total_suspected_malaria_cases
        self.pw_total_severe_malaria_cases = total_severe_malaria_cases
        self.pw_total_tested_malaria_cases = total_tested_malaria_cases
        self.pw_total_confirmed_malaria_cases = total_confirmed_malaria_cases
        self.pw_total_treated_malaria_cases = total_treated_malaria_cases
        self.pw_total_inpatient_all_causes = total_inpatient_all_causes
        self.pw_total_malaria_inpatient = total_malaria_inpatient
        self.pw_total_death_all_causes = total_death_all_causes
        self.pw_total_malaria_death = total_malaria_death
        self.pw_total_distributed_bednets = total_distributed_bednets
        self.pw_total_anc1 = total_anc1
        self.pw_total_sp1 = total_sp1
        self.pw_total_sp2 = total_sp2

    def add_stockout_data(self, stockout_act_children, \
                                stockout_act_youth, \
                                stockout_act_adult, \
                                stockout_arthemeter, \
                                stockout_quinine, \
                                stockout_serum, \
                                stockout_bednet, \
                                stockout_rdt, \
                                stockout_sp):
        self.stockout_act_children = stockout_act_children
        self.stockout_act_youth = stockout_act_youth
        self.stockout_act_adult = stockout_act_adult
        self.stockout_arthemeter = stockout_arthemeter
        self.stockout_quinine = stockout_quinine
        self.stockout_serum = stockout_serum
        self.stockout_bednet = stockout_bednet
        self.stockout_rdt = stockout_rdt
        self.stockout_sp = stockout_sp

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
        """ runs MalariaReportValidator """
        validator = MalariaReportValidator(self)
        validator.validate()
        return validator.errors


@receiver(pre_save, sender=MalariaReport)
def pre_save_report(sender, instance, **kwargs):
    """ change _status property of Report on save() at creation """
    if instance._status == instance.STATUS_UNSAVED:
        instance._status = instance.STATUS_CLOSED
    # following will allow us to detect failure in registration
    if not instance.receipt:
        instance.receipt = 'NO_RECEIPT'


@receiver(post_save, sender=MalariaReport)
def post_save_report(sender, instance, **kwargs):
    """ generates the receipt """
    if instance.receipt == 'NO_RECEIPT':
        instance.receipt = sender.generate_receipt(instance)
        instance.save()

reversion.register(MalariaReport)
