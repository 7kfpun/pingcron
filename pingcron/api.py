# -*- coding: utf-8 -*-
from protorpc import remote
from models import PingUrl
from utils import getDigest, isPassword
import endpoints
import logging


logger = logging.getLogger(__name__)
package = 'pingcron'

QUERY_LIMIT = 100


@endpoints.api(name='url', version='v1', description='Ping url API')
class PingUrlApi(remote.Service):

    @PingUrl.method(path='add_url', http_method='POST', name='pingurl.insert')
    def PingUrlInsert(self, pingurl):
        security_code = pingurl.security_code
        pingurl.status = PingUrl.STATUS_CHOICE['PENDING']
        pingurl.security_code = getDigest(security_code)[1]
        pingurl.is_deleted = False
        pingurl.put()
        pingurl.security_code = security_code
        return pingurl

    @PingUrl.method(path='delete_url',
                    http_method='POST', name='pingurl.delete')
    def PingUrlDelete(self, pingurl):
        security_code = pingurl.security_code
        delete = False
        for pingurl in PingUrl.query(
            PingUrl.url == pingurl.url,
        ):
            if isPassword(security_code, pingurl.security_code):
                pingurl.is_deleted = True
                pingurl.put()
                delete = True

        assert delete
        return pingurl

    @PingUrl.query_method(
        limit_default=QUERY_LIMIT, path='url', name='pingurl.list',
        collection_fields=('url',))
    def PingUrlList(self, query):
        logger.info(query)
        return query


APPLICATION = endpoints.api_server([PingUrlApi])
