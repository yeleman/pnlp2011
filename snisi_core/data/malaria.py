#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django import forms

from snisi_core.models.MalariaReport import MalariaR, AggMalariaR
from snisi_core.data import COMMON_EXCLUDED_FIELDS


class MalariaRForm(forms.ModelForm):
    class Meta:
        model = MalariaR
        exclude = COMMON_EXCLUDED_FIELDS


class AggMalariaRForm(forms.ModelForm):
    class Meta:
        model = AggMalariaR
        exclude = COMMON_EXCLUDED_FIELDS


class MalariaDataHolder(object):

    def get(self, slug):
        return getattr(self, slug)

    def field_name(self, slug):
        return MalariaR._meta.get_field(slug).verbose_name

    def set(self, slug, data):
        try:
            setattr(self, slug, data)
        except AttributeError:
            exec 'self.%s = None' % slug
            setattr(self, slug, data)

    def fields_for(self, cat):
        u5fields = ['u5_total_consultation_all_causes',
                    'u5_total_suspected_malaria_cases',
                    'u5_total_simple_malaria_cases',
                    'u5_total_severe_malaria_cases',
                    'u5_total_tested_malaria_cases',
                    'u5_total_confirmed_malaria_cases',
                    'u5_total_treated_malaria_cases',
                    'u5_total_inpatient_all_causes',
                    'u5_total_malaria_inpatient',
                    'u5_total_death_all_causes',
                    'u5_total_malaria_death',
                    'u5_total_distributed_bednets']
        if cat == 'u5':
            return u5fields
        if cat == 'o5':
            return [f.replace('u5', 'o5') for f in u5fields][:-1]
        if cat == 'pw':
            fields = [f.replace('u5', 'pw') for f in u5fields]
            fields.remove('pw_total_simple_malaria_cases')
            fields.extend(['pw_total_anc1', 'pw_total_sp1', 'pw_total_sp2'])
            return fields
        if cat == 'so':
            return ['stockout_act_children',
                    'stockout_act_youth',
                    'stockout_act_adult',
                    'stockout_artemether',
                    'stockout_quinine',
                    'stockout_serum',
                    'stockout_bednet',
                    'stockout_rdt',
                    'stockout_sp']

    def data_for_cat(self, cat, as_dict=False):
        data = []
        for field in self.fields_for(cat):
            data.append(self.get(field))
        return data
