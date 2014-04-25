ping cron
=========

## API

### Add url

    curl -X POST <address>/_ah/api/url/v1/add_url/ -d '{"url": "http://www.google.com"}' -H "Content-Type: application/json"

### Delete url

    curl -X POST <address>/_ah/api/url/v1/remove_url/ -d '{"url": "http://www.google.com"}' -H "Content-Type: application/json"
