#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import logging
from datetime import datetime, date, timedelta
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from pnlp_core.data import (time_cscom_over, time_district_over, \
                            time_region_over, current_reporting_period, \
                            contact_for)
from pnlp_core.models import MalariaReport, Alert
from bolibana_reporting.models import Entity
from nosms.utils import send_sms
from bolibana_auth.models import Provider, Access
from pnlp_core.utils import send_email, full_url

logger = logging.getLogger(__name__)


class IndividualMalariaReportCreated(Alert):

    """ An individual Malaria Report Created

        Created by the meta MalariaReportCreated Alert
        1. Send message to district to let them now they can validate

        ARGUMENTS:
            - report """

    class Meta:
        proxy = True

    def get_alert_id(self):
        """ Unique report ID attached to (one alert per report) """
        return self.args.report.receipt

    def can_trigger(self, *args, **kwargs):
        # triggers happens if:
        # 1. Such alert has not been triggered
        # 2. We are in the next period as P (don't trigger is it's too late
        return self.not_triggered \
               and self.args.report.mperiod == current_reporting_period()

    def action(self):
        """ send SMS to district/region for each new report """

        report = self.args.report

        # we have a district/cscom report
        logger.info(u"Report %s found." % report)

        contact = contact_for(report.entity.parent)

        message = _(u"[PNLP] Le rapport %(receipt)s de %(entity)s " \
                    "a ete recu. Vous devez le valider.") \
                  % {'receipt': report.receipt, 'entity': report.entity}

        if contact.phone_number:
            send_sms(contact.phone_number, message)
        elif contact.email:
            send_email(recipients=contact.email, message=message, \
                       title=_(u"[PNLP] Nouveau rapport recu!"))
        else:
            send_email(settings.HOTLINE_EMAIL, message, \
                       _(u"[PNLP] Unable to send report notification " \
                         "to %(contact)s") \
                       % {'contact': contact.name_access()})


class MalariaReportCreated(Alert):

    """ Recently Created Malaria Reports (from CSCom, Districts, Region)

        Every now and then between 1st..5th of the month
        1. Send message to district to let them now they can validate

        ARGUMENTS:
            - period """

    class Meta:
        proxy = True

    def get_alert_id(self):
        """ should happen once per month only """
        return datetime.now().strftime('%s')

    def can_trigger(self, *args, **kwargs):
        # triggers happens if:
        # 1. Such alert has not been triggered
        # 2. We are in the next period as P (don't trigger is it's too late
        return self.not_triggered \
               and self.args.period == current_reporting_period()

    def action(self):
        """ send SMS to district/region | email to PNLP for each new report """

        for report in MalariaReport.unvalidated\
                                   .filter(period=self.args.period):

            # entity has no parent. Either Mali or error
            if not report.entity.parent:
                # should never happen but we never know
                # drop if entity has no parent.
                if not report.entity.level == 0:
                    return

                # we now have a national report
                logger.info(u"Report %s found." % report)
                report.status = MalariaReport.STATUS_VALIDATED
                report.save()

                # send emails
                ct, oi = Access.target_data(Entity.objects.get(slug='mali'))
                nat_access = list(Access.objects.filter(content_type=ct, \
                                                        object_id=oi))
                providers = Provider.active\
                                    .select_related()\
                                    .filter(user__email__isnull=False, \
                                            access__in=nat_access)\
                                    .values_list('user__email', flat=True)

                rurl = full_url(path=reverse('raw_data', \
                                   kwargs={'entity_code': report.entity.slug, \
                       'period_str': report.period.middle().strftime('%m%Y')}))

                sent, sent_message = send_email(recipients=providers, \
                                        context={'report': report, \
                                                 'report_url': rurl, \
                                                 'url': full_url()},
                                 template='emails/mali_report_available.txt', \
                      title_template='emails/title.mali_report_available.txt')

                # the rest of the method is only for non-national
                return

            # we only send notifications for CSCom & District reports.
            if report.entity.type.slug not in ('cscom', 'district'):
                continue

            # we don't bug district if cscom period is over
            if report.entity.type.slug == 'cscom' \
               and time_cscom_over(period=self.args.period):
                continue

            # we don't bug region if district period is over
            if report.entity.type.slug == 'district' \
               and time_district_over(period=self.args.period):
                continue

            # create a dedicated alert so it can be tracked by report
            # then fire it.
            alert = IndividualMalariaReportCreated.create(report=report)
            if alert.can_trigger():
                alert.trigger()


