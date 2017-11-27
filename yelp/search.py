import logging
import argparse
import json
import requests
import requests_oauthlib

from .auth import load_auth_from_env


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def iter_businesses(auth, offset=0, limit=20, **kwargs):
    params = dict(kwargs, offset=offset, limit=limit)
    response = requests.get('https://api.yelp.com/v2/search', params=params, auth=auth)
    result = response.json()
    businesses = result['businesses']
    logger.info('Fetched %d-%d of %d results (%d businesses)',
                 offset, offset + limit, result['total'], len(businesses))
    for business in businesses:
        yield business
    # continue with next page
    if businesses:
        for business in iter_businesses(auth, offset=offset + limit, limit=limit, **kwargs):
            yield business


def main():
    parser = argparse.ArgumentParser(
        description='Yelp API v2 - Search API')

    # General Search Parameters
    general = parser.add_argument_group('General Search Parameters')
    general.add_argument('--term', type=str,
                         help='''Search term (e.g. "food", "restaurants"). If term isn't included we search everything.''')
    general.add_argument('--limit', type=int,
                         help='''Number of business results to return''')
    general.add_argument('--offset', type=int,
                         help='''Offset the list of returned business results by this amount''')
    general.add_argument('--sort', type=int, choices={0, 1, 2},
                         help='''Sort mode: 0=Best matched (default), 1=Distance, 2=Highest Rated. If the mode is 1 or 2 a search may retrieve an additional 20 businesses past the initial limit of the first 20 results. This is done by specifying an offset and limit of 20. Sort by distance is only supported for a location or geographic search. The rating sort is not strictly sorted by the rating value, but by an adjusted rating value that takes into account the number of ratings, similar to a bayesian average. This is so a business with 1 rating of 5 stars doesn't immediately jump to the top.''')
    general.add_argument('--category_filter', type=str,
                         help='''Category to filter search results with. See the list of supported categories. The category filter can be a list of comma delimited categories. For example, 'bars,french' will filter by Bars and French. The category identifier should be used (for example 'discgolf', not 'Disc Golf').''')
    general.add_argument('--radius_filter', type=int,
                         help='''Search radius in meters. If the value is too large, a AREA_TOO_LARGE error may be returned. The max value is 40000 meters (25 miles).''')
    general.add_argument('--deals_filter', action='store_true',
                         help='''Whether to exclusively search for businesses with deals''')

    # Location parameters
    location = parser.add_argument_group('Methods of Specifying Location',
        description='''There are three available methods to specify location in a search. The location is a required parameter, and exactly one of these methods should be used for a request.''')
    address = parser.add_argument_group('Specify Location by Neighborhood, Address, or City')
    address.add_argument('--location', type=str,
                         help='''Specifies the combination of "address, neighborhood, city, state or zip, optional country" to be used when searching for businesses.''')
    address.add_argument('--cll', type=str,
                         help='''An optional latitude, longitude parameter can also be specified as a hint to the geocoder to disambiguate the location text. The format for this is defined as: latitude,longitude''')
    boundingbox = parser.add_argument_group('Specify Location by Geographical Bounding Box')
    boundingbox.add_argument('--bounds', type=str,
                             help='''sw_latitude,sw_longitude|ne_latitude,ne_longitude''')
    geocoordinate = parser.add_argument_group('Specify Location by Geographic Coordinate')
    geocoordinate.add_argument('--ll', type=str,
                               help='''The geographic coordinate format is defined as: latitude,longitude,accuracy,altitude,altitude_accuracy (only latitude and longitude are required)''')

    # Locale Parameters
    locale = parser.add_argument_group('Locale Parameters')
    locale.add_argument('--cc', type=str,
                        help='''ISO 3166-1 alpha-2 country code. Default country to use when parsing the location field. United States = US, Canada = CA, United Kingdom = GB (not UK).''')
    locale.add_argument('--lang', type=str,
                        help='''ISO 639 language code (default=en). Reviews written in the specified language will be shown.''')

    opts = parser.parse_args()
    params = {k: v for k, v in opts.__dict__.items() if v}

    auth = requests_oauthlib.OAuth1(*load_auth_from_env())

    for business in iter_businesses(auth, **params):
        print(json.dumps(business))


if __name__ == '__main__':
    main()
