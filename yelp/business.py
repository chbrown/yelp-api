import json
import argparse
import urllib.request
import urllib.error
import urllib.parse
import oauth2


def request(host, path, url_params, consumer_key, consumer_secret, token, token_secret):
    """Returns response for API request."""
    # Unsigned URL
    encoded_params = ''
    if url_params:
        encoded_params = urllib.parse.urlencode(url_params)
    url = 'http://%s%s?%s' % (host, path, encoded_params)
    print('URL: %s' % (url,))

    # Sign the URL
    consumer = oauth2.Consumer(consumer_key, consumer_secret)
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                          'oauth_timestamp': oauth2.generate_timestamp(),
                          'oauth_token': token,
                          'oauth_consumer_key': consumer_key})

    token = oauth2.Token(token, token_secret)
    oauth_request.sign_request(
        oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()
    print('Signed URL: %s\n' % (signed_url,))

    # Connect
    try:
        conn = urllib.request.urlopen(signed_url, None)
        try:
            response = json.loads(conn.read())
        finally:
            conn.close()
    except urllib.error.HTTPError as error:
        response = json.loads(error.read())

    return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--consumer_key', required=True,
                        help='OAuth consumer key')
    parser.add_argument('-s', '--consumer_secret', required=True,
                        help='OAuth consumer secret')
    parser.add_argument('-t', '--token', required=True,
                        help='OAuth token')
    parser.add_argument('-e', '--token_secret', required=True,
                        help='OAuth token secret')
    parser.add_argument('-a', '--host', default='api.yelp.com',
                        help='Host')
    parser.add_argument('-i', '--id', required=True,
                        help='Business')
    parser.add_argument('-u', '--cc',
                        help='Country code')
    parser.add_argument('-n', '--lang',
                        help='Language code')

    opts = parser.parse_args()

    url_params = {}
    if opts.cc:
        url_params['cc'] = opts.cc
    if opts.lang:
        url_params['lang'] = opts.lang

    path = '/v2/business/{}'.format(opts.id)

    response = request(opts.host, path, url_params, opts.consumer_key,
                       opts.consumer_secret, opts.token, opts.token_secret)
    print(json.dumps(response, sort_keys=True, indent=2))
