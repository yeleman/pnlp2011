#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import logging
from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

from pnlp_core.data import (time_cscom_over, time_district_over, \
                            time_region_over, current_reporting_period, \
                            contact_for)
from pnlp_core.models import MalariaReport
from bolibana_reporting.models import Entity
from nosms.utils import send_sms
from bolibana_auth.models import Provider, Access
from pnlp_core.utils import send_email, full_url

logger = logging.getLogger(__name__)


class Options(dict, object):

    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs)

    def __getattribute__(self, name):
        try:
            return self[name]
        except:
            return None


class Alert(models.Model):

    class Meta:
        app_label = 'pnlp_core'

    alert_id = models.CharField(max_length=100, primary_key=True)
    created = models.DateTimeField(_(u"created"), auto_now_add=True)
    content_type = models.ForeignKey(ContentType)

    def __unicode__(self):
        return u"Alert.%(ct)s/%(id)s" \
               % {'ct': self.content_type.model.title(), \
                  'id': self.alert_id}

    @classmethod
    def create(cls, *args, **kwargs):
        instance = cls(content_type=cls.get_ct(), \
                       created=datetime.now())
        if not 'persist' in kwargs:
            kwargs['persist'] = True
        instance.args = Options(**kwargs)
        instance.alert_id = instance.get_alert_id()
        return instance

    def triggered(self):
        """ if this alert has been triggered (exists in DB) """
        return self.__class__.objects.filter(alert_id=self.get_alert_id(), \
                                  content_type=self.content_type).count() > 0

    @property
    def aid(self):
        """ returns the generated Alert ID for use before creating alert """
        return self.get_alert_id()

    @property
    def not_triggered(self):
        """ shortcut property to know if alert has been triggered already """
        return not self.triggered()

    def can_trigger(self, *args, **kwargs):
        """ override this to set whether or not alert should be triggered """
        return False

    @classmethod
    def get_ct(cls):
        """ returns the ContentType for this class """

        ctype, created = ContentType.objects.get_or_create(
            app_label=cls._meta.app_label,
            model=cls._meta.object_name.lower(),
            defaults={'name': smart_unicode(cls._meta.verbose_name_raw)})

        return ctype

    def trigger(self, *args, **kwargs):
        """ call this to trigger your alert's action """
        self.action()
        if self.args.persist:
            self.save()

    def action(self):
        """ your code for that alert """
        pass

    def save(self, *args, **kwargs):
        if not self.alert_id:
            self.alert_id = self.get_alert_id()
        try:
            if not self.content_type:
                self.content_type = self.get_ct()
        except:
            self.content_type = self.get_ct()
        super(Alert, self).save(*args, **kwargs)


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
            send_email(contact.email, message, \
                       _(u"[PNLP] Nouveau rapport recu!"))
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
               and period == current_reporting_period()

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

            message = _(u"[PNLP] %(unval)s%(unsent)") \
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
                else:
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
               and period == current_reporting_period()

    def action(self):
        """ Validate remaining reports and inform region """

        # retrieve autobot provider if possible
        try:
            author = Provider.active.get(user__username='autobot')
        except:
            pass

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
            rauthor = contact_for(entity) if not author else author
            report = MalariaReport.create_aggregated(period, entity, rauthor)
            # region auto-validates their reports
            if not self.args.is_district:
                report.status = MalariaReport.STATUS_VALIDATED
                report.save()

        # region-only section
        # create national report
        if not self.args.is_district:
            mali = Entity.objects.get(slug='mali')
            rauthor = author if author else Provider.objects.all()[0]
            report = MalariaReport.create_aggregated(period, mali, rauthor)

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
