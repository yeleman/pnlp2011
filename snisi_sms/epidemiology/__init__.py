#!/usr/bin/env python
# encoding: utf-8
# maintainer: rgaudin

import logging
import locale
import re

from django.conf import settings

from epidemiology import epidemiology

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, settings.DEFAULT_LOCALE)


def epidemiology_handler(message):
    """ FNUAP SMS router """
    def main_epid_handler(message):
        keyword = 'epid'
        commands = {
            'epid': epidemiology}

        if message.content.lower().startswith('fnuap '):
            for cmd_id, cmd_target in commands.items():
                command = '%s %s' % (keyword, cmd_id)
                if message.content.lower().startswith(command):
                    n, args = re.split(r'^%s\s?' \
                                       % command,
                                         message.content.lower().strip())
                    return cmd_target(message,
                                      args=args,
                                      sub_cmd=cmd_id,
                                      cmd=command)
        else:
            return False

    if main_epid_handler(message):
        message.status = message.STATUS_PROCESSED
        message.save()
        logger.info(u"[HANDLED] msg: %s" % message)
        return True
    logger.info(u"[NOT HANDLED] msg : %s" % message)
    return False

