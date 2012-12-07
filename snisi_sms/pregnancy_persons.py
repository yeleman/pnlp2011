#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from snisi_core.models import PregnancyReport
from bolibana.models import Entity, MonthPeriod
from common import (contact_for, resp_error, conv_str_int, resp_error_dob,
                    resp_error_provider, parse_age_dob,
                    resp_error_date, date_is_old)

SOURCE = {
    'f': PregnancyReport.UNFPA,
    'c': PregnancyReport.CREDOS
}


def unfpa_pregnancy(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap gpw profile reporting_location householder_name reccord_date
            mother_name dob pregnancy_age expected_delivery_date
            pregnancy_result delivery_date
        example:
           'fnuap gpw f wolo alou_dolo 20120109 fola_keita 45a 9 20110509 0
            20120109'
        Outgoing:
            [SUCCES] Le rapport de name a ete enregistre.
            or [ERREUR] message """

    try:
        profile, reporting_location, householder_name, reccord_date, \
        mother_name, dob, pregnancy_age, expected_delivery_date, \
        pregnancy_result, delivery_date = args.split()
    except:
        return resp_error(message, u"l'enregistrement de la grossesse.")

    # Entity code
    try:
        entity = Entity.objects.get(slug=reporting_location)
    except Entity.DoesNotExist:
        message.respond(u"Le code %s n'existe pas" % reporting_location)
        return True

    # DOB (YYYY-MM-DD) or age (11a/11m)
    try:
        dob, dob_auto = parse_age_dob(dob)
    except:
        return resp_error_dob(message)

    # reccord date
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

    # expected delivery date
    try:
        expected_delivery_date, _expected_delivery_date = \
                                parse_age_dob(expected_delivery_date)
    except:
        return resp_error_dob(message)

    # delivery date
    try:
        delivery_date, _delivery_date = parse_age_dob(delivery_date)
    except:
        delivery_date = None

    contact = contact_for(message.identity)
    pregnancy_age = conv_str_int(pregnancy_age)
    pregnancy_result = conv_str_int(pregnancy_result)

    report = PregnancyReport()

    report.reporting_location = entity

    if contact:
        report.created_by = contact
    else:
        return resp_error_provider(message)

    report.householder_name = householder_name.replace('_', ' ')
    report.mother_name = mother_name.replace('_', ' ')
    report.dob = dob
    report.dob_auto = dob_auto

    if not pregnancy_age:
        message.respond(u"[Age de la grossesse] l'age n'est pas correct.")
        return True
    else:
        report.pregnancy_age = pregnancy_age

    report.expected_delivery_date = expected_delivery_date
    report.delivery_date = delivery_date

    report.source = SOURCE.get(profile, PregnancyReport.UNFPA)

    if not pregnancy_result:
        report.pregnancy_result = pregnancy_result
    else:
        message.respond(u"[Issu de la grossesse] ce choix n'est pas correct.")
        return True

    try:
        report.save()
        report.created_on = reccord_date
        report.save()
        message.respond(u"[SUCCES] Le rapport de grossesse de %(mother_name)s "
                        u"a ete enregistre."
                        % {'mother_name': report.mother_name})
    except:
        message.respond(u"[ERREUR] Le rapport de naissance "
                        u"n'a pas ete enregistre.")

    return True