class EndOfCSComPeriod(Alert):

    """ End Of CSCom sending Timeframe

        Each month on the 6th.
        1. Send message to those who have not sent.
        2. Warn districts about available reports

        ARGUMENTS:
            - period """

    class Meta:
        proxy = True

    def get_alert_id(self):
        """ should happen once per month only """
        return self.args.period.middle().strftime('%m%Y')

    def can_trigger(self, *args, **kwargs):
        # triggers happens if:
        # 1. CSCom period for P is over
        # 2. Such alert has not been triggered
        # 3. We are in the next period as P (don't trigger is it's too late)
        return time_cscom_over(period=self.args.period) \
               and self.not_triggered \
               and self.args.period == current_reporting_period()

    def action(self):
        """ send SMS to non-sender and to districts

            Non-sending CSCom will receive a message saying they missed.
            District will be reminded they have reports to validate
            and non-sending cscom if applicable """

        # send an SMS to non-reporting CSCOM.
        message = _(u"[PNLP] Vous n'avez pas envoye votre rapport mensuel." \
                    " Il est desormais trop tard pour l'envoyer. " \
                    "Vos donnees ne seront donc pas integrees.")
        for contact in [contact_for(entity, recursive=False) \
                        for entity in self.get_bad_cscom()]:
            if not contact or not contact.phone_number:
                continue

            send_sms(to=contact.phone_number, text=message)

        # send an SMS to districts:
        # 1. those with non-validated reports.
        # 2. those with non-reporting cscom.
        for dis, e in self.get_all_district().items():

            contact = contact_for(e['entity'], recursive=False)

            if not contact or not contact.phone_number:
                continue

            # already received everything and validated.
            # congrats, we won't bug you buddy.
            if e['unval'] == 0 and e['unsent'] == 0:
                continue

            if e['unval']:
                msg_unval = _(u"%(nb)s de vos CSCom ont envoye leur " \
                              "rapport. Vous devez les valider avant le 15.") \
                            % {'nb': e['unval']}
            else:
                msg_unval = u""

            if e['unsent']:
                msg_unsent = _(u"%(nb)s n'ont pas envoyer leur rapport " \
                               "mensuel dans les temps!") % {'nb': e['unsent']}
            else:
                msg_unsent = u""

            # add space before second sentence if both
            if e['unval'] and e['unsent']:
                msg_unsent = u" %s" % msg_unsent

            message = _(u"[PNLP] %(unval)s%(unsent)s") \
                      % {'unval': msg_unval, 'unsent': msg_unsent}

            send_sms(to=contact.phone_number, text=message)

    def get_all_district(self):
        districts = {}
        unval = [r.entity for r \
                          in MalariaReport.unvalidated.select_related()\
                                      .filter(period=self.args.period, \
                                              type=MalariaReport.TYPE_SOURCE)]
        unsent = self.get_bad_cscom()

        def increment(entities, cat):
            for e in entities:
                try:
                    districts[e.parent.slug][cat]
                except:
                    districts[e.parent.slug] = {'entity': e, \
                                                'unval': 0, 'unsent': 0}
                districts[e.parent.slug][cat] += 1
        increment(unval, 'unval')
        increment(unsent, 'unsent')
        return districts

    def get_bad_cscom(self):
        reported = MalariaReport.objects.select_related()\
                                        .filter(period=self.args.period, \
                                                entity__type__slug='cscom')\
                                        .values_list('entity__id', flat=True)
        return list(Entity.objects.filter(~models.Q(pk__in=reported), \
                                          type__slug='cscom'))


class EndOfDistrictPeriod(Alert):

    """ End Of District Validation Timeframe

        Each month on the 16th.
        1. Auto-validate all reports
        2. Create aggregated reports
        3. Warn region about available reports

        ARGUMENTS:
            - period
            - is_district (assumed region is not set) """

    class Meta:
        proxy = True

    def get_alert_id(self):
        """ should happen once per month only """
        return self.args.period.middle().strftime('%m%Y')

    def can_trigger(self, *args, **kwargs):
        # triggers happens if:
        # 1. District period for P is over
        # 2. Such alert has not been triggered
        # 3. We are in the next period as P (don't trigger is it's too late
        if self.args.is_district:
            time_is_over = time_district_over(period=self.args.period)
        else:
            time_is_over = time_region_over(period=self.args.period)
        return time_is_over \
               and self.not_triggered \
               and self.args.period == current_reporting_period()

    def action(self):
        """ Validate remaining reports and inform region """

        # retrieve autobot provider if possible
        try:
            author = Provider.active.get(user__username='autobot')
        except:
            author = None

        if self.args.is_district:
            validate_level = 'cscom'
            aggregate_level = 'district'
        else:
            validate_level = 'district'
            aggregate_level = 'region'

        # validate non-validated reports
        for report in MalariaReport.unvalidated\
                                   .filter(period=self.args.period, \
                                           entity__type__slug=validate_level):
            report.status = MalariaReport.STATUS_VALIDATED
            if author:
                report.modified_by = author
            report.modified_on = datetime.now()
            report.save()

        # create aggregated reports
        for entity in Entity.objects.filter(type__slug=aggregate_level):
            if entity.reports.filter(period=self.args.period).count() > 0:
                continue
            rauthor = contact_for(entity) if not author else author
            logger.info(u"Creating Aggregated report for %s" % entity)
            report = MalariaReport.create_aggregated(self.args.period, \
                                                     entity, rauthor)
            # region auto-validates their reports
            if not self.args.is_district:
                report.status = MalariaReport.STATUS_VALIDATED
                report.save()

        # region-only section
        # create national report
        mali = Entity.objects.get(slug='mali')
        if not self.args.is_district \
           and mali.reports.filter(period=self.args.period).count() == 0:
            rauthor = author if author else Provider.objects.all()[0]
            logger.info(u"Creating National report")
            report = MalariaReport.create_aggregated(self.args.period, \
                                                     mali, rauthor)

            # following only applies to districts (warn regions).
            return

        # district-only section
        # let region know there are reports to validate
        for region in Entity.objects.filter(type__slug='region'):
            contact = contact_for(region, recursive=False)

            # skip if not recipient
            if not contact or not contact.phone_number:
                continue

            nb_reports = MalariaReport.unvalidated\
                                   .filter(period=self.args.period, \
                                           entity__type__slug='district', \
                                           entity__parent=region).count()

            message = _(u"[PNLP] La periode de validation CSRef est " \
                        "terminee. Vous avez %(nb)d rapports de " \
                        "CSRef a valider.") % {'nb': nb_reports}

            send_sms(to=contact.phone_number, text=message)


