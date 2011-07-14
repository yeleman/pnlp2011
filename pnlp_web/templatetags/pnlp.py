#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import re
import locale

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from django.contrib.humanize.templatetags.humanize import intcomma

from bolibana_reporting.models import Report, Entity
from pnlp_core.models import MalariaReport
from pnlp_core.utils import clean_phone_number

locale.setlocale(locale.LC_ALL, '')

register = template.Library()


@register.filter(name='phone')
@stringfilter
def phone_number_formatter(number):
    """ turns 21345678 into 12 34 56 78 """

    def format(number):
        if len(number) & 1:
            span = 3
        else:
            span = 2
        return u" ".join([u"".join(number[i:i + span]) \
                          for i in range(0, len(number), span)])

    ind, clean_number = clean_phone_number(number)
    if ind:
        return _(u"(%(ind)s) %(num)s") \
               % {'ind': ind, 'num': format(clean_number)}
    return format(clean_number)


@register.filter(name='pnlpcat')
@stringfilter
def formcategories(value):
    """ categorie name from category slug """
    value = value.lower()
    if value in ('u5', 'under_five'):
        return _(u"Children Under 5yo.")
    if value in ('o5', 'over_five'):
        return _(u"Children Over 5yo.")
    if value in ('pw', 'pregnant_women'):
        return _(u"Pregnant Women")
    if value == 'period':
        return _(u"Reporting")
    if value == 'fillin':
        return _(u"Collect / Data Entry")
    if value == 'stockout':
        return _(u"Stock outs")
    if value == 'all':
        return _(u"Tout âge confondu")
    if value == 'all_over_five':
        return u"%s avec %s" % (formcategories('o5'), formcategories('pw'))
    return _(u"Default")


@register.filter(name='reporttype')
@stringfilter
def report_type_verbose(value):
    for v, name in Report.TYPES:
        if v.__str__() == value:
            return name
    return value


@register.filter(name='reportstatus')
@stringfilter
def report_status_verbose(value):
    for v, name in Report.STATUSES:
        if v.__str__() == value:
            return name
    return value


@register.filter(name='reportvalue')
@stringfilter
def report_type_verbose(value):
    try:
        float(value)
        return number_format(value)
    except:
        return report_type_verbose(value)


@register.filter(name='reportstockouts')
@stringfilter
def report_type_verbose(value):
    for v, name in MalariaReport.YESNO:
        if v.__str__() == value:
            return name
    return value


def strnum_french(numstr):
    if locale.getdefaultlocale()[0].startswith('fr'):
        return numstr
    else:
        return numstr.replace(',', ' ').replace('.', ',')


@register.filter(name='numberformat')
@stringfilter
def number_format(value, precision=2, french=True):
    try:
        format = '%d'
        value = int(value)
    except:
        try:
            format = '%.' + '%df' % precision
            value = float(value)
        except:
            format = '%s'
        else:
            if value.is_integer():
                format = '%d'
                value = int(value)
    try:
        if french:
            return strnum_french(locale.format(format, value, grouping=True))
        return locale.format(format, value, grouping=True)
    except Exception as e:
        pass
    return value


@register.filter(name='concat')
@stringfilter
def concat_strings(value, value2):
    try:
        return u"%s%s" % (value, value2)
    except:
        return value


@register.filter(name='url')
@stringfilter
def retrieve_url(url_name, arg1=None, arg2=None, arg3=None, arg4=None):
    args = [arg1, arg2, arg3, arg4]
    while True:
        try:
            args.remove(None)
        except ValueError:
            break
    return reverse(url_name, args=args)


@register.filter(name='index')
@stringfilter
def string_index(value, index):
    if not ':' in index:
        return value[index]
    pref, sep, suf = index.partition(':')
    pref = int(pref) if pref else None
    suf = int(suf) if suf else None

    return value[None:suf]


@register.filter(name='percent')
@stringfilter
def format_percent(value, precision=2, french=True):
    try:
        return number_format(float(value) * 100, precision, french) + '%'
    except:
        return value


@register.filter(name='percentraw')
@stringfilter
def format_percent_us(value, precision=2, french=True):
    return format_percent(value, precision, french=False)[:-1]


def get_parent_by_type(entity_slug, type):
    entity = Entity.objects.get(slug=entity_slug)
    if entity.type.slug == type:
        return entity
    while entity.parent:
        if entity.parent.type.slug == type:
            return entity.parent
        entity = entity.parent
    return None


@register.filter(name='region')
@stringfilter
def region_from_slug(entity_slug):
    return get_parent_by_type(entity_slug, 'region')


@register.filter(name='district')
@stringfilter
def region_from_slug(entity_slug):
    return get_parent_by_type(entity_slug, 'district')
