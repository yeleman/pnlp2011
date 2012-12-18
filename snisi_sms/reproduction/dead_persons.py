#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from snisi_core.models import MaternalMortalityReport, ChildrenMortalityReport
from bolibana.models import Entity, MonthPeriod
from snisi_sms.common import (contact_for, resp_error, resp_error_dob,
                    resp_error_provider, parse_age_dob,
                     resp_error_date, date_is_old)

SEX = {
    'm': ChildrenMortalityReport.MALE,
    'f': ChildrenMortalityReport.FEMALE
}

DEATHPLACE = {
    'd': ChildrenMortalityReport.HOME,
    'c': ChildrenMortalityReport.CENTER,
    'a': ChildrenMortalityReport.OTHER,
}

DEATH_CAUSES_MAT = {
    'b': MaternalMortalityReport.CAUSE_BLEEDING,
    'f': MaternalMortalityReport.CAUSE_FEVER,
    'h': MaternalMortalityReport.CAUSE_HTN,
    'd': MaternalMortalityReport.CAUSE_DIARRHEA,
    'c': MaternalMortalityReport.CAUSE_CRISIS,
    'm': MaternalMortalityReport.CAUSE_MISCARRIAGE,
    'a': MaternalMortalityReport.CAUSE_ABORTION,
    'o': MaternalMortalityReport.CAUSE_OTHER,
}

DEATH_CAUSES_U5 = {
    'f': ChildrenMortalityReport.CAUSE_FEVER,
    'd': ChildrenMortalityReport.CAUSE_DIARRHEA,
    'b': ChildrenMortalityReport.CAUSE_DYSPNEA,
    'a': ChildrenMortalityReport.CAUSE_ANEMIA,
    'r': ChildrenMortalityReport.CAUSE_RASH,
    'c': ChildrenMortalityReport.CAUSE_COUGH,
    'v': ChildrenMortalityReport.CAUSE_VOMITING,
    'n': ChildrenMortalityReport.CAUSE_NUCHAL_RIGIDITY,
    'e': ChildrenMortalityReport.CAUSE_RED_EYE,
    't': ChildrenMortalityReport.CAUSE_EAT_REFUSAL,
    'o': ChildrenMortalityReport.CAUSE_OTHER,
}


def resp_error_reporting_location(message, code):
    message.respond(u"[ERREUR] Le Lieu de rapportage %s n'existe pas."
                                                               % code)
    return True


def resp_error_death_location(message, code):
    message.respond(u"[ERREUR] Le lieu du deces %s n'existe pas."
                                                               % code)
    return True


def resp_error_dod(message):
    message.respond(u"[ERREUR] La date de décès n'est pas valide")
    return True


def resp_success(message, name):
    message.respond(u"[SUCCES] Le rapport de deces de %(name)s a"
                    u" ete enregistre." % {'name': name})
    return True


