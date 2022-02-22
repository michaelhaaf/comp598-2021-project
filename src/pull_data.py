import requests
import json
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAGshWQEAAAAA7Ro%2FeM6XFAFeB%2B%2BdyJIC1OSTP1U%3DUurtolh5MUlnoNlus9TG1TzXOTe2JGqlVxdfCMyp2hFAA77Nic'

search_url = 'https://api.twitter.com/2/tweets/search/recent'

until_id_26 = '1464423352295165954'
until_id_27 = '1464706955130269702'
until_id_28 = '1465043882618540045'

def bearer_oauth(r):
  '''
  Method required by bearer token authentication.
  '''

  r.headers['Authorization'] = f'Bearer {bearer_token}'
  r.headers['User-Agent'] = 'comp599finalproj'
  return r

def connect_to_endpoint(url, until_id):
  # We want it to include either 'covid', 'vaccination', or a name-brand vaccine
  # For simplicity we consider the vaccines 'pfizer', 'moderna', 'astrazeneca'
  # Note that the API is case insensitive
  # Retweets are removed and lang is set to english as specified in the assignment

  query_params = {
    'query': f'(covid OR vaccination OR pfizer OR moderna OR astrazeneca) lang:en -is:retweet',
    'tweet.fields': 'created_at',
    'until_id': {until_id},
    'max_results': 100 # Maximum allowed for this level
  }


  response = requests.request('GET', search_url, auth=bearer_oauth, params=query_params)
  print(response.status_code)
  if response.status_code != 200:
    raise Exception(response.status_code, response.text)
  return response.json()


def main():
  # Need 1000 tweets: take 400/300/300 across 26/27/28
  # So we have 4 tweet ids from 11/26, 3 from 11/27, and 3 from 11/28
  # The only way to separate tweet dates in the basic API is by tweet id
  tweet_ids = [
    '1464423352295165954',
    '1464368398897459202',
    '1464414567828582401',
    '1464295440774582274', # end of day 1
    '1464475071146188322',
    '1464641601876148226',
    '1464706955130269702', # end of day 2
    '1465043882618540045',
    '1465120130757799943',
    '1465095692041564174'
  ]

  for i in range(10):
    file_to_write = os.path.join(parentdir, 'data', f'day_{i}.json')

    # If file exists don't resend request
    if os.path.isfile(file_to_write):
      continue

    json_response = connect_to_endpoint(search_url, tweet_ids[i])

    with open(file_to_write, 'w') as outfile:
      json.dump(json_response, outfile, indent=2)

if __name__ == '__main__':
  main()
