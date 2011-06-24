#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.translation import ugettext as _

register = template.Library()


@register.filter(name='pnlpcat')
@stringfilter
def formcategories(value):
    """ categorie name from category slug """
    value = value.lower()
    if value == 'u5':
        return _(u"Children Under 5yo.")
    if value == 'o5':
        return _(u"Children Over 5yo.")
    if value == 'pw':
        return _(u"Pregnant Women")
    if value == 'period':
        return _(u"Reporting")
    if value == 'fillin':
        return _(u"Collect / Data Entry")
    if value == 'stockout':
        return _(u"Stock outs")
