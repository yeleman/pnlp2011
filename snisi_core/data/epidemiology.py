#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django import forms

from snisi_core.models.Epidemiology import EpidemiologyR
from snisi_core.data import COMMON_EXCLUDED_FIELDS


class EpidemiologyRForm(forms.ModelForm):
    class Meta:
        model = EpidemiologyR
        exclude = COMMON_EXCLUDED_FIELDS

AggEpidemiologyRForm = EpidemiologyRForm
