#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys

from bolibana.models import Provider
from nosms.utils import send_sms


def filter_pilot_cscom(provider):
    """ return True if provider is part of pilot CSCOM """

    return provider.first_role().slug == 'cscom' \
       and provider.first_target().parent.slug in ('nion', 'maci')


def filter_none(provider):
    return True


def filter_district(provider):
    """ return True if district role """

    return provider.first_role().slug == 'district'


def filter_region(provider):
    """ return True if district role """

    return provider.first_role().slug == 'region'


def filter_district_region(provider):
    return filter_district(provider) or filter_region(provider)


def send_message(message, provider_filter=filter_none, dry_run=True):

    count = 0

    for provider in Provider.objects.all():

        if not provider_filter.__call__(provider):
            continue

        count += 1

        print(u">>%(phone)s | %(msg)s" % {'phone': provider.phone_number,
                                          'msg': message})

        if not dry_run:
            send_sms(provider.phone_number, message)
            pass

    print(count)
