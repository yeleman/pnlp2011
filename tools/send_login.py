#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys

from bolibana.models import Provider
from nosmsd.utils import send_sms


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


def send_login(csv_file, provider_filter=filter_none, dry_run=True):
    """ Send an SMS with login/pass from CSV file

    CSV FORMAT:

    """

    message = u"[PNLP] Systeme de routine Paludisme. Votre identifiant est %(username)s Votre mot de passe est %(password)s Appellez le 65731076 en cas de besoin. Ala ka to nooro ya."

    count = 0
    f = open(csv_file)
    for line in f.readlines():
        # explode CSV line
        entname, rolename, fname, lname, \
        username, password, password_enc = line.strip().split(',')

        username = username.strip()
        password = password.strip()

        try:
            provider = Provider.objects.get(user__username=username)
        except:
            print("ERROR: can't find user: %s" % username)
            continue

        if not provider_filter.__call__(provider):
            continue

        count += 1

        msg = message % {'username': username, 'password': password}

        print(u">>%(phone)s | %(msg)s" % {'phone': provider.phone_number,
                                          'msg': msg})

        if not dry_run:
            send_sms(provider.phone_number, msg)
            pass

    f.close()
    print(count)

if __name__ == '__main__':
    if sys.argv.__len__() < 2:
        print("No CSV file specified. exiting.")
        exit(1)

    send_login(sys.argv[1])
