#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from nosms.utils import send_sms
from django_conditions.models import ConditionClass
from django_conditions.decorators import initial_action

from pnlp_core.models import MalariaReport
from pnlp_core.data import contact_for
from pnlp_core.utils import send_email


class MalariaReportCreated(ConditionClass, MalariaReport):
    """ MalariaReport has been created.

    Both for Source and Aggregated Reports """

    class Meta:
        proxy = True

    exists_when = models.Q(_status=MalariaReport.STATUS_CREATED)

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
