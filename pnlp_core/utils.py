#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import logging
import smtplib
import re

from django.core import mail
from django.conf import settings
from django.template import Template, loader, Context
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site, get_current_site

logger = logging.getLogger(__name__)


def send_email(recipients, message=None, template=None, context={}, \
               title=None, title_template=None, sender=None):
    """ forge and send an email message

        recipients: a list of or a string email address
        message: string or template name to build email body
        title: string or title_template to build email subject
        sender: string otherwise EMAIL_SENDER setting
        content: a dict to be used to render both templates

        returns: (success, message)
            success: a boolean if connecion went through
            message: an int number of email sent if success is True
                     else, an Exception """

    if not isinstance(recipients, (list, tuple)):
        recipients = [recipients]

    # remove empty emails from list
    # might happen everytime a user did not set email address.
    try:
        while True:
            recipients.remove(u"")
    except ValueError:
        pass

    # no need to continue if there's no recipients
    if recipients.__len__() == 0:
        return (False, ValueError(_(u"No Recipients for that message")))

    # no body text forbidden. most likely an error
    if not message and not template:
        return (False, ValueError(_(u"Unable to send empty email messages")))

    # build email body. rendered template has priority
    if template:
        email_msg = loader.get_template(template).render(Context(context))
    else:
        email_msg = message

    # if no title provided, use default one. empty title allowed
    if title == None and not title_template:
        email_subject = _(u"Message from %(site)s") \
                        % {'site': Site.objects.get_current().name}

    # build email subject. rendered template has priority
    if title_template:
        email_subject = loader.get_template(title_template)\
                                                      .render(Context(context))
    elif title != None:
        email_subject = title

    # title can't contain new line
    email_subject = email_subject.strip()

    # default sender from config
    if not sender:
        sender = settings.EMAIL_SENDER

    msgs = []
    for recipient in recipients:
        msgs.append((email_subject, email_msg, sender, [recipient]))

    try:
        mail.send_mass_mail(tuple(msgs), fail_silently=False)
        return (True, recipients.__len__())
    except smtplib.SMTPException as e:
        # log that error
        return (False, e)


def full_url(request=None, path=''):
    if path.startswith('/'):
        path = path[1:]
    return 'http%(ssl)s://%(domain)s/%(path)s' \
           % {'domain': get_current_site(request).domain, \
              'path': path, 'ssl': u"s" if settings.USE_HTTPS else u''}

ALL_COUNTRY_CODES = [1242, 1246, 1264, 1268, 1284, 1340, 1345, 1441, 1473, \
                     1599, 1649, 1664, 1670, 1671, 1684, 1758, 1767, 1784, \
                     1809, 1868, 1869, 1876, 1, 20, 212, 213, 216, 218, 220, \
                     221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, \
                     232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, \
                     243, 244, 245, 248, 249, 250, 251, 252, 253, 254, 255, \
                     256, 257, 258, 260, 261, 262, 263, 264, 265, 266, 267, \
                     268, 269, 27, 290, 291, 297, 298, 299, 30, 31, 32, 33, \
                     34, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, \
                     36, 370, 371, 372, 373, 374, 375, 376, 377, 378, 380, \
                     381, 382, 385, 386, 387, 389, 39, 40, 41, 420, 421, 423, \
                     43, 44, 45, 46, 47, 48, 49, 500, 501, 502, 503, 504, \
                     505, 506, 507, 508, 509, 51, 52, 53, 54, 55, 56, 57, 58, \
                     590, 591, 592, 593, 595, 597, 598, 599, 60, 61, 62, 63, \
                     64, 65, 66, 670, 672, 673, 674, 675, 676, 677, 678, 679, \
                     680, 681, 682, 683, 685, 686, 687, 688, 689, 690, 691, \
                     692, 7, 81, 82, 84, 850, 852, 853, 855, 856, 86, 870, \
                     880, 886, 90, 91, 92, 93, 94, 95, 960, 961, 962, 963, \
                     964, 965, 966, 967, 968, 970, 971, 972, 973, 974, 975, \
                     976, 977, 98, 992, 993, 994, 995, 996, 998]


def clean_phone_number(number):
    """ turns 21345678 into 12 34 56 78 """

    def is_int(number):
        if re.match(r'^[+|(]', number):
            return True
        if re.match(r'^\d{1,4}\.\d+$', number):
            return True
        return False

    def get_indicator(number):
        for indic in ALL_COUNTRY_CODES:
            if number.startswith(indic.__str__()):
                return indic.__str__()
        return ''

    if not isinstance(number, basestring):
        number = number.__str__()

    # cleanup markup
    clean_number = re.sub(r'[^\d]', '', number)

    # is in international format?
    if is_int(re.sub(r'[\-\s]', '', number)):
        h, indicator, clean_number = \
                            clean_number.partition(get_indicator(clean_number))
        return (indicator, clean_number)
    return (None, clean_number)

def get_autobot(self):
    from bolibana_auth.models import Provider
    return Provider.objects.get(user__username='autobot')
