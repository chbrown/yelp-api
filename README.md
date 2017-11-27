# Yelp API Examples

Prerequisites:

    pip install requests requests-oauthlib

And then put the following variables in your environment with `~/.bashrc` or something.

    YELP_CONSUMER_KEY
    YELP_CONSUMER_SECRET
    YELP_TOKEN
    YELP_TOKEN_SECRET


## Examples

Put the source code on the Python PATH:

    export PYTHONPATH=$(pwd)/yelp

Crawl all the restaurants within 20,000 ft of the center of Chicago, Illinois:

    python -m yelp.search --location "Chicago, IL" --radius_filter 20000 \
      --term "restaurants" --json --depaginate > restaurants.json

It will capture the full Yelp listing json objects, so that you can then sort:

    <restaurants.json json -C review_count rating name | sort -g

The `json` filtering + flattening command above can be fetched via `npm -g install json`.


## License

Copyright © 2013 Christopher Brown, [MIT Licensed](LICENSE),
except where Yelp!'s [original API repository](https://github.com/Yelp/yelp-api)
is licensed under different terms. (No license is included with that repository.)
