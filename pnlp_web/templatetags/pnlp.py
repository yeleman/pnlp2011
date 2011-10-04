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
        return _(u"All Age")
    if value == 'all_over_five':
        return u"%s avec %s" % (formcategories('o5'), formcategories('pw'))
    return _(u"Default")


@register.filter(name='reporttype')
@stringfilter
def report_type_verbose(value):
    if value == Report.TYPE_SOURCE.__str__():
        return u"Primaire"
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
    if locale.getdefaultlocale()[0].__str__().startswith('fr'):
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
    if value == u'n/a':
        return value
    try:
        return number_format(float(value) * 100, precision, french) + '%'
    except:
        return value


@register.filter(name='percentraw')
@stringfilter
def format_percent_us(value, precision=2, french=True):
    return format_percent(value, precision, french=False)[:-1].replace(',', '.')


def get_parent_by_type(entity, type):
    if entity.type.slug == type:
        return entity
    while entity.parent:
        if entity.parent.type.slug == type:
            return entity.parent
        entity = entity.parent
    return None


@register.filter(name='region')
def region_from_slug(entity):
    return get_parent_by_type(entity, 'region')


@register.filter(name='district')
def region_from_slug(entity):
    return get_parent_by_type(entity, 'district')


@register.filter(name='stage')
@stringfilter
def stage_name(slug):
    if slug == 'cscom':
        return _(u"Data Collection")
    if slug == 'district':
        return _(u"District Validation")
    if slug == 'region':
        return _(u"Region Validation")
    if slug == 'over':
        return _(u"National Analysis")
    return slug


@register.filter(name='rate_class')
@stringfilter
def css_rate_class(rate):
    try:
        rate = float(rate)
    except:
        return rate
    else:
        if rate < 20:
            return 'error'
        if rate < 60:
            return 'warning'
        return 'success'


@register.filter(name='has_permission')
def provider_has_permission(provider, perm_slug=None):
    try:
        return provider.has_permission(perm_slug)
    except:
        return False

@register.filter(name='sorted')
def data_sort(data):
    return sorted(data)
