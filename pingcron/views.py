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
        self.response.write('Hello, World!')

        template = JINJA_ENVIRONMENT.get_template('hello.html')
        pingurls = [p.to_dict() for p in PingUrl.query()]
        rendered_page = template.render(pingurls=pingurls)

        self.response.write(rendered_page)


class PingPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        self.response.write('Hello, World!')

        template = JINJA_ENVIRONMENT.get_template('hello.html')
        rendered_page = template.render(r=1)

        self.response.write(rendered_page)
        for pingurl in PingUrl.query():
            try:
                response = requests.get(pingurl.url)
                logger.info(response.status_code)

                pingurl.status_code = response.status_code
                pingurl.headers = json.dumps(dict(response.headers))
                pingurl.updated_date = datetime.now()
                pingurl.put()
                logger.info('{} {}'.format(pingurl.status, pingurl.url))

            except requests.exceptions.MissingSchema, e:
                logger.info('cannot ping {} {}'.format(pingurl.url, e))
            except requests.exceptions.ConnectionError, e:
                logger.info('cannot ping {} {}'.format(pingurl.url, e))
            except Exception, e:
                logger.warning('Unknown error {}'.format(e))

        template = JINJA_ENVIRONMENT.get_template('hello.html')
        pingurls = [p.to_dict() for p in PingUrl.query()]
        rendered_page = template.render(pingurls=pingurls)

        self.response.write(rendered_page)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/ping', PingPage),
], debug=True)
