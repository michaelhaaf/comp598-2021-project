import argparse
import json
import os, sys
import random
import csv
from pathlib import Path


def main(args):
    
    # process input file
    print(f"Loading from {args.json_file}...")
    with open(args.json_file, "r") as in_file:
        input_data = json.load(in_file)

    # Write tsv file
    print(f"Writing to {args.out_file}...")
    with safe_open(args.out_file, 'w') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['id', 'tweet', 'coding', 'sentiment'])
        for tweet_id, tweet in input_data.items():
            tsv_writer.writerow([tweet_id, tweet, '', ''])

    print("Finished!")
    

# helper method inspired by: https://stackoverflow.com/a/23794010
# Open "path" for writing, creating any parent directories as needed.
def safe_open(filename, mode):
    path = Path(filename).resolve()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, mode)


## Usage
# python3 extract_to_tsv.py -o <out_file> -i <json_file> 
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='accepts json file of tweetid/tweet pairs from twitter, outputs to tsv ready for annotation')
    parser.add_argument('-o',
            required=True,
            help='output tsv file',
            type=str,
            dest='out_file'
            )
    parser.add_argument('-i',
            required=True,
            help='input json file',
            type=str,
            dest='json_file'
            )
    args = parser.parse_args()

    main(args)
