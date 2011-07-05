#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from nosms.utils import send_sms
from django_conditions.models import ConditionClass
from django_conditions.decorators import initial_action

from pnlp_core.models import MalariaReport
from bolibana_auth.models import Provider, Access
from bolibana_reporting.models import Entity
from pnlp_core.data import contact_for
from pnlp_core.utils import send_email, full_url


class MalariaReportCreated(ConditionClass, MalariaReport):
    """ MalariaReport has been created.

    Both for Source and Aggregated Reports """

    class Meta:
        proxy = True

    exists_when = models.Q(_status=MalariaReport.STATUS_CREATED, entity__level__gte=1)

    @initial_action
    def notify_superior_level(self):
        """ retrieve phone number or email of parent entity contact """

        # national level doesn't trigger anything
        if not self.entity.parent:
            return

        contact = contact_for(self.entity.parent)

        message = _(u"[INCOMING] The report %(receipt)s from %(entity)s " \
                    "has been received. Your action is required.") \
                  % {'receipt': self.receipt, 'entity': self.entity}

        if contact.phone_number:
            send_sms(contact.phone_number, message)
        elif contact.email:
            send_email(contact.email, message, \
                       _(u"[PNLP] New report received!"))
        else:
            send_email(settings.HOTLINE_EMAIL, message, \
                       _(u"[PNLP] Unable to send report notification " \
                         "to %(contact)s") \
                       % {'contact': contact.name_access()})


class NationalReportCreated(ConditionClass, MalariaReport):

    class Meta:
        proxy = True

    # we will *always* create those conditions manually.
    exists_when = models.Q(_status=MalariaReport.STATUS_CREATED, entity__level=0)

    @initial_action
    def warn_people(self):
        """ Let everybody know the report is ready """
        # auto-validate the report as there is no one to do it.
        self.status = self.STATUS_VALIDATED

        # send emails
        ct, oi = Access.target_data(Entity.objects.get(slug='mali'))
        providers = Provider.active.select_related().filter(user__email__isnull=False, access__in=list(Access.objects.filter(content_type=ct, object_id=oi))).values_list('user__email', flat=True)

        sent, sent_message = send_email(recipients=providers, \
                                context={'report': self, \
                                         'report_url': full_url(path=reverse('raw_data', kwargs={'entity_code': 'mali', 'period_str': '062011'})), \
                                         'url': full_url()},
                               template='emails/mali_report_available.txt', \
                     title_template='emails/title.mali_report_available.txt')
