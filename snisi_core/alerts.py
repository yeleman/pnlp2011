#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import logging
from datetime import datetime, date, timedelta

import reversion
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from nosmsd.utils import send_sms

from bolibana.models.Entity import Entity
from bolibana.models.Provider import Provider
from bolibana.models.Access import Access
from bolibana.tools.utils import get_autobot, send_email, full_url
from snisi_core.data import (time_cscom_over, time_district_over,
                            time_region_over, current_reporting_period,
                            contact_for)
from snisi_core.models.alert import Alert
from snisi_core.models.MalariaReport import MalariaR, AggMalariaR

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

        message = u"[PNLP] Le rapport %(receipt)s de %(entity)s " \
                  u"a ete recu. Vous devez le valider." \
                  % {'receipt': report.receipt, 'entity': report.entity}

        # if contact.phone_number:
        #     send_sms(contact.phone_number, message)
        if contact.email:
            send_email(recipients=contact.email, message=message, \
                       title=u"[PNLP] Nouveau rapport recu!")
        else:
            send_email(settings.HOTLINE_EMAIL, message, \
                       u"[PNLP] Unable to send report notification " \
                       u"to %(contact)s" \
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

        for report in MalariaR.unvalidated\
                                   .filter(period=self.args.period):

            # entity has no parent. Either Mali or error
            if not report.entity.parent:
                # should never happen but we never know
                # drop if entity has no parent.
                if not report.entity.level == 0:
                    return

                # we now have a national report
                logger.info(u"Report %s found." % report)
                report._status = MalariaR.STATUS_VALIDATED
                with reversion.create_revision():
                    report.save()
                    reversion.set_user(get_autobot().user)
                    #report.save()

                # send emails
                ct, oi = Access.target_data(Entity.objects.get(slug='mali'))
                nat_access = list(Access.objects.filter(content_type=ct, \
                                                        object_id=oi))
                providers = list(Provider.active\
                                    .select_related()\
                                    .filter(user__email__isnull=False, \
                                            access__in=nat_access)\
                                    .values_list('user__email', flat=True))

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
        message = u"[PNLP] Vous n'avez pas envoye votre rapport mensuel." \
                    " Il est desormais trop tard pour l'envoyer. " \
                    "Vos donnees ne seront donc pas integrees."
        for contact in [contact_for(entity, recursive=False) \
                        for entity in mobile_entity_gen(self.get_bad_cscom())]:
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
                msg_unval = u"%(nb)s de vos CSCom ont envoye leur " \
                            u"rapport. Vous devez les valider avant le 15." \
                            % {'nb': e['unval']}
            else:
                msg_unval = u""

            if e['unsent']:
                msg_unsent = u"%(nb)s n'ont pas envoye leur rapport " \
                             u"mensuel dans les temps!" % {'nb': e['unsent']}
            else:
                msg_unsent = u""

            # add space before second sentence if both
            if e['unval'] and e['unsent']:
                msg_unsent = u" %s" % msg_unsent

            message = u"[PNLP] %(unval)s%(unsent)s" \
                      % {'unval': msg_unval, 'unsent': msg_unsent}

            send_sms(to=contact.phone_number, text=message)

    def get_all_district(self):
        districts = {}
        unval = [r.entity for r \
                          in MalariaR.unvalidated.select_related()\
                                      .filter(period=self.args.period, \
                                              type=MalariaR.TYPE_SOURCE)]
        unsent = self.get_bad_cscom()

        def increment(entities, cat):
            for e in entities:
                try:
                    districts[e.parent.slug][cat]
                except:
                    districts[e.parent.slug] = {'entity': e.parent, \
                                                'unval': 0, 'unsent': 0}
                districts[e.parent.slug][cat] += 1
        increment(unval, 'unval')
        increment(unsent, 'unsent')
        return districts

    def get_bad_cscom(self):
        reported = MalariaR.objects.select_related()\
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
        prefix = 'district' if self.args.is_district else 'region'
        return '%s_%s' % (prefix, self.args.period.middle().strftime('%m%Y'))

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
        for report in MalariaR.unvalidated\
                                   .filter(period=self.args.period, \
                                           entity__type__slug=validate_level):
            report._status = MalariaR.STATUS_VALIDATED
            if author:
                report.modified_by = author
            report.modified_on = datetime.now()
            with reversion.create_revision():
                report.save()
                if author:
                    reversion.set_user(author.user)
                else:
                    reversion.set_user(get_autobot().user)
                #report.save()

        # create aggregated reports
        for entity in Entity.objects.filter(type__slug=aggregate_level):
            if entity.snisi_core_malariar_reports\
                     .filter(period=self.args.period).count() > 0:
                continue
            rauthor = contact_for(entity) if not author else author
            logger.info(u"Creating Aggregated report for %s" % entity)
            report = AggMalariaR.create_from(self.args.period, \
                                                     entity, rauthor)
            # region auto-validates their reports
            if not self.args.is_district:
                report._status = MalariaR.STATUS_VALIDATED
                #report.save()
                with reversion.create_revision():
                    report.save()
                    reversion.set_user(rauthor.user)

        # region-only section
        # create national report
        mali = Entity.objects.get(slug='mali')
        if not self.args.is_district \
           and mali.snisi_core_malariar_reports\
                   .filter(period=self.args.period).count() == 0:
            rauthor = author if author else get_autobot()
            logger.info(u"Creating National report")
            report = AggMalariaR.create_from(self.args.period, \
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

            nb_reports = MalariaR.unvalidated\
                                   .filter(period=self.args.period, \
                                           entity__type__slug='district', \
                                           entity__parent=region).count()

            message = u"[PNLP] La periode de validation CSRef est " \
                      u"terminee. Vous avez %(nb)d rapports de " \
                      u"CSRef a valider." % {'nb': nb_reports}
            email_title = u"[PNLP] Fin de la periode de validation CSRef"

            if not contact.email:
                continue
            send_email(contact.email, message=message, title=email_title)
            # send_sms(to=contact.phone_number, text=message)


def level_statistics(period, level):
    """ district slug indexed hash of {'entity': district, 'unval': x}

        representing the number of unvalidated reports for the district """
    entities = {}
    sublevel = 'cscom' if level == 'district' else 'district'
    unval = [r.entity for r \
                      in MalariaR.unvalidated.select_related()\
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
    reported = MalariaR.objects.select_related()\
                                    .filter(period=period, \
                                            entity__type__slug='cscom')\
                                    .values_list('entity__id', flat=True)
    return list(Entity.objects.filter(~models.Q(pk__in=reported), \
                                      type__slug='cscom'))


def mobile_entity_gen(entities):
    """ Filter on Niono/Macina (mobile users) """
    for entity in entities:
        try:
            if entity.parent.slug in ('nion', 'maci'):
                yield entity
        except:
            pass


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
        """ should happen once per day only """
        now = datetime.now()
        # CSCOM: send 2 SMS: 1st, 4th, 5th
        if self.args.level == 'cscom':
            if now.day <= 3:
                fmt = now.strftime('01%m%Y')
            else:
                fmt = now.strftime('04%m%Y')
        # DISTICT: send 1 SMS: 6th
        elif self.args.level == 'district':
            fmt = now.strftime('10%m%Y')
        # REGION: send 1 SMS: 16th
        elif self.args.level == 'region':
            fmt = now.strftime('20%m%Y')
        return u'%s_%s' % (self.args.level, fmt)

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
        now = datetime.now()
        return self.not_triggered \
               and now.day >= int(self.get_alert_id()[-8:-6]) \
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
            message = u"[PNLP] Votre rapport mensuel paludisme est " \
                      u"attendu au plus tard le %(date)s" \
                      % {'date': date(today.year, \
                                      today.month, 5).strftime('%x')}
            for cscom in mobile_entity_gen(cscom_without_report(self.args.period)):
                contact = contact_for(cscom, recursive=False)
                if not contact or not contact.phone_number:
                    continue
                # CSCOM: only cellphone transmiting ones.
                if not cscom.parent.slug in ('nion', 'maci'):
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

            dom = 15 if level == 'district' else 25

            message = u"[PNLP] Vous avez %(unval)d rapports a valider " \
                      u"au plus tard le %(date)s." \
                      % {'unval': stat['unval'], \
                         'date': date(today.year, \
                                      today.month, dom).strftime('%x')}
            email_title = u"[PNLP] Rapports a valider"
            # send_sms(to=contact.phone_number, text=message)
            if not contact.email:
                continue
            sent, sent_message = send_email(recipients=contact.email,
                       message=message, title=email_title)


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
                                      - timedelta(days=1)) \
                and self.args.period == current_reporting_period()

    def action(self):
        """ send SMS to HOTLINE """

        message = u"[PNLP] La periode %(period)s va commencer. " \
                  u"Il faut s'occuper de la surveillance de la collecte " \
                  u"des donnees primaires." \
                  % {'period': self.args.period.next()\
                                               .full_name()}

        send_sms(to=settings.HOTLINE_NUMBER, text=message)

        # malitel_url = full_url(path=reverse('malitel'))
        title = u"[PNLP] La période va commencer."
        # sent, sent_message = send_email(recipients=settings.HOTLINE_EMAIL, \
        #                                 template='emails/send_airtime.txt', \
        #                                 context={'url': malitel_url}, \
        #                                 title=title)
        sent, sent_message = send_email(recipients=settings.HOTLINE_EMAIL, \
                                        message=message, \
                                        title=title)
