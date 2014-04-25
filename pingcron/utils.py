# -*- coding: utf-8 -*-
import base64
import hashlib
import os
import re

SALT_MESSAGE = 'gA7YbaRDmHjx9SABp0UvKweE8dHnZ22fZWxf/bLlwUI='


def is_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain... # noqa
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return bool(regex.match(url))


def chunks(list, size):
    """ Yield successive sized chunks from list. """

    for i in xrange(0, len(list), size):
        yield list[i:i + size]


def getDigest(password, salt=SALT_MESSAGE):
    if not salt:
        salt = base64.b64encode(os.urandom(32))
    digest = hashlib.sha256(salt + password).hexdigest()
    for x in range(0, 100001):
        digest = hashlib.sha256(digest).hexdigest()
    return salt, digest


def isPassword(password, digest, salt=SALT_MESSAGE):
    return getDigest(password, salt)[1] == digest
