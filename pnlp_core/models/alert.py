#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from pnlp_core.data import (time_cscom_over, \
                            current_reporting_period, \
                            contact_for)
from pnlp_core.models import MalariaReport
from bolibana_reporting.models import Entity
from nosms.utils import send_sms


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
        instance = cls(content_type=cls.get_ct(), created=datetime.now())
        instance.args = Options(**kwargs)
        return instance

    def triggered(self):
        """ if this alert has been triggered (exists in DB) """
        return self.objects.count(id=self.alert_id(), \
                                  content_type=self.content_type) > 0

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


class EndOfCSComPeriod(Alert):

    class Meta:
        proxy = True

    def get_alert_id(self):
        return self.args.period.middle().strftime('%m%Y')

    def can_trigger(self, *args, **kwargs):
        # triggers happens if:
        # 1. CSCom period for P is over
        # 2. Such alert has not been triggered
        # 3. We are in the next period as P (don't trigger is it's too late
        return time_cscom_over(period=self.args.period) \
               and self.not_triggered \
               and period == current_reporting_period()

    def action(self):
        """ Let the Entity's provider that they missed the sending period

            and that this will be notified to PNLP """

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
                              "rapport. Vous devez les valider avant le 15.")
            else:
                msg_unval = u""

            if e['unsent']:
                msg_unsent = _(u"%(nb)s n'ont pas envoyer leur rapport " \
                               "mensuel dans les temps!")
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


# district or region
# validate non-validated reports and create aggregated
# let region know there are reports to validate

# regions created
# create Mali report based on region ones
