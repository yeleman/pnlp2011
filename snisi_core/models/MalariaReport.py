#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import inspect

import reversion
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from bolibana.models import EntityType, Report, MonthPeriod

from common import (pre_save_report, post_save_report, report_create_from,
                    aggregated_model_report_pre_save)


class MalariaReportIface(object):

    @property
    def total_consultation_all_causes(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_suspected_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_simple_malaria_cases(self):
        # no value for pregnant_women
        return self.u5_total_simple_malaria_cases \
               + self.o5_total_simple_malaria_cases

    @property
    def total_severe_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_tested_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_confirmed_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_treated_malaria_cases(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_inpatient_all_causes(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_malaria_inpatient(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_death_all_causes(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_malaria_death(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_anc1(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_sp1(self):
        return self.total_for_field(inspect.stack()[0][3])

    @property
    def total_sp2(self):
        return self.total_for_field(inspect.stack()[0][3])

    def total_for_field(self, field):
        values = []
        for cat in ('u5', 'o5', 'pw'):
            fname = '%s_%s' % (cat, field)
            if hasattr(self, fname):
                values.append(getattr(self, fname))
        return sum(values)

    @property
    def mperiod(self):
        """ casted period to MonthPeriod """
        mp = self.period
        mp.__class__ = MonthPeriod
        return mp

    @classmethod
    def start(cls, period, entity, author, \
               type=Report.TYPE_SOURCE, is_late=False, *args, **kwargs):
        """ creates a report object with meta data only. Object not saved """
        report = cls(period=period, entity=entity, created_by=author, \
                     modified_by=author, _status=cls.STATUS_CREATED, \
                     type=type)
        report.is_late = is_late
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
                                stockout_artemether, \
                                stockout_quinine, \
                                stockout_serum, \
                                stockout_bednet, \
                                stockout_rdt, \
                                stockout_sp):
        self.stockout_act_children = stockout_act_children
        self.stockout_act_youth = stockout_act_youth
        self.stockout_act_adult = stockout_act_adult
        self.stockout_artemether = stockout_artemether
        self.stockout_quinine = stockout_quinine
        self.stockout_serum = stockout_serum
        self.stockout_bednet = stockout_bednet
        self.stockout_rdt = stockout_rdt
        self.stockout_sp = stockout_sp

    def to_dict(self):
        d = {}
        for field in self.data_field():
            d[field] = getattr(self, field)
        return d

    @classmethod
    def data_field(cls):
        fields = []
        for field in cls._meta.get_all_field_names():
            try:
                if field.split('_')[0] in ('u5', 'o5', 'pw', 'stockout'):
                    fields.append(field)
            except:
                continue
        fields.append('is_late')
        return fields

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
        """ runs MalariaReportValidator """
        from snisi_core.validators.malaria import MalariaReportValidator
        validator = MalariaReportValidator(self)
        validator.validate()
        return validator.errors


class MalariaReport(Report, MalariaReportIface):

    """ Complies with bolibana.reporting.DataBrowser """

    YES = 'Y'
    NO = 'N'
    YESNO = ((YES, _(u"Yes")), (NO, _(u"No")))

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _(u"Malaria Report")
        verbose_name_plural = _(u"Malaria Reports")
        unique_together = ('period', 'entity', 'type')

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
    stockout_artemether = models.CharField(_(u"Artemether"), \
                                           max_length=1, choices=YESNO)
    stockout_quinine = models.CharField(_(u"Quinine"), \
                                        max_length=1, choices=YESNO)
    stockout_serum = models.CharField(_(u"Serum"), max_length=1, choices=YESNO)
    stockout_bednet = models.CharField(_(u"Bednets"), \
                                       max_length=1, choices=YESNO)
    stockout_rdt = models.CharField(_(u"RDTs"), max_length=1, choices=YESNO)
    stockout_sp = models.CharField(_(u"SPs"), max_length=1, choices=YESNO)

    is_late = models.BooleanField(default=False,
                                  verbose_name=_(u"Is Late?"))

    sources = models.ManyToManyField('MalariaReport', \
                                     verbose_name=_(u"Sources"), \
                                     blank=True, null=True)

    def fill_blank(self):
        self.add_underfive_data(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.add_overfive_data(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.add_pregnantwomen_data(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.add_stockout_data(self.NO, self.NO, self.NO, self.NO, self.NO, \
                               self.NO, self.NO, self.NO, self.NO)

    @classmethod
    def create_aggregated(cls, period, entity, author, *args, **kwargs):
        agg_report = cls.start(period, entity, author, \
               type=Report.TYPE_AGGREGATED, *args, **kwargs)

        sources = MalariaReport.validated.filter(period=period, \
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

receiver(pre_save, sender=MalariaReport)(pre_save_report)
receiver(post_save, sender=MalariaReport)(post_save_report)

reversion.register(MalariaReport)


class AggregatedMalariaReport(Report, MalariaReportIface):

    class Meta:
        app_label = 'snisi_core'
        verbose_name = _(u"Aggregated Malaria Report")
        verbose_name_plural = _(u"Aggregated Malaria Reports")
        unique_together = ('period', 'entity', 'type')

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

    stockout_act_children = models.PositiveIntegerField(_(u"ACT Children"))
    stockout_act_youth = models.PositiveIntegerField(_(u"ACT Youth"))
    stockout_act_adult = models.PositiveIntegerField(_(u"ACT Adult"))
    stockout_artemether = models.PositiveIntegerField(_(u"Artemether"))
    stockout_quinine = models.PositiveIntegerField(_(u"Quinine"))
    stockout_serum = models.PositiveIntegerField(_(u"Serum"))
    stockout_bednet = models.PositiveIntegerField(_(u"Bednets"))
    stockout_rdt = models.PositiveIntegerField(_(u"RDTs"))
    stockout_sp = models.PositiveIntegerField(_(u"SPs"))

    nb_prompt = models.PositiveIntegerField()

    indiv_sources = models.ManyToManyField('MalariaReport',
                                           verbose_name=_(u"Indiv. Sources"),
                                           blank=True, null=True,
                                           related_name='indiv_agg_malaria_reports')

    agg_sources = models.ManyToManyField('AggregatedMalariaReport',
                                         verbose_name=_(u"Aggr. Sources"),
                                         blank=True, null=True,
                                         related_name='aggregated_agg_malaria_reports')

    def fill_blank(self):
        self.add_underfive_data(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.add_overfive_data(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.add_pregnantwomen_data(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.add_stockout_data(0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.nb_prompt = 0

    @classmethod
    def create_from(cls, period, entity, author):
        return report_create_from(cls, period=period, entity=entity,
                                  author=author, indiv_cls=MalariaReport)

    @classmethod
    def update_instance_with_indiv(cls, report, instance):

        for field in instance.data_field():
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


receiver(pre_save, sender=AggregatedMalariaReport)(pre_save_report)
receiver(pre_save,
         sender=AggregatedMalariaReport)(aggregated_model_report_pre_save)
receiver(post_save, sender=AggregatedMalariaReport)(post_save_report)

reversion.register(AggregatedMalariaReport)