def level_statistics(period, level):
    """ district slug indexed hash of {'entity': district, 'unval': x}

        representing the number of unvalidated reports for the district """
    entities = {}
    sublevel = 'cscom' if level == 'district' else 'district'
    unval = [r.entity for r \
                      in MalariaReport.unvalidated.select_related()\
                                  .filter(period=period, \
                                          entity__type__slug=sublevel)]

    for e in unval:
        try:
            entities[e.parent.slug]['entity']
        except:
            entities[e.parent.slug] = {'entity': e.parent, 'unval': 0}
        entities[e.parent.slug]['unval'] += 1

    return entities


def cscom_without_report(period):
    """ list of Entity (cscom) which have not sent report """
    reported = MalariaReport.objects.select_related()\
                                    .filter(period=period, \
                                            entity__type__slug='cscom')\
                                    .values_list('entity__id', flat=True)
    return list(Entity.objects.filter(~models.Q(pk__in=reported), \
                                      type__slug='cscom'))


class Reminder(Alert):

    """ Reminder of action required

        Every day within action time frame
        1. send SMS to remind provider

        ARGUMENTS:
            - period
            - level (cscom|district|region) """

    class Meta:
        proxy = True

    def get_alert_id(self):
        """ should happen once per month only """
        return u'%s_%s' % (self.args.level, datetime.now().strftime('%d%m%Y'))

    def can_trigger(self, *args, **kwargs):
        # triggers happens if:
        # 1. Such alert has not been triggered
        # 2. Action period is not over
        # 2. We are in the next period as P
        try:
            time_is_over = eval('time_%s_over' \
                                % self.args.level)(period=self.args.period)
        except:
            return False
        return self.not_triggered \
               and not time_is_over \
               and self.args.period == current_reporting_period()

    def action(self):
        """ Send every reporter with an action left to do a reminder """

        today = date.today()

        level = self.args.level
        if not level:
            return False

        logger.info(u"Level: %s" % level)

        if level == 'cscom':
            message = _(u"[PNLP] Votre rapport mensuel paludisme est " \
                        "attendu au plus tard le %(date)s") \
                      % {'date': date(today.year, \
                                      today.month, 5).strftime('%x')}
            for cscom in cscom_without_report(self.args.period):
                contact = contact_for(cscom, recursive=False)
                if not contact or not contact.phone_number:
                    continue

                logger.info(u"Sending cscom text to %s" % contact.phone_number)
                send_sms(to=contact.phone_number, text=message)

            # end of CSCom section
            return

        for stat in level_statistics(self.args.period, level).values():

            contact = contact_for(stat['entity'], recursive=False)

            if not contact or not contact.phone_number:
                continue

            # nothing waiting validation.
            if not stat['unval']:
                continue

            logger.info(u"Sending %s text to %s" \
                        % (level, contact.phone_number))

            message = _(u"[PNLP] Vous avez %(unval)d rapports a valider " \
                        "au plus tard le %(date)s.") \
                      % {'unval': stat['unval'], \
                         'date': date(today.year, \
                                      today.month, 15).strftime('%x')}

            send_sms(to=contact.phone_number, text=message)


class EndOfMonth(Alert):

    """ Warn HOTLINE that new period is starting soon

        Last day of month
        1. send SMS to HOTLINE

        ARGUMENTS:
            - period """

    class Meta:
        proxy = True

    def get_alert_id(self):
        """ should happen once per month only """
        return datetime.now().strftime('%m%Y')

    def can_trigger(self, *args, **kwargs):
        # triggers happens if:
        # 1. Such alert has not been triggered
        # 2. We are in the next period as P (don't trigger is it's too late
        return self.not_triggered \
               and datetime.now() >= (self.args.period.end_on \
                                      - timedelta(days=2)) \
                and self.args.period == current_reporting_period()

    def action(self):
        """ send SMS to HOTLINE """

        message = _(u"[PNLP] La periode %(period)s va commencer. " \
                    "Il faut envoyer du credit aux utilisateurs.") \
                  % {'period': self.args.period.next()\
                                               .middle().full_name()}

        send_sms(to=settings.HOTLINE_NUMBER, text=message)
