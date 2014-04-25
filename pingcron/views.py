# -*- coding: utf-8 -*-
from datetime import datetime
from models import PingUrl
import jinja2
import json
import logging
import os
import requests
import webapp2

logger = logging.getLogger(__name__)

NUMBER_OF_FETCH = 1000

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__), "templates"),
    ),
    extensions=[
        'jinja2.ext.i18n',
        'jinja2.ext.autoescape',
    ]
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'

        template = JINJA_ENVIRONMENT.get_template('index.html')
        pingurls = [p.to_dict() for p in
                    PingUrl.query(PingUrl.is_deleted != True)]
        rendered_page = template.render(pingurls=pingurls)

        self.response.write(rendered_page)


class PingPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'

        for pingurl in PingUrl.query(
            PingUrl.is_deleted != True
        ).order(
            PingUrl.is_deleted, PingUrl.updated_datetime
        ).fetch(NUMBER_OF_FETCH):
            try:
                response = requests.get(pingurl.url)
                logger.info(response.status_code)

            except Exception, e:
                pingurl.headers = str(e.message)
                pingurl.fail_from_datetime = datetime.now()
                logger.warning('Unknown error {}'.format(e))

            else:
                pingurl.status_code = response.status_code
                pingurl.headers = json.dumps(dict(response.headers))
                if 199 < response.status_code < 300:
                    pingurl.last_success_datetime = datetime.now()
                else:
                    pingurl.fail_from_datetime = datetime.now()
                logger.info('{} {}'.format(pingurl.status, pingurl.url))

            finally:
                pingurl.updated_date = datetime.now()
                pingurl.put()

        template = JINJA_ENVIRONMENT.get_template('index.html')
        pingurls = [
            p.to_dict() for p in PingUrl.query(PingUrl.is_deleted != True)]
        rendered_page = template.render(pingurls=pingurls)

        self.response.write(rendered_page)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/ping', PingPage),
], debug=True)

# pymode:lint_ignore=E712
