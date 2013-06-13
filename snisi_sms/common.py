#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import datetime
import re

from datetime import date, timedelta

from bolibana.models.Provider import Provider


def contact_for(identity):
    try:
        provider = Provider.objects.get(phone_number=identity)
    except Provider.DoesNotExist:
        provider = None

    return provider


def resp_error(message, action):
    message.respond(u"[ERREUR] Impossible de comprendre "
                    u"le SMS pour %s" % action)
    return True


def resp_error_date(message):
    message.respond(u"[Date de visite] la date n'est pas valide.")
    return True


def conv_str_int(value):
    try:
        value = int(value)
    except:
        value = None
    return value


def resp_error_dob(message):
    message.respond(u"[ERREUR] la date de naissance n'est pas valide")
    return True


def resp_error_provider(message):
    message.respond(u"Aucun utilisateur ne possede ce numero de telephone")
    return True


def parse_age_dob(age_or_dob, only_date=False):
    """ parse argument as date or age. return date and bool if estimation """

    if re.match(r'^\d{8}$', age_or_dob):
        auto = False
        parsed_date = date(int(age_or_dob[0:4]), int(age_or_dob[4:6]),
                           int(age_or_dob[6:8]))
    else:
        auto = True
        today = date.today()
        unit = age_or_dob[-1]
        value = int(age_or_dob[:-1])
        if unit.lower() == 'a':
            parsed_date = today - timedelta(365 * value) - timedelta(160)
        elif unit.lower() == 'm':
            parsed_date = today - timedelta(30 * value) - timedelta(15)
        else:
            raise ValueError(u"Age unit unknown: %s" % unit)

    if only_date:
        return parsed_date
    else:
        return (parsed_date, auto)


def date_is_old(reporting_date):

    if (date.today() - reporting_date).days > 30:
        raise ValueError(u"Le %s est passé il y a plus 30 jours" % reporting_date)


def test(message, **kwargs):
    try:
        code, msg = message.content.split()
    except:
        msg = ''

    message.respond(u"Received on %(date)s: %(msg)s"
                    % {'date': datetime.datetime.now(), 'msg': msg})
    return True


def echo(message, **kwargs):
    message.respond(kwargs['args'])
    return True
