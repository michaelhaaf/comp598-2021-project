import tweepy as tw
import pandas as pd

import argparse
import json
import os, sys

from dotenv import load_dotenv
from pathlib import Path

NUM_POSTS = 1000

load_dotenv()
API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

def api_setup():
    auth = tw.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tw.API(auth, wait_on_rate_limit=True)
    print(api.verify_credentials().screen_name)
    return api

    # eg search_query = "#covid19 -filter:retweets"
def twitter_fetch(api, query):
    print(f'Fetching {query} using api object {api}')
    tweets = tw.Cursor(api.search_tweets,
            q=query,
            lang="en").items(1000)
    return tweets


def tweets_to_df(api, tweets):
    df = pd.DataFrame()

    for tweet in tweets:
        hashtags = []
        try:
            for hashtag in tweet.entities["hashtags"]:
                hashtags.append(hashtag["text"])
            text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
        except:
            pass

        tweets_df = tweets_df.append(pd.DataFrame({'user_name': tweet.user.name,
                                                   'user_location': tweet.user.location,
                                                   'user_description': tweet.user.description,
                                                   'user_verified': tweet.user.verified,
                                                   'date': tweet.created_at,
                                                   'text': text,
                                                   'hashtags': [hashtags if hashtags else None],
                                                   'source': tweet.source}))
        tweets_df = tweets_df.reset_index(drop=True)


def main(args):
    api = api_setup()
    print(api)
    search_query = "#covid19 -filter:retweets"
    tweets = twitter_fetch(api, search_query)
    df = tweets_to_df(api, tweets)
    df.to_json(args.outputFile, indent=4) 


## Usage
# python3 collect_newest.py -o <output_file> -s <subreddit>
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
