# -*- coding: utf-8 -*-
from protorpc import remote
from models import PingUrl
import endpoints
import logging


logger = logging.getLogger(__name__)
package = 'pingcron'

QUERY_LIMIT = 50


@endpoints.api(name='url', version='v1', description='Ping url API')
class PingUrlApi(remote.Service):

    @PingUrl.method(path='url', http_method='POST', name='pingurl.insert')
    def PingUrlInsert(self, pingurl):
        pingurl.status = PingUrl.STATUS_CHOICE['PENDING']
        pingurl.put()
        return pingurl

    @PingUrl.query_method(
        limit_default=QUERY_LIMIT,
        path='url', name='pingurl.list')
    def PingUrlList(self, query):
        logger.info(query)
        return query


APPLICATION = endpoints.api_server([PingUrlApi])
