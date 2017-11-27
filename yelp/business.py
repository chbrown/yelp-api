import logging
import argparse
import json
import requests
import requests_oauthlib

from .auth import load_auth_from_env


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', required=True,
                        help='Business')
    parser.add_argument('--cc',
                        help='Country code')
    parser.add_argument('--lang',
                        help='Language code')

    opts = parser.parse_args()

    params = {}
    if opts.cc:
        params['cc'] = opts.cc
    if opts.lang:
        params['lang'] = opts.lang

    auth = requests_oauthlib.OAuth1(*load_auth_from_env())

    response = requests.get('https://api.yelp.com/v2/business/{}'.format(opts.id),
                            params=params, auth=auth)
    result = response.json()
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
