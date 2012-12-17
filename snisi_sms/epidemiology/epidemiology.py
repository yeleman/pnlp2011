#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.db import IntegrityError
from snisi_core.models import EpidemiologyReport
from bolibana.models import Entity, WeekPeriod
from snisi_sms.common import (contact_for, resp_error, resp_error_provider)


def epidemiology(message, args, sub_cmd, **kwargs):
    """  Incomming:
             epid year number_week code_reporting_location

        example:
           'epid e 2012 1 v01619 1 1 2 2 3 3 4 4 5 5 6 6 7 7 8 8 9 9 10 10 11 11'

        Outgoing:
            [SUCCES] Le rapport de name a ete enregistre.
            or [ERREUR] message """

    # def comparecasedeath(case, death):
    #     if case < death:
    #         message.respond(u"le cas de decès (%s) ne peut pas etre supeieur"
    #                         u" au cas d'epidemie (%s)" %
    #                         (death, case))
    #         return True
    #     return False

    try:
        profile, reporting_year, reporting_week, reporting_location, \
        acute_flaccid_paralysis_case, acute_flaccid_paralysis_death, \
        influenza_a_h1n1_case, influenza_a_h1n1_death, cholera_case, \
        cholera_death, red_diarrhea_case, red_diarrhea_death, measles_case, \
        measles_death, yellow_fever_case, yellow_fever_death, \
        neonatal_tetanus_case, neonatal_tetanus_death, meningitis_case, \
        meningitis_death, rabies_case, rabies_death, \
        acute_measles_diarrhea_case, acute_measles_diarrhea_death, \
        other_notifiable_disease_case, \
        other_notifiable_disease_death = args.split()
    except:
        return resp_error(message, u"l'enregistrement de la naissance.")

    # Entity code
    try:
        entity = Entity.objects.get(slug=reporting_location)
    except Entity.DoesNotExist:
        message.respond(u"Le code %s n'existe pas." % reporting_location)
        return True

    try:
        period = WeekPeriod.find_create_by_weeknum(int(reporting_year),
                                    int(reporting_week))
    except:
        message.respond(u"La periode (%s %s) n'est pas valide" %
                        (reporting_week, reporting_year))
        return True

    # liste = args.split()[4:]

    # comp = 0
    # for u in range(0, len(liste) / 2):
    #     print liste[comp], "?",  liste[comp + 1]
    #     if liste[comp] < liste[comp + 1]:
    #         print liste[comp], "<",  liste[comp + 1]
    #     else:
    #         print "cool"
    #     comp += 2

    # print acute_flaccid_paralysis_case, acute_flaccid_paralysis_death

    # comparecasedeath(acute_flaccid_paralysis_case,
    #                  acute_flaccid_paralysis_death)
    # comparecasedeath(influenza_a_h1n1_case, influenza_a_h1n1_death)
    # comparecasedeath(cholera_case, cholera_death)
    # comparecasedeath(red_diarrhea_case, red_diarrhea_death)
    # comparecasedeath(measles_case, measles_death)
    # comparecasedeath(yellow_fever_case, yellow_fever_death)
    # comparecasedeath(neonatal_tetanus_case, neonatal_tetanus_death)
    # comparecasedeath(meningitis_case, meningitis_death)
    # comparecasedeath(rabies_case, rabies_death)
    # comparecasedeath(acute_measles_diarrhea_case, acute_measles_diarrhea_death)
    # comparecasedeath(other_notifiable_disease_case,
    #                  other_notifiable_disease_death)

    try:
        EpidemiologyReport.objects.get(entity=entity, period=period)
        message.respond(u"Il existe un rapport pour cette periode (%s %s) " %
                        (reporting_week, reporting_year))
        return True
    except:
        pass

    report = EpidemiologyReport()
    report.type = 0
    report.period = period

    report.entity = entity
    report.acute_flaccid_paralysis_case = acute_flaccid_paralysis_case
    report.acute_flaccid_paralysis_death = acute_flaccid_paralysis_death
    report.influenza_a_h1n1_case = influenza_a_h1n1_case
    report.influenza_a_h1n1_death = influenza_a_h1n1_death
    report.cholera_case = cholera_case
    report.cholera_death = cholera_death
    report.red_diarrhea_case = red_diarrhea_case
    report.red_diarrhea_death = red_diarrhea_death
    report.measles_case = measles_case
    report.measles_death = measles_death
    report.yellow_fever_case = yellow_fever_case
    report.yellow_fever_death = yellow_fever_death
    report.neonatal_tetanus_case = neonatal_tetanus_case
    report.neonatal_tetanus_death = neonatal_tetanus_death
    report.meningitis_case = meningitis_case
    report.meningitis_death = meningitis_death
    report.rabies_case = rabies_case
    report.rabies_death = rabies_death
    report.acute_measles_diarrhea_case = acute_measles_diarrhea_case
    report.acute_measles_diarrhea_death = acute_measles_diarrhea_death
    report.other_notifiable_disease_case = other_notifiable_disease_case
    report.other_notifiable_disease_death = other_notifiable_disease_death

    contact = contact_for(message.identity)

    if contact:
        report.created_by = contact
    else:
        return resp_error_provider(message)

    try:
        report.save()
        message.respond(u"[SUCCES] Le rapport de %(cscom)s pour %(period)s "
                        u"a ete enregistre. "
                        u"Le No de recu est #%(receipt)s."
                        % {'cscom': report.entity.display_full_name(),
                           'period': report.period,
                           'receipt': report.receipt})
    except IntegrityError:
        message.respond(u"[ERREUR] il ya deja un rapport pour cette periode")
    except:
        message.respond(u"[ERREUR] Le rapport n est pas enregiste")

    return True
