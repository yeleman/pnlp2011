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

from bolibana_reporting.models import Report
from pnlp_core.models import MalariaReport

locale.setlocale(locale.LC_ALL, '')

register = template.Library()

ALL_COUNTRY_CODES = [1242, 1246, 1264, 1268, 1284, 1340, 1345, 1441, 1473, \
                     1599, 1649, 1664, 1670, 1671, 1684, 1758, 1767, 1784, \
                     1809, 1868, 1869, 1876, 1, 20, 212, 213, 216, 218, 220, \
                     221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, \
                     232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, \
                     243, 244, 245, 248, 249, 250, 251, 252, 253, 254, 255, \
                     256, 257, 258, 260, 261, 262, 263, 264, 265, 266, 267, \
                     268, 269, 27, 290, 291, 297, 298, 299, 30, 31, 32, 33, \
                     34, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, \
                     36, 370, 371, 372, 373, 374, 375, 376, 377, 378, 380, \
                     381, 382, 385, 386, 387, 389, 39, 40, 41, 420, 421, 423, \
                     43, 44, 45, 46, 47, 48, 49, 500, 501, 502, 503, 504, \
                     505, 506, 507, 508, 509, 51, 52, 53, 54, 55, 56, 57, 58, \
                     590, 591, 592, 593, 595, 597, 598, 599, 60, 61, 62, 63, \
                     64, 65, 66, 670, 672, 673, 674, 675, 676, 677, 678, 679, \
                     680, 681, 682, 683, 685, 686, 687, 688, 689, 690, 691, \
                     692, 7, 81, 82, 84, 850, 852, 853, 855, 856, 86, 870, \
                     880, 886, 90, 91, 92, 93, 94, 95, 960, 961, 962, 963, \
                     964, 965, 966, 967, 968, 970, 971, 972, 973, 974, 975, \
                     976, 977, 98, 992, 993, 994, 995, 996, 998]


@register.filter(name='phone')
@stringfilter
def phone_number_formatter(number):
    """ turns 21345678 into 12 34 56 78 """

    def is_int(number):
        if re.match(r'^[+|(]', number):
            return True
        if re.match(r'^\d{1,4}\.\d+$', number):
            return True
        return False

    def get_indicator(number):
        for indic in ALL_COUNTRY_CODES:
            if number.startswith(indic.__str__()):
                return indic.__str__()
        return ''

    def format(number):
        if len(number) & 1:
            span = 3
        else:
            span = 2
        return u" ".join([u"".join(number[i:i + span]) \
                          for i in range(0, len(number), span)])

    if not isinstance(number, basestring):
        number = number.__str__()

    # cleanup markup
    clean_number = re.sub(r'[^\d]', '', number)

    # is in international format?
    if is_int(re.sub(r'[\-\s]', '', number)):
        h, indicator, clean_number = \
                            clean_number.partition(get_indicator(clean_number))
        return _(u"(%(ind)s) %(num)s") \
               % {'ind': indicator, 'num': format(clean_number)}
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
