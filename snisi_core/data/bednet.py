#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django import forms

from snisi_core.models.BednetReport import BednetR
from snisi_core.data import COMMON_EXCLUDED_FIELDS


class BednetRForm(forms.ModelForm):
    class Meta:
        model = BednetR
        exclude = COMMON_EXCLUDED_FIELDS


AggBednetRForm = BednetRForm
