ping cron
=========

## API

### Add url

    curl -X POST <address>/_ah/api/url/v1/url/ -d '{"url": "http://www.google.com"}' -H "Content-Type: application/json"

### Delete url

    curl -X DELETE <address>/_ah/api/url/v1/url/ -d '{"url": "http://www.google.com"}' -H "Content-Type: application/json"
