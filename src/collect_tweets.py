import tweepy as tw
import pandas as pd

import argparse
import json
import os, sys
from datetime import datetime, timedelta

from dotenv import load_dotenv
from pathlib import Path


NUM_TWEETS = 1000
API_LIMIT = 50 # reduced by factor of two, just in case
WINDOW_SIZE = 3 # in days

load_dotenv()
API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')


def client_setup():
    client = tw.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True)
    return client


def twitter_fetch(client, query):
    print(f'Fetching {query} using api object {client}')
    tweet_search = tw.Paginator(client.search_recent_tweets,
            query=query,
            start_time=datetime.now() - timedelta(days=WINDOW_SIZE),
            max_results=API_LIMIT
            ).flatten(limit=NUM_TWEETS)
    return tweet_search


def tweets_to_dict(tweets):
    print("Collecting tweets. Might be paginating; usually takes less than a minute...")
    return {tweet.id: tweet.text for tweet in tweets}


def build_query():
    vaccine_brands = ["pfizer", "moderna", "astrazeneca"]
    key_words = ["covid", "vaccination"]
    params = " OR ".join(vaccine_brands + key_words)
    return f"({params}) lang:en -is:retweet"

def main(args):
    client = client_setup()
    search_query = build_query()
    tweets = twitter_fetch(client, search_query)
    output_dict = tweets_to_dict(tweets)
    with open(args.outputFile, "w") as fh:
        json.dump(output_dict, fh, indent=4)


## Usage
# python3 collect_newest.py -o <output_file> 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='collects 1000 tweets and stores them in a named file')
    parser.add_argument('-o',
            required=True,
            help='output json file (needs to be .json)',
            type=str,
            dest='outputFile'
            )
    args = parser.parse_args()
    main(args)
