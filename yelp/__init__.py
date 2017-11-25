import os
import sys
import oauth2
import requests
import urllib

consumer = oauth2.Consumer(os.environ['YELP_CONSUMER_KEY'], os.environ['YELP_CONSUMER_SECRET'])
token = oauth2.Token(os.environ['YELP_TOKEN'], os.environ['YELP_TOKEN_SECRET'])


def get(params):
    encoded_params = urllib.urlencode(params)
    url = 'http://api.yelp.com/v2/search?' + encoded_params
    print >> sys.stderr, 'url', url
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update({
        'oauth_nonce': oauth2.generate_nonce(),
        'oauth_timestamp': oauth2.generate_timestamp(),
        'oauth_token': token.key,
        'oauth_consumer_key': consumer.key,
    })

    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    response = requests.get(signed_url)
    return response.json()
