#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from snisi_core.models import BirthReport
from bolibana.models import Entity, MonthPeriod
from common import (contact_for, resp_error, resp_error_dob,
                             resp_error_provider, parse_age_dob,
                             resp_error_date, date_is_old)


BIRTHPLACE = {
    'd': BirthReport.HOME,
    'c': BirthReport.CENTER,
    'a': BirthReport.OTHER
}

SEX = {
    'm': BirthReport.MALE,
    'f': BirthReport.FEMALE
}

SOURCE = {
    'f': BirthReport.UNFPA,
    'c': BirthReport.CREDOS
}


def unfpa_birth(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap born profile reccord_date reporting_location family_name
            name_mother name_child dob birth_location sex born_alive
        example:
           'fnuap born c 20120514 baga dolo assan mele 20120514 d m 1'
        Outgoing:
            [SUCCES] Le rapport de name a ete enregistre.
            or [ERREUR] message """

    try:
        profile, reccord_date, reporting_location, family_name, name_mother,\
        name_child, dob, birth_location, sex, born_alive = args.split()
    except:
        return resp_error(message, u"l'enregistrement de la naissance.")

    # Entity code
    try:
        entity = Entity.objects.get(slug=reporting_location)
    except Entity.DoesNotExist:
        message.respond(u"Le code %s n'existe pas." % reporting_location)
        return True

    # DOB (YYYY-MM-DD) or age (11a/11m)
    try:
        dob, dob_auto = parse_age_dob(dob)
    except:
        return resp_error_dob(message)

    # Reporting date (YYYY-MM-DD)
    try:
        reccord_date, _reccord_date = parse_age_dob(reccord_date)
    except:
        return resp_error_date(message)

    try:
        date_is_old(reccord_date)
    except ValueError, e:
        message.respond(u"[ERREUR] %s" % e)
        return True

    MonthPeriod.find_create_from(year=reccord_date.year,
                                 month=reccord_date.month)
    report = BirthReport()

    birth_location = BIRTHPLACE.get(birth_location, BirthReport.OTHER)
    sex = SEX.get(sex, BirthReport.FEMALE)

    born_alive = bool(int(born_alive))

    # if no name of the mother
    if name_mother == '-':
        name_mother = ''

    # if no name of the child
    if name_child == '-':
        name_child = ''

    contact = contact_for(message.identity)

    report.reporting_location = entity

    if contact:
        report.created_by = contact
    else:
        return resp_error_provider(message)

    report.family_name = family_name.replace('_', ' ')
    report.surname_mother = name_mother.replace('_', ' ')
    report.surname_child = name_child.replace('_', ' ')
    report.sex = sex
    report.dob = dob
    report.dob_auto = dob_auto
    report.birth_location = birth_location
    report.born_alive = born_alive
    report.source = SOURCE.get(profile, BirthReport.UNFPA)

    try:
        report.save()
        report.created_on = reccord_date
        report.save()
        message.respond(u"[SUCCES] Le rapport de naissance de" \
                        u"%(full_name_dob)s a ete enregistre." \
                        % {'full_name_dob': report.full_name_dob()})
    except:
        raise
        message.respond(u"[ERREUR] Le rapport de naissance "
                        u"n'a pas ete enregistre.")

    return True
