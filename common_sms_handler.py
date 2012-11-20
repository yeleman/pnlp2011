#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

''' Common nosmsd handler for PNLP & UNFPA projects on same modem '''

from pnlp_sms.palu import nosms_handler as pnlp_handler
from unfpa_sms import nosms_handler as unfpa_handler


def common_nosmsd_handler(message):

    keywords = {'palu': pnlp_handler,
                'fnuap': unfpa_handler}

    for keyword, handler in keywords.items():
        if message.content.lower().startswith(keyword):
            return handler(message)
    # message.respond(u"Message non pris en charge.")
    return False
