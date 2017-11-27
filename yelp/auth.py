import os


def load_auth_from_env(client_key='YELP_CONSUMER_KEY',
                       client_secret='YELP_CONSUMER_SECRET',
                       resource_owner_key='YELP_TOKEN',
                       resource_owner_secret='YELP_TOKEN_SECRET'):
    for name in (client_key, client_secret, resource_owner_key, resource_owner_secret):
        yield os.environ[name]