def unfpa_dead_pregnant_woman(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap dpw profile reccord_date reporting_location_code
                      name age_or_dob dod_text death_location_code
                      living_children_text dead_children_text pregnant_text
                      pregnancy_weeks_text pregnancy_related_death_text
            exemple: 'fnuap dpw f 20120524 bana kona_diarra 20120524 20120524
                       bana 1 0 0 - 0 m'

         Outgoing:
            [SUCCES] Le rapport de deces name a ete enregistre.
            or [ERREUR] message """

    try:
        profile, reccord_date, reporting_location_code, name, age_or_dob, \
        dod_text, death_location_code, living_children_text, \
        dead_children_text, pregnant_text, pregnancy_weeks_text, \
        pregnancy_related_death_text, cause_of_death_text = args.split()
    except:
        return resp_error(message, u"le rapport")

    # Entity code
    try:
        reporting_location = Entity.objects.get(slug=reporting_location_code)
    except Entity.DoesNotExist:
        return resp_error_reporting_location(message, reporting_location_code)

    # DOB (YYYY-MM-DD) or age (11y/11m)
    try:
        dob, dob_auto = parse_age_dob(age_or_dob)
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

    # Date of Death, YYYY-MM-DD
    try:
        dod = parse_age_dob(dod_text, True)
    except:
        return resp_error_dod(message)

    # Place of death, entity code
    try:
        death_location = Entity.objects.get(slug=death_location_code)
    except Entity.DoesNotExist:
        return resp_error_death_location(message, death_location_code)

    # Nb of living children
    try:
        living_children = int(living_children_text)
    except:
        return resp_error(message, u"le nombre d'enfants vivant du defunt")

    # Nb of dead children
    try:
        dead_children = int(dead_children_text)
    except:
        return resp_error(message, u"le nombre d'enfants morts de la"
                                   u" personne decedee")

    # was she pregnant (0/1)
    pregnant = bool(int(pregnant_text))

    # Nb of weeks of pregnancy (or 0)
    try:
        pregnancy_weeks = int(pregnancy_weeks_text)
    except:
        pregnancy_weeks = None

    # Pregnancy related death? (0/1)
    pregnancy_related_death = bool(int(pregnancy_related_death_text))

    contact = contact_for(message.identity)

    report = MaternalMortalityReport()

    if contact:
        report.created_by = contact
    else:
        resp_error_provider(message)

    report.reporting_location = reporting_location
    report.name = name.replace('_', ' ')
    report.dob = dob
    report.dob_auto = dob_auto
    report.dod = dod
    report.death_location = death_location
    report.living_children = living_children
    report.dead_children = dead_children
    report.pregnant = pregnant
    report.pregnancy_weeks = pregnancy_weeks
    report.pregnancy_related_death = pregnancy_related_death
    report.cause_of_death = DEATH_CAUSES_MAT.get(cause_of_death_text,
                                        MaternalMortalityReport.CAUSE_OTHER)

    try:
        report.save()
        report.created_on = reccord_date
        report.save()
    except:
        message.respond(u"[ERREUR] Le rapport n est pas enregiste")
        return True

    return resp_success(message, report.name)


def unfpa_dead_children_under5(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap du5 profile reccord_date reporting_location_code name sex
            age_or_dob dod_text death_location_code place_death
         exemple: 'fnuap du5 f 20120502 wolo nom F 20100502 20120502 wolo D o'

         Outgoing:
            [SUCCES] Le rapport de deces name a ete enregistre.
            or [ERREUR] message """

    try:
        profile, reccord_date, reporting_location_code, name, sex, \
        age_or_dob, dod_text, death_location_code, \
        place_death, cause_of_death_text = args.split()
    except:
        return resp_error(message, u"l'enregistrement de rapport "
                                   u" des moins de 5ans")

    # Entity code
    try:
        reporting_location = Entity.objects.get(slug=reporting_location_code)
    except Entity.DoesNotExist:
        return resp_error_reporting_location(message, reporting_location_code)

    # DOB (YYYY-MM-DD) or age (11a/11m)
    try:
        dob, dob_auto = parse_age_dob(age_or_dob)
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

    # Date of Death, YYYY-MM-DD
    try:
        dod = parse_age_dob(dod_text, True)
    except:
        return resp_error_dod(message)

    # Place of death, entity code
    try:
        death_location = Entity.objects.get(slug=death_location_code)
    except Entity.DoesNotExist:
        return resp_error_death_location(message, death_location_code)

    contact = contact_for(message.identity)

    report = ChildrenMortalityReport()

    if contact:
        report.created_by = contact
    else:
        return resp_error_provider(message)

    report.reporting_location = reporting_location
    report.name = name.replace('_', ' ')
    report.sex = SEX.get(sex, ChildrenMortalityReport.MALE)
    report.dob = dob
    report.dob_auto = dob_auto
    report.dod = dod
    report.death_location = death_location
    report.death_place = DEATHPLACE.get(place_death,
                                        ChildrenMortalityReport.OTHER)
    report.cause_of_death = DEATH_CAUSES_U5.get(cause_of_death_text,
                                        ChildrenMortalityReport.CAUSE_OTHER)

    try:
        report.save()
        report.created_on = reccord_date
        report.save()
        return resp_success(message, report.name)
    except:
        return resp_error(message, u"Le rapport de deces n'a pas ete enregistre.")
