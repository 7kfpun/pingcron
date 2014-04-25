# -*- coding: utf-8 -*-
from endpoints_proto_datastore.ndb import EndpointsModel
from google.appengine.ext import ndb
from utils import is_url
import logging

logger = logging.getLogger(__name__)


class PingUrl(EndpointsModel):
    """ User models."""

    _message_fields_schema = ('url', 'security_code')

    STATUS_CHOICE = dict([
        ('SUCCESS', 'SUCCESS'),
        ('PENDING', 'PENDING'),
        ('FAIL', 'FAIL')
    ])

    def validate_url(self, value):
        if not is_url(value):
            raise Exception('Not an url')
        #pingurl = PingUrl.query()
        #if pingurl.filter(PingUrl.url == value).count():
            #raise Exception('Url exists!')
        return value

    url = ndb.StringProperty(required=True, validator=validate_url)
    security_code = ndb.StringProperty()
    status = ndb.StringProperty(
        default='PENDING', choices=STATUS_CHOICE.keys(),
    )
    status_code = ndb.IntegerProperty()
    headers = ndb.TextProperty()
    is_deleted = ndb.BooleanProperty(default=False)
    created_datetime = ndb.DateTimeProperty(auto_now_add=True)
    updated_datetime = ndb.DateTimeProperty()
    last_success_datetime = ndb.DateTimeProperty()
    fail_from_datetime = ndb.DateTimeProperty()
