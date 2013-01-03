#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

''' Common nosmsd handler for PNLP & UNFPA projects on same modem '''

from snisi_sms.malaria.malaria import malaria_handler
from snisi_sms.reproduction import dead_persons_handler
from snisi_sms.epidemiology.epidemiology import epidemiology_handler


def common_nosmsd_handler(message):

    keywords = {'palu': malaria_handler,
                'fnuap': dead_persons_handler,
                'epid': epidemiology_handler}

    for keyword, handler in keywords.items():
        if message.content.lower().startswith(keyword):
            return handler(message)
    # message.respond(u"Message non pris en charge.")
    return False
