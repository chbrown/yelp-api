#!/usr/bin/env python
import argparse
import json
import oauth2
import os
import pprint
import requests
import sys
import urllib

parser = argparse.ArgumentParser(description='Yelp API v2 - Search',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# General Search Parameters
general = parser.add_argument_group('General Search Parameters')
general.add_argument('--term', type=str,
    help='''Search term (e.g. "food", "restaurants"). If term isn't included we search everything.''')
general.add_argument('--limit', type=int,
    help='''Number of business results to return''')
general.add_argument('--offset', type=int,
    help='''Offset the list of returned business results by this amount''')
general.add_argument('--sort', type=int,
    help='''Sort mode: 0=Best matched (default), 1=Distance, 2=Highest Rated. If the mode is 1 or 2 a search may retrieve an additional 20 businesses past the initial limit of the first 20 results. This is done by specifying an offset and limit of 20. Sort by distance is only supported for a location or geographic search. The rating sort is not strictly sorted by the rating value, but by an adjusted rating value that takes into account the number of ratings, similar to a bayesian average. This is so a business with 1 rating of 5 stars doesn't immediately jump to the top.''')
general.add_argument('--category_filter', type=str,
    help='''Category to filter search results with. See the list of supported categories. The category filter can be a list of comma delimited categories. For example, 'bars,french' will filter by Bars and French. The category identifier should be used (for example 'discgolf', not 'Disc Golf').''')
general.add_argument('--radius_filter', type=int,
    help='''Search radius in meters. If the value is too large, a AREA_TOO_LARGE error may be returned. The max value is 40000 meters (25 miles).''')
general.add_argument('--deals_filter', action='store_true',
    help='''Whether to exclusively search for businesses with deals''')

# Locale Parameters
locale = parser.add_argument_group('Locale Parameters')
locale.add_argument('--cc', type=str,
    help='''ISO 3166-1 alpha-2 country code. Default country to use when parsing the location field. United States = US, Canada = CA, United Kingdom = GB (not UK).''')
locale.add_argument('--lang', type=str,
    help='''ISO 639 language code (default=en). Reviews written in the specified language will be shown.''')
locale.add_argument('--lang_filter', action='store_true',
    help='''Whether to filter business reviews by the specified lang''')

# Specify Location by Geographical Bounding Box
boundingbox = parser.add_argument_group('Specify Location by Geographical Bounding Box')
boundingbox.add_argument('--bounds', type=str,
    help='''sw_latitude,sw_longitude|ne_latitude,ne_longitude''')

# Specify Location by Geographic Coordinate
geocoordinate = parser.add_argument_group('Specify Location by Geographic Coordinate')
geocoordinate.add_argument('--ll', type=str,
    help='''latitude,longitude,accuracy,altitude,altitude_accuracy''')

# Specify Location by Neighborhood, Address, or City
address = parser.add_argument_group('Specify Location by Neighborhood, Address, or City')
address.add_argument('--location', type=str,
    help='''Specifies the combination of "address, neighborhood, city, state or zip, optional country" to be used when searching for businesses.''')
address.add_argument('--cll', type=str,
    help='''An optional latitude, longitude parameter can also be specified as a hint to the geocoder to disambiguate the location text. The format for this is defined as: latitude,longitude''')

# Local flags:
local_flags = parser.add_argument_group('Local Flags')
local_flags.add_argument('--json', action='store_true',
    help='''Output business as json, one per line''')
local_flags.add_argument('--depaginate', action='store_true',
    help='''Start with limit =  through all the business as json, one per line''')

consumer = oauth2.Consumer(os.environ['YELP_CONSUMER_KEY'], os.environ['YELP_CONSUMER_SECRET'])
token = oauth2.Token(os.environ['YELP_TOKEN'], os.environ['YELP_TOKEN_SECRET'])

local_flags = ['json', 'depaginate']


def get(params, json_output=False):
    encoded_params = urllib.urlencode(params)
    url = 'http://api.yelp.com/v2/search?%s' % encoded_params
    print >> sys.stderr, 'url', url
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update({
        'oauth_nonce': oauth2.generate_nonce(),
        'oauth_timestamp': oauth2.generate_timestamp(),
        'oauth_token': token.key,
        'oauth_consumer_key': consumer.key})

    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    response = requests.get(signed_url)
    result = response.json()

    if json_output:
        for business in result['businesses']:
            print json.dumps(business)
    else:
        print pprint.pformat(result)


def main():
    opts = parser.parse_args()
    params = dict((k, v) for k, v in opts.__dict__.items() if v and k not in local_flags)

    if opts.depaginate:
        params['limit'] = 20
        for i in range(100):
            params['offset'] = i*params['limit']
            get(params, opts.json)
    else:
        get(params, opts.json)


if __name__ == '__main__':
    main()
