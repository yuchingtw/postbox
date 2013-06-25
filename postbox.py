#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getpass import getpass
from smtplib import SMTP

class Postbox(object):

    host = None
    port = None
    user = None
    password = None
    tls = True
    prompt_user = None
    prompt_password = 'password? '
    debuglevel = None

    def __init__(self, **attrs):

        for key, value in attrs.items():
            setattr(self, key, value)

        self.server = SMTP(self.host, self.port)

        if self.debuglevel:
            self.server.set_debuglevel(self.debuglevel)

        if self.tls:
            self.server.starttls()

        if not self.user and self.prompt_user:
            self.user = raw_input(self.prompt_user)

        if self.user and not self.password and self.prompt_password:
            self.password = getpass(self.prompt_password)

        if self.user and self.password:
            self.server.login(self.user, self.password)

    def send(self, body, **headers_dict):

        sendmail_args = {'from': '', 'to': ''}
        headers = []

        for key, value in headers_dict.items():

            key = key.rstrip('_').lower().replace('_', '-')
            if key in sendmail_args:
                sendmail_args[key] = value

            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = ', '.join(value)

            headers.append('%s: %s' % (key, value))

        headers = '\r\n'.join(headers)

        self.server.sendmail(
            sendmail_args['from'],
            sendmail_args['to'],
            '%s\r\n\r\n%s' % (headers, body)
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.server.quit()

class Gmail(Postbox):
    host = 'smtp.gmail.com'
    port = '587'